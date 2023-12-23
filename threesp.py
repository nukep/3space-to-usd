# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO
from enum import Enum


if getattr(kaitaistruct, 'API_VERSION', (0, 9)) < (0, 9):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Threesp(KaitaiStruct):

    class Filetype(Enum):
        scene = 1
        material = 2

    class Gridfloor(Enum):
        xy = 0
        xz = 1
        yz = 2

    class Objtype(Enum):
        cylinder = 2
        line = 4
        point = 6
        sphere = 11
        triangle_set = 15
        text = 16
        group_start = 17
        group_finish = 18
        spot_light = 20
        distant_light = 21
        point_light = 22
        indexed_face_set = 28
        cube = 31
        cone = 32
        torus = 34
        character = 35
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.contents = Threesp.Container(self._io, self, self._root)

    class Mat4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.elements = []
            for i in range(16):
                self.elements.append(self._io.read_f4le())



    class ObjectSphereData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.radius = self._io.read_f4le()


    class ObjectCharacterDataMesh2(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_verts = self._io.read_u4le()
            self.verts = []
            for i in range((self.num_verts * 3)):
                self.verts.append(self._io.read_f4le())

            self.num_faces = self._io.read_u4le()
            self.num_face_indices = self._io.read_u4le()
            self.face_indices = []
            for i in range(self.num_face_indices):
                self.face_indices.append(self._io.read_s4le())

            self.num_normals = self._io.read_u4le()
            self.normals = []
            for i in range((self.num_normals * 3)):
                self.normals.append(self._io.read_f4le())

            self.someother = self._io.read_u4le()
            self._unnamed8 = self._io.read_bytes(1)
            self.num_normal_indices = self._io.read_u4le()
            self.normal_indices = []
            for i in range(self.num_normal_indices):
                self.normal_indices.append(self._io.read_s4le())

            self.num_unk5data = self._io.read_u4le()
            self.unk5data = []
            for i in range(self.num_unk5data):
                self.unk5data.append(self._io.read_f4le())

            self.num_unk6 = self._io.read_u4le()
            self.num_unk7data = self._io.read_u4le()
            self.unk7data = []
            for i in range(self.num_unk7data):
                self.unk7data.append(self._io.read_s4le())



    class ObjectTorusData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.major_radius = self._io.read_f4le()
            self.minor_radius = self._io.read_f4le()


    class ObjectUnk2data(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.u1 = self._io.read_f4le()
            self.u2 = self._io.read_f4le()
            self.u3 = self._io.read_f4le()
            self.u4_zero = self._io.read_bytes(12)
            self.u5 = self._io.read_f4le()
            self.u6_zero = self._io.read_bytes(3)
            self.u7 = self._io.read_u1()
            self.u8 = self._io.read_u1()
            self.u9 = self._io.read_bytes(11)


    class ObjectTriangleSetData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.num_verts = self._io.read_u4le()
            self.verts = []
            for i in range((self.num_verts * 3)):
                self.verts.append(self._io.read_f4le())

            self.num_faces = self._io.read_u4le()
            self.faces = []
            for i in range(self.num_faces):
                self.faces.append(Threesp.ObjectTriangleFace(self._io, self, self._root))

            self.num_normals = self._io.read_u4le()
            self.normals = []
            for i in range((self.num_normals * 3)):
                self.normals.append(self._io.read_f4le())

            self.someother = self._io.read_u4le()


    class ObjectIndexedFaceSetData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk1 = self._io.read_f4le()
            self.unk2 = self._io.read_f4le()
            self.unk3 = self._io.read_f4le()
            self.unk4 = self._io.read_f4le()
            self.unk5 = self._io.read_f4le()
            self.unk6 = self._io.read_f4le()
            self.unk7 = self._io.read_u1()
            self.num_verts = self._io.read_u4le()
            self.verts = []
            for i in range((self.num_verts * 3)):
                self.verts.append(self._io.read_f4le())

            self.num_faces = self._io.read_u4le()
            self.num_face_indices = self._io.read_u4le()
            self.face_indices = []
            for i in range(self.num_face_indices):
                self.face_indices.append(self._io.read_s4le())

            self.num_normals = self._io.read_u4le()
            self.normals = []
            for i in range((self.num_normals * 3)):
                self.normals.append(self._io.read_f4le())

            self.someother = self._io.read_u4le()
            self._unnamed15 = self._io.read_bytes(1)
            self.num_normal_indices = self._io.read_u4le()
            self.normal_indices = []
            for i in range(self.num_normal_indices):
                self.normal_indices.append(self._io.read_s4le())

            self.unk8 = self._io.read_bytes(12)


    class Materialfile(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk = self._io.read_bytes(1)
            self.has_thumbnail = self._io.read_u1()
            if self.has_thumbnail != 0:
                self.thumbnail = Threesp.Rgbimage(self._io, self, self._root)

            self.material = Threesp.Material(self._io, self, self._root)


    class ObjectLineData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.p0 = Threesp.Vec3(self._io, self, self._root)
            self.p1 = Threesp.Vec3(self._io, self, self._root)


    class ObjectSpotLightData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.color = Threesp.Rgba4(self._io, self, self._root)
            self.unk2 = self._io.read_bytes(2)
            self.lookat_vector = Threesp.Vec3(self._io, self, self._root)
            self.unk3 = self._io.read_f4le()
            self.unk4 = self._io.read_f4le()


    class Rgbimage(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.width = self._io.read_u4le()
            self.height = self._io.read_u4le()
            self.data = self._io.read_bytes(((self.width * self.height) * 3))


    class KeyframeData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.frame_number = self._io.read_u4le()
            self.matrix = Threesp.Mat4(self._io, self, self._root)
            self.translate = Threesp.Vec3(self._io, self, self._root)
            self.scale = Threesp.Vec3(self._io, self, self._root)
            self.rotate = Threesp.Vec3(self._io, self, self._root)
            self.shear = Threesp.Vec3(self._io, self, self._root)


    class ObjectUnknownData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk1 = self._io.read_u1()
            self.unk2 = self._io.read_u1()
            if self.unk2 != 0:
                self.unk2data = Threesp.ObjectUnk2data(self._io, self, self._root)

            self.unk3 = self._io.read_u1()
            if self.unk3 != 0:
                self.unk3data = []
                for i in range(3):
                    self.unk3data.append(self._io.read_f4le())




    class Sstr(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len = self._io.read_u1()
            self.value = (self._io.read_bytes(self.len)).decode(u"ASCII")


    class ObjectTriangleFace(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.vert1 = self._io.read_u4le()
            self.vert2 = self._io.read_u4le()
            self.vert3 = self._io.read_u4le()
            self.unk = self._io.read_u1()


    class Container(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.header = Threesp.Header(self._io, self, self._root)
            if self.header.filetype == Threesp.Filetype.scene:
                self.scene = Threesp.Scene(self._io, self, self._root)

            if self.header.filetype == Threesp.Filetype.material:
                self.materialfile = Threesp.Materialfile(self._io, self, self._root)



    class ObjectPointLightData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.unk1 = self._io.read_f4le()
            self.color = Threesp.Rgba4(self._io, self, self._root)
            self.unk2 = self._io.read_bytes(2)


    class TangentData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.endpoint = Threesp.Vec3(self._io, self, self._root)
            self.prev_cpoint = Threesp.Vec3(self._io, self, self._root)
            self.next_cpoint = Threesp.Vec3(self._io, self, self._root)
            self.frame_number = self._io.read_u4le()


    class Layer(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.name = Threesp.Sstr(self._io, self, self._root)
            self.enabled = self._io.read_u1()
            self.material_index = self._io.read_u4le()


    class ObjectCharacterData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.character = (self._io.read_bytes(1)).decode(u"ASCII")
            self._unnamed1 = self._io.read_bytes(142)
            self.font = Threesp.Sstr(self._io, self, self._root)
            self.enable1 = self._io.read_u1()
            if self.enable1 != 0:
                self.mesh1 = Threesp.ObjectCharacterDataMesh1(self._io, self, self._root)

            self.enable2 = self._io.read_u1()
            if self.enable2 != 0:
                self.mesh2 = Threesp.ObjectCharacterDataMesh2(self._io, self, self._root)



    class Scene(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.has_thumbnail = self._io.read_u1()
            if self.has_thumbnail != 0:
                self.thumbnail = Threesp.Rgbimage(self._io, self, self._root)

            self.show_lights = self._io.read_u1()
            self.lock_viewport = []
            for i in range(4):
                self.lock_viewport.append(self._io.read_u1())

            self.unk1 = self._io.read_bytes(1)
            self.view_lookat = []
            for i in range(5):
                self.view_lookat.append(Threesp.Vec3(self._io, self, self._root))

            self.view_camera_pos = []
            for i in range(5):
                self.view_camera_pos.append(Threesp.Vec3(self._io, self, self._root))

            self.view_up_vectors = []
            for i in range(5):
                self.view_up_vectors.append(Threesp.Vec3(self._io, self, self._root))

            self.view_perspective_on = []
            for i in range(5):
                self.view_perspective_on.append(self._io.read_u1())

            self.ambient_light_color = Threesp.Rgba4(self._io, self, self._root)
            self.somedata = []
            for i in range(30):
                self.somedata.append(self._io.read_u1())

            self.gridfloor = KaitaiStream.resolve_enum(Threesp.Gridfloor, self._io.read_u1())
            self.prop_31 = self._io.read_u1()
            self.prop_32 = self._io.read_u1()
            self.unk10 = self._io.read_bytes(1)
            self.somedata2 = []
            for i in range(3):
                self.somedata2.append(self._io.read_f4le())

            self.unk12 = self._io.read_bytes(1)
            self.background_color = Threesp.Rgba4(self._io, self, self._root)
            self.unk11 = self._io.read_bytes(1)
            self.enable_background_texture = self._io.read_u1()
            self.unk22 = self._io.read_u1()
            if self.enable_background_texture != 0:
                self.background_texture = Threesp.Sstr(self._io, self, self._root)

            self.unk20 = self._io.read_bytes(13)
            self.fog_density = self._io.read_f4le()
            self.fog_color = Threesp.Rgba4(self._io, self, self._root)
            self._unnamed25 = self._io.read_bytes(4)
            self.headlights_on = self._io.read_u1()
            self._unnamed27 = self._io.read_bytes(1)
            self.headlight_color = Threesp.Rgba4(self._io, self, self._root)
            self._unnamed29 = self._io.read_bytes(1)
            self.somedata4 = []
            for i in range(13):
                self.somedata4.append(self._io.read_f4le())

            self.view_zoom = []
            for i in range(5):
                self.view_zoom.append(self._io.read_f4le())

            self.view_rotate1 = []
            for i in range(5):
                self.view_rotate1.append(self._io.read_f4le())

            self.view_rotate2 = []
            for i in range(5):
                self.view_rotate2.append(self._io.read_f4le())

            self.somedata5 = []
            for i in range(21):
                self.somedata5.append(self._io.read_f4le())

            self.num_frames = self._io.read_u4le()
            self.unknown = self._io.read_bytes(12)
            self.font_default = Threesp.Sstr(self._io, self, self._root)
            self.fontunk1 = self._io.read_u1()
            self.num_fontentries = self._io.read_u1()
            if self.fontunk1 != 0:
                self.fontunk3 = self._io.read_u4le()

            self.fontentries = []
            for i in range(self.num_fontentries):
                self.fontentries.append(self._io.read_bytes(36))

            self.unk2 = self._io.read_bytes(1)
            self.frames_per_second = self._io.read_f4le()
            self.num_layers = self._io.read_u4le()
            self.layers = []
            for i in range(self.num_layers):
                self.layers.append(Threesp.Layer(self._io, self, self._root))

            self.unk6 = self._io.read_s4le()
            self.num_materials = self._io.read_u4le()
            self.materials = []
            for i in range(self.num_materials):
                self.materials.append(Threesp.Material(self._io, self, self._root))

            self.num_objects = self._io.read_u4le()
            if True:
                self.objects = []
                for i in range(self.num_objects):
                    self.objects.append(Threesp.Objekt(self._io, self, self._root))


            self.magicend = self._io.read_bytes(1)
            if not self.magicend == b"\x63":
                raise kaitaistruct.ValidationNotEqualError(b"\x63", self.magicend, self._io, u"/types/scene/seq/51")


    class Rgba4(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.r = self._io.read_f4le()
            self.g = self._io.read_f4le()
            self.b = self._io.read_f4le()
            self.a = self._io.read_f4le()


    class ObjectDistantLightData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.unk = self._io.read_f4le()
            self.color = Threesp.Rgba4(self._io, self, self._root)
            self.unk2 = self._io.read_bytes(2)


    class ObjectCubeData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.size = Threesp.Vec3(self._io, self, self._root)


    class Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.magic = self._io.read_bytes(16)
            if not self.magic == b"\x33\x53\x70\x61\x63\x65\x20\x50\x75\x62\x6C\x69\x73\x68\x65\x72":
                raise kaitaistruct.ValidationNotEqualError(b"\x33\x53\x70\x61\x63\x65\x20\x50\x75\x62\x6C\x69\x73\x68\x65\x72", self.magic, self._io, u"/types/header/seq/0")
            self.unused1 = self._io.read_bytes(16)
            self.version = self._io.read_u4le()
            self.filetype = KaitaiStream.resolve_enum(Threesp.Filetype, self._io.read_u4le())


    class Material(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.index = self._io.read_u4le()
            self.is_mirror = self._io.read_u1()
            self.name = Threesp.Sstr(self._io, self, self._root)
            self.texture_filename = Threesp.Sstr(self._io, self, self._root)
            self.unk1 = self._io.read_u1()
            self.unk_filename = Threesp.Sstr(self._io, self, self._root)
            self.num_anim_keyframes = self._io.read_u4le()
            self.frames = []
            for i in range((1 if self.num_anim_keyframes < 1 else self.num_anim_keyframes)):
                self.frames.append(Threesp.MaterialFrame(self._io, self, self._root))



    class Vec3(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.x = self._io.read_f4le()
            self.y = self._io.read_f4le()
            self.z = self._io.read_f4le()


    class Objekt(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.type = KaitaiStream.resolve_enum(Threesp.Objtype, self._io.read_u1())
            self.visible = self._io.read_u1()
            self.material_index = self._io.read_s4le()
            self.layer_index = self._io.read_s4le()
            self.name = Threesp.Sstr(self._io, self, self._root)
            self.has_transform_matrix = self._io.read_u1()
            if self.has_transform_matrix != 0:
                self.transform_matrix = Threesp.Mat4(self._io, self, self._root)

            self.has_animation = self._io.read_u1()
            if self.has_animation != 0:
                self.animation_data = Threesp.AnimationData(self._io, self, self._root)

            self.unkdata = Threesp.ObjectUnknownData(self._io, self, self._root)
            _on = self.type
            if _on == Threesp.Objtype.cube:
                self.data = Threesp.ObjectCubeData(self._io, self, self._root)
            elif _on == Threesp.Objtype.line:
                self.data = Threesp.ObjectLineData(self._io, self, self._root)
            elif _on == Threesp.Objtype.text:
                self.data = Threesp.ObjectTextData(self._io, self, self._root)
            elif _on == Threesp.Objtype.spot_light:
                self.data = Threesp.ObjectSpotLightData(self._io, self, self._root)
            elif _on == Threesp.Objtype.point_light:
                self.data = Threesp.ObjectPointLightData(self._io, self, self._root)
            elif _on == Threesp.Objtype.cone:
                self.data = Threesp.ObjectConeData(self._io, self, self._root)
            elif _on == Threesp.Objtype.cylinder:
                self.data = Threesp.ObjectCylinderData(self._io, self, self._root)
            elif _on == Threesp.Objtype.sphere:
                self.data = Threesp.ObjectSphereData(self._io, self, self._root)
            elif _on == Threesp.Objtype.torus:
                self.data = Threesp.ObjectTorusData(self._io, self, self._root)
            elif _on == Threesp.Objtype.triangle_set:
                self.data = Threesp.ObjectTriangleSetData(self._io, self, self._root)
            elif _on == Threesp.Objtype.character:
                self.data = Threesp.ObjectCharacterData(self._io, self, self._root)
            elif _on == Threesp.Objtype.distant_light:
                self.data = Threesp.ObjectDistantLightData(self._io, self, self._root)
            elif _on == Threesp.Objtype.indexed_face_set:
                self.data = Threesp.ObjectIndexedFaceSetData(self._io, self, self._root)
            elif _on == Threesp.Objtype.point:
                self.data = Threesp.ObjectPointData(self._io, self, self._root)
            self.magic_end = self._io.read_bytes(4)
            if not self.magic_end == b"\x10\x32\x34\x12":
                raise kaitaistruct.ValidationNotEqualError(b"\x10\x32\x34\x12", self.magic_end, self._io, u"/types/objekt/seq/11")


    class ObjectTextData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.text = Threesp.Sstr(self._io, self, self._root)
            self._unnamed1 = self._io.read_bytes(28)
            self.font = Threesp.Sstr(self._io, self, self._root)


    class ObjectCharacterDataMesh1(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.len_unk2 = self._io.read_u4le()
            self.unk2data = []
            for i in range((self.len_unk2 * 3)):
                self.unk2data.append(self._io.read_f4le())

            self.num_unk3 = self._io.read_u4le()
            self.num_unk3data = self._io.read_u4le()
            self.unk3data = []
            for i in range(self.num_unk3data):
                self.unk3data.append(self._io.read_s4le())



    class ObjectConeData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.radius = self._io.read_f4le()
            self.height = self._io.read_f4le()


    class AnimationData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.unk = self._io.read_f4le()
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.num_keyframes = self._io.read_u4le()
            self.keyframes = []
            for i in range(self.num_keyframes):
                self.keyframes.append(Threesp.KeyframeData(self._io, self, self._root))

            self.has_custom_tangents = self._io.read_u1()
            if self.has_custom_tangents != 0:
                self.num_tangent_keyframes = self._io.read_u4le()

            if self.has_custom_tangents != 0:
                self.tangent_keyframes = []
                for i in range(self.num_tangent_keyframes):
                    self.tangent_keyframes.append(Threesp.TangentData(self._io, self, self._root))




    class ObjectCylinderData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)
            self.radius = self._io.read_f4le()
            self.height = self._io.read_f4le()
            self.has_cap_at_height = self._io.read_u1()
            self.has_cap_at_origin = self._io.read_u1()
            self.has_outer = self._io.read_u1()


    class MaterialFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ambient = Threesp.Rgba4(self._io, self, self._root)
            self.diffuse = Threesp.Rgba4(self._io, self, self._root)
            self.specular = Threesp.Rgba4(self._io, self, self._root)
            self.emissive = Threesp.Rgba4(self._io, self, self._root)
            self.shininess = self._io.read_f4le()
            self.transparency = self._io.read_f4le()
            self.refractive_index = self._io.read_f4le()
            self.frame_number = self._io.read_u4le()


    class ObjectPointData(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pos = Threesp.Vec3(self._io, self, self._root)



