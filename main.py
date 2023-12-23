from pxr import Usd, UsdGeom, Gf, Sdf, UsdShade, UsdLux
import numpy as np
import itertools
import math


def np_mat4_to_GfMatrix4d(mat4):
    return Gf.Matrix4d(*list(np.array(mat4.transpose().flatten(), dtype=float)))

def split_delimited_list(l, delimiter):
    grouped = itertools.groupby(l, lambda x: x == delimiter)
    result = [list(g) for is_delimiter, g in grouped if not is_delimiter]
    return result

from collections import namedtuple

Node = namedtuple('Node', ['obj', 'children'])

def flat_objects_to_nested(objects):
    '''Returns a list of nodes. A node contains a reference to an object, as well as a list of descendant nodes.'''

    root = []
    parent_stack = [root]
    
    for obj in objects:
        children = None
        push_to_parent_stack = False
        
        if obj.type == Threesp.Objtype.group_start:
            children = []
            push_to_parent_stack = True
        elif obj.type == Threesp.Objtype.group_finish:
            parent_stack.pop()
            continue

        parent_stack[-1].append(Node(obj, children))

        if push_to_parent_stack:
            parent_stack.append(children)
    
    return root

import re

def sanitize_name(s):
    # Alphanumeric and underscore
    regex = re.compile(r'[^a-zA-Z0-9_]')
    new_str = re.sub(regex, '', s)

    if len(new_str) == 0:
        return '_'

    if new_str[0] > '0' and new_str[0] < '9':
        return '_' + new_str

    return new_str

def unique_name_builder():
    names = set()

    def mkname(s):
        new_name = sanitize_name(s)
        i = 2
        while new_name in names:
            new_name = sanitize_name(f"{s}{i}")
            i += 1
        names.add(new_name)
        return new_name
    return mkname


def make_path(elements):
    p = Sdf.Path('/')
    for s in elements:
        p = p.AppendChild(s)
    return p

def add_cube(stage, path, pos, size):
    container = UsdGeom.Xform.Define(stage, path)
    cube = UsdGeom.Cube.Define(stage, path.AppendChild('cube'))
    cube.CreateSizeAttr(1)
    x,y,z = pos
    sx,sy,sz = size

    cube.AddTranslateOp().Set((x,y,z))
    cube.AddScaleOp().Set((abs(sx),abs(sy),abs(sz)))
    # use absolute scales, because certain USD clients don't like inverted cubes
    cube.AddTranslateOp(opSuffix='corner').Set(
        (0.5 if sx > 0 else -0.5,
         0.5 if sy > 0 else -0.5,
         0.5 if sz > 0 else -0.5)
    )

    return container, cube

def add_sphere(stage, path, pos, radius):
    container = UsdGeom.Xform.Define(stage, path)
    sphere = UsdGeom.Sphere.Define(stage, path.AppendChild('sphere'))
    sphere.CreateRadiusAttr(radius)
    x,y,z = pos
    sphere.AddTranslateOp().Set((x,y,z))

    return container, sphere

def add_cone(stage, path, pos, radius, height):
    container = UsdGeom.Xform.Define(stage, path)
    cone = UsdGeom.Cone.Define(stage, path.AppendChild('cone'))
    cone.CreateRadiusAttr(abs(radius))
    cone.CreateHeightAttr(abs(height))
    cone.CreateAxisAttr('Z')

    x,y,z = pos
    cone.AddTranslateOp().Set((x,y,z))

    # not all usd clients handle negative heights well
    # Fusion will flip the normals and we see the inside of the cone
    if height < 0:
        cone.AddRotateYOp().Set(180)
        height = -height

    cone.AddTranslateOp(opSuffix='base').Set((0, 0, height/2))

    return container, cone

def add_cylinder(stage, path, pos, radius, height):
    container = UsdGeom.Xform.Define(stage, path)
    cyl = UsdGeom.Cylinder.Define(stage, path.AppendChild('cylinder'))
    cyl.CreateRadiusAttr(abs(radius))
    cyl.CreateHeightAttr(abs(height))
    cyl.CreateAxisAttr('Z')

    x,y,z = pos
    cyl.AddTranslateOp().Set((x,y,z))

    if height < 0:
        cyl.AddRotateYOp().Set(180)
        height = -height

    cyl.AddTranslateOp(opSuffix='base').Set((0, 0, height/2))

    return container, cyl

def build_mesh(stage, path, face_indices_grouped, verts):
    mesh = UsdGeom.Mesh.Define(stage, path)

    # some USD clients (ahem, Fusion) assume a subdivided mesh. These are crappy 90's graphics, so they're definitely _not_ subdivided.
    mesh.CreateSubdivisionSchemeAttr('none')

    face_vertex_counts = [len(x) for x in face_indices_grouped]
    face_vertex_indices = [x for ind in face_indices_grouped for x in ind]
    points = [tuple(verts[i:i+3]) for i in range(0, len(verts), 3)]

    mesh.CreateFaceVertexCountsAttr(face_vertex_counts)
    mesh.CreateFaceVertexIndicesAttr(face_vertex_indices)
    mesh.CreatePointsAttr(points)

    return mesh

def add_mesh_from_indexed_face_set_data(stage, path, data):
    mesh = build_mesh(stage, path, split_delimited_list(data.face_indices, -1), data.verts)
    return mesh

def add_mesh_from_triangle_set_data(stage, path, data):
    face_indices_grouped = [[f.vert1,f.vert2,f.vert3] for f in data.faces]
    mesh = build_mesh(stage, path, face_indices_grouped, data.verts)
    return mesh

def add_character(stage, path, data):
    # add a character from text
    if data.enable2:
        mesh = build_mesh(stage, path, split_delimited_list(data.mesh2.face_indices, -1), data.mesh2.verts)
        return mesh
    else:
        # some characters have no mesh, such as the space character
        return None

# 3space interpolates translations using tangent control points. There are two "handles", as well as a central endpoint.

# Effectively, this represents a 3d cubic bezier curve.


# $$
# P(t) = \begin{bmatrix}1&t&t^2&t^3\end{bmatrix} 
# \begin{bmatrix}
# 1 & 0 & 0 & 0\\
# -3 & 3 & 0 & 0\\
# 3 & -6 & 3 & 0\\
# -1 & 3 & -3 & 1
# \end{bmatrix} \begin{bmatrix}P_0\\P_1\\P_2\\P_3\end{bmatrix} 
# $$


def sample_tangents(tangents):
    '''Returns a list of translations'''

    # we're applying a cubic bezier curve interpolation

    # there's a really concise way to calculate these with matrices.

    first_frame_number = tangents[0].frame_number
    last_frame_num = tangents[-1].frame_number

    curve_characteristic = np.array([
        [1,0,0,0],
        [-3,3,0,0],
        [3,-6,3,0],
        [-1,3,-3,1]
    ])

    points = []

    for frame_num in range(first_frame_number, last_frame_num):
        for i, tangent in reversed(list(enumerate(tangents))):
            if frame_num >= tangent.frame_number:
                break
        a = tangents[i]
        b = tangents[i+1]

        t = (frame_num - a.frame_number) / (b.frame_number - a.frame_number)

        # set each of the control points as a row vector
        ctrls = np.array([a.endpoint.np(),
                          a.next_cpoint.np(),
                          b.prev_cpoint.np(),
                          b.endpoint.np()])

        # our resulting point is a row vector
        point = np.array([1, t, t**2, t**3]) @ curve_characteristic @ ctrls

        points.append(tuple(point))
    
    # append the last point
    points.append(tuple(tangents[-1].endpoint.np()))

    return (first_frame_number, points)

def add_animation(xform, a):
    '''Add transform time samples to the USD xform, based on animation data'''

    translate = xform.AddTranslateOp()
    orient = xform.AddOrientOp()
    # TODO - add "shear". USD doesn't have a shear xformop.
    scale = xform.AddScaleOp()
    pivot = xform.AddTranslateOp(opSuffix='pos')
    pivot.Set(tuple(-a.pos.np()))

    for kf in a.keyframes:
        frame_num = kf.frame_number

        # note: the translation information from the .3sp file is completely ignored here
        # TODO: unless has_custom_tangents is off? I haven't tested this, but none of the provided files do so.

        # convert to quaternions. 3space performs interpolations on quaternions.
        quat = eulerxyz_to_quaternion(kf.rotate.x, kf.rotate.y, kf.rotate.z)

        # xyzw -> wxyz ordering
        orient.Set(Gf.Quatf(quat[3], quat[0], quat[1], quat[2]), frame_num)

        scale.Set((kf.scale.x, kf.scale.y, kf.scale.z), frame_num)

    if a.has_custom_tangents:
        # USD only supports linear and hold interpolation.
        # We have to sample the bezier curve interpolations ourselves.
        tangent_frame_num, samples = sample_tangents(a.tangent_keyframes)

        for point in samples:
            translate.Set(point, tangent_frame_num)
            tangent_frame_num += 1

def lerp(a,b,t):
    return (b-a)*t + a

def add_materials(stage, materials):
    mat_lookup = {}

    mkname = unique_name_builder()
    for i, mat in enumerate(materials):
        name = mkname(mat.name.value)

        matprim = stage.DefinePrim(f'/root/Materials/{name}')
        matprim.SetDisplayName(mat.name.value)
        matprim.GetInherits().AddInherit('/_class_material')
        mat_lookup[i] = UsdShade.Material(matprim)

        diffuse_in   = matprim.GetAttributeAtPath('Shader.inputs:diffuseColor')
        opacity_in   = matprim.GetAttributeAtPath('Shader.inputs:opacity')
        metallic_in  = matprim.GetAttributeAtPath('Shader.inputs:metallic')
        roughness_in = matprim.GetAttributeAtPath('Shader.inputs:roughness')

        if mat.is_mirror:
            metallic_in.Set(0.6)
            roughness_in.Set(0.15)
        else:
            metallic_in.Set(0)
            roughness_in.Set(0.5)

        # Set the materials. Animate them if the material supports animation.
        single_frame = len(mat.frames) == 1
        for frame in mat.frames:
            color = (frame.diffuse.r, frame.diffuse.g, frame.diffuse.b)
            opacity = 1-frame.transparency

            # ignore the color of the specular, use it as a measure of "how specular"
            specular = sum([frame.specular.r, frame.specular.g, frame.specular.b])/3
            shininess = frame.shininess * specular

            roughness = lerp(0.65, 0.2, shininess)

            if not mat.is_mirror:
                if single_frame:
                    roughness_in.Set(roughness)
                else:
                    roughness_in.Set(roughness, frame.frame_number)

            # there are ambient and emission properties, but they don't seem to have an effect in 3space

            if single_frame:
                diffuse_in.Set(color)
                opacity_in.Set(opacity)
            else:
                diffuse_in.Set(color, frame.frame_number)
                opacity_in.Set(opacity, frame.frame_number)

    return mat_lookup

def add_cameras(stage, view_lookat, view_camera_pos, view_up_vectors, view_perspective_on, scaleby):
    mkname = unique_name_builder()
    for camera_id in range(5):
        is_persp = view_perspective_on[camera_id] != 0
        if is_persp:
            # 3space's field of view is defined by the height of the viewport

            cameraname = mkname('persp')
            # rename the first persp camera to main_cam
            if cameraname == 'persp':
                cameraname = 'main_cam'
            camera = UsdGeom.Camera.Define(stage, f'/root/Cameras/{cameraname}')
            
            z_basis = view_camera_pos[camera_id].np() - view_lookat[camera_id].np()
            z_basis = z_basis / numpy.linalg.norm(z_basis)
            y_basis = view_up_vectors[camera_id].np()
            y_basis = y_basis / numpy.linalg.norm(y_basis)
            x_basis = np.cross(y_basis, z_basis)
            camera_orient = np.array([ x_basis,
                                    y_basis,
                                    z_basis ]).transpose()
            cameramat = mat3_to_mat4(camera_orient, translate=view_camera_pos[camera_id].np() * scaleby)

            # The focal length of the camera in 3space is about (exactly?) 35mm
            camera.CreateFocalLengthAttr(35)
            # camera.CreateClippingRangeAttr((0.01, 10000))

            camera.AddTransformOp().Set(np_mat4_to_GfMatrix4d(cameramat))


def makeusd(usd_filename, filename, scene):
    stage = Usd.Stage.CreateNew(usd_filename)

    stage.GetRootLayer().subLayerPaths.append('base.usda')

    rootxform = UsdGeom.Xform(stage.GetPrimAtPath('/root'))
    geomxform = UsdGeom.Xform(stage.GetPrimAtPath('/root/Geom'))

    UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.y)
    stage.SetStartTimeCode(1)
    stage.SetEndTimeCode(scene.num_frames)
    stage.SetDefaultPrim(stage.GetPrimAtPath('/root'))
    stage.SetFramesPerSecond(scene.frames_per_second)
    stage.SetTimeCodesPerSecond(scene.frames_per_second)

    mat_lookup = add_materials(stage, scene.materials)

    nodes = flat_objects_to_nested(scene.objects)

    def traverse_node(curpath, node):
        obj = node.obj

        geo = None
        if obj.type == Threesp.Objtype.indexed_face_set:
            xform = add_mesh_from_indexed_face_set_data(stage, curpath, obj.data)
            geo = xform
        elif obj.type == Threesp.Objtype.triangle_set:
            xform = add_mesh_from_triangle_set_data(stage, curpath, obj.data)
            geo = xform
        elif obj.type == Threesp.Objtype.character:
            xform = add_character(stage, curpath, obj.data)
            geo = xform
        elif obj.type == Threesp.Objtype.cube:
            xform,geo = add_cube(stage, curpath, obj.data.pos.np(), obj.data.size.np())
        elif obj.type == Threesp.Objtype.sphere:
            xform,geo = add_sphere(stage, curpath, obj.data.pos.np(), obj.data.radius)
        elif obj.type == Threesp.Objtype.cone:
            xform,geo = add_cone(stage, curpath, obj.data.pos.np(), obj.data.radius, obj.data.height)
        elif obj.type == Threesp.Objtype.cylinder:
            xform,geo = add_cylinder(stage, curpath, obj.data.pos.np(), obj.data.radius, obj.data.height)
        elif obj.type == Threesp.Objtype.group_start:
            xform = UsdGeom.Xform.Define(stage, curpath)
        elif obj.type == Threesp.Objtype.text:
            return
        else:
            print(f'WARNING: unhandled type: {obj.type}, in file {filename}')
            xform = UsdGeom.Xform.Define(stage, curpath)

        if not xform:
            return
        
        # Set the display name to whatever was in 3space
        xform.GetPrim().SetDisplayName(node.obj.name.value)
        
        # calculate the extents
        if geo:
            boundable = UsdGeom.Boundable(geo)
            extent = boundable.ComputeExtent(0)
            boundable.CreateExtentAttr().Set(extent)
        
        if obj.material_index != -1 and geo is not None:
            matbinding = UsdShade.MaterialBindingAPI(geo)
            matbinding.Bind(mat_lookup[obj.material_index])

        if obj.has_animation:
            # animation ignores the transform matrix

            add_animation(xform, obj.animation_data)
        elif obj.has_transform_matrix:
            mat = obj.transform_matrix.np()
            xform.AddTransformOp().Set(np_mat4_to_GfMatrix4d(mat))

        if node.children:
            mkname = unique_name_builder()
            for cnode in node.children:
                cpath = xform.GetPath().AppendChild(mkname(cnode.obj.name.value))
                traverse_node(cpath, cnode)

    mkname = unique_name_builder()
    for node in nodes:
        cpath = geomxform.GetPath().AppendChild(mkname(node.obj.name.value))
        traverse_node(cpath, node)

    # Get a sense of the magnitude of the scene's scale.
    # The files are wildly inconsistent on using units of 0.01's, 1's, 100's, and 1000's.

    bboxcache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), includedPurposes=[UsdGeom.Tokens.default_])
    worldbounds = bboxcache.ComputeWorldBound(stage.GetPrimAtPath('/root'))
    centroid = worldbounds.ComputeCentroid()
    worldsize = worldbounds.GetBox()
    x,y,z = worldsize.GetSize()
    xyzsort = sorted([x,y,z])
    primary_magnitude = round(math.log(xyzsort[2], 10))
    secondary_magnitude = round(math.log(xyzsort[1], 10))

    target_magnitude = 1
    scaleby = 10**(-primary_magnitude + target_magnitude)

    # compensate accordingly
    geomxform.AddScaleOp().Set((scaleby, scaleby, scaleby))

    add_cameras(stage, scene.view_lookat, scene.view_camera_pos, scene.view_up_vectors, scene.view_perspective_on, scaleby)


    if scene.gridfloor == Threesp.Gridfloor.xy:
        # If the file's grid floor is XY, it implies Z is up.
        # to make things consistent, we want Y to be up.
        # We'll compensate by rotating the root primitive (everything, including the cameras)
        rootxform.AddRotateXOp().Set(-90)

    stage.GetRootLayer().Save()


from threesp import Threesp
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
import numpy as np
import numpy.linalg
from scipy.spatial.transform import Rotation as R

# extend the classes generated by kaitai struct with convenience methods

Threesp.Sstr.__repr__ = lambda self: self.value
Threesp.Vec3.np = lambda self: np.array([self.x, self.y, self.z])
Threesp.Vec3.__repr__ = lambda self: f'<Vec3 {self.np()}>'
Threesp.Vec3.col4 = lambda self: np.array([[self.x], [self.y], [self.z], [1]])

# assuming the matrix is stored in column-major order
Threesp.Mat4.np = lambda self: np.array(self.elements).reshape(4,4).transpose()

def mat4_to_mat3_orient(mat4):
    # take the top-left 3x3 matrix, effectively discarding the translation info
    return np.delete(np.delete(mat4, -1, axis=0), -1, axis=1)

def mat3_to_mat4(mat3, translate=None):
    '''Converts a 3x3 transform matrix to a 4x4 matrix'''
    new_matrix = np.eye(4)
    new_matrix[:3, :3] = mat3
    if translate is not None:
        new_matrix[:3, 3] = translate
    return new_matrix

def col3(x,y,z):
    return np.array([[x,y,z]]).transpose()
def col4(x,y,z,w=1):
    return np.array([[x,y,z,w]]).transpose()

def eulerxyz_to_mat4(x,y,z):
    return mat3_to_mat4(R.from_euler('xyz', [[x,y,z]], degrees=False).as_matrix())

def eulerxyz_to_quaternion(x,y,z):
    return R.from_euler('xyz', [[x,y,z]], degrees=False).as_quat()[0]

# all of these matrices are post-multiplied by a column vector.

def scale_to_mat4(x,y,z):
    return np.array([[x,0,0,0],
                     [0,y,0,0],
                     [0,0,z,0],
                     [0,0,0,1]])

def translate_to_mat4(x,y,z):
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]])

def shear_to_mat4(x,y,z):
    return np.array([[1,x,y,0],
                     [0,1,z,0],
                     [0,0,1,0],
                     [0,0,0,1]])
def test_animation_matrices(filename, scene):
    '''Tests that each calculated matrix in the file is equal to the composition of scale, then shear, then rotation, then translation'''
    pass_test = True

    for obj in scene.objects:
        if not obj.has_animation: continue
        a = obj.animation_data

        for kf,tkf in zip(a.keyframes, a.tangents):
            precalc_mat = kf.matrix.np()

            scalemat = scale_to_mat4(*kf.scale.np())
            rotmat = eulerxyz_to_mat4(*kf.rotate.np())
            transmat = translate_to_mat4(*kf.translate.np())
            shearmat = shear_to_mat4(*kf.shear.np())

            # diffs the precalc'd matrix with our composed matrix, and check if each element is within a threshold
            composed_mat = transmat @ rotmat @ shearmat @ scalemat
            matches_matrix = set(abs(precalc_mat - composed_mat).reshape(16) < 0.005) == {True}

            if not matches_matrix:
                print('DOES NOT MATCH', filename, obj.type, obj.name.value)
                pass_test = False
    return pass_test

import os

def processall(process):
    files = os.listdir('./all_3sp_files_raw_v1/')
    for filename in files:
        print(filename)
        with open(f'./all_3sp_files_raw_v1/{filename}', 'rb') as f:
            t = Threesp(KaitaiStream(f))

        if t.contents.header.filetype == Threesp.Filetype.scene:
            process(filename, t.contents.scene)

def processone(filename, process):
    with open(f'./all_3sp_files_raw_v1/{filename}', 'rb') as f:
        t = Threesp(KaitaiStream(f))

    if t.contents.header.filetype == Threesp.Filetype.scene:
        process(filename, t.contents.scene)


processone('567-Computer', lambda filename, scene: makeusd('Computer.usd', filename, scene))

