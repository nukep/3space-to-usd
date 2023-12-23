meta:
  id: threesp
  file-extension: 3sp
  endian: le
seq:
  - id: contents
    #size-eos: true
    #process: zlib
    type: container
types:
  container:
    seq:
      - id: header
        type: header
      - id: scene
        type: scene
        if: header.filetype == filetype::scene
      - id: materialfile
        type: materialfile
        if: header.filetype == filetype::material
  header:
    seq:
      - id: magic
        contents: '3Space Publisher'
      - id: unused1
        size: 16
      - id: version
        type: u4
      - id: filetype
        enum: filetype
        type: u4
  materialfile:
    seq:
      - id: unk   # always seems to be 0
        size: 1

      - id: has_thumbnail
        type: u1
      - id: thumbnail
        type: rgbimage
        if: has_thumbnail != 0
      - id: material
        type: material
  scene:
    seq:
      - id: has_thumbnail
        type: u1
      - id: thumbnail
        type: rgbimage
        if: has_thumbnail != 0
      - id: show_lights
        type: u1
      - id: lock_viewport
        type: u1
        repeat: expr
        repeat-expr: 4


      - id: unk1
        size: 1
        
      # The five viewports are in the order: top-left, bottom-right, top-right, bottom-right, floating window
      # The viewports are not explicitly tagged as "front", "right", "perspective" or any other tag.
      # Which view a camera is, is inferred by information about the camera.
        
      # The camera will look at this coordinate, as well as pivot around it when rotating (in 3space)
      - id: view_lookat
        type: vec3
        repeat: expr
        repeat-expr: 5
        
      - id: view_camera_pos
        type: vec3
        repeat: expr
        repeat-expr: 5
      
      - id: view_up_vectors
        type: vec3
        repeat: expr
        repeat-expr: 5
        
      - id: view_perspective_on
        type: u1
        repeat: expr
        repeat-expr: 5
      - id: ambient_light_color
        type: rgba4
      
      # These are just 0s and 1s. Probably flags.
      # somedata[2] = show axis
      # somedata[5] = show grid
      - id: somedata
        type: u1
        repeat: expr
        repeat-expr: 30
      
      - id: gridfloor
        type: u1
        enum: gridfloor
      - id: prop_31
        type: u1
      - id: prop_32
        type: u1
      
      # - id: some_v2_setting
      #   size: 3
      #   if: _root.contents.header.version == 2
      
      
      # this part of the file is weird and idk what it is.
      # the floats sometimes read better if unk10 isn't present
      # if it's in the order 4, 4, 1, 4  instead of 1, 4, 4, 4
      - id: unk10  # seems to always be 0
        size: 1
      - id: somedata2
        type: f4
        repeat: expr
        repeat-expr: 3
      
      - id: unk12
        size: 1
      - id: background_color
        type: rgba4
      - id: unk11
        size: 1
        
      - id: enable_background_texture
        type: u1
      - id: unk22
        type: u1
      - id: background_texture
        type: sstr
        if: enable_background_texture != 0
      - id: unk20
        size: 13
      - id: fog_density
        type: f4
      - id: fog_color
        type: rgba4
      - size: 4
      - id: headlights_on
        type: u1
      - size: 1
      - id: headlight_color
        type: rgba4
        
      # something 0x171 "when stationary draw scene using lines"
      - size: 1
      
      - id: somedata4
        type: f4
        repeat: expr
        repeat-expr: 13
      - id: view_zoom
        type: f4
        repeat: expr
        repeat-expr: 5
        
      - id: view_rotate1    # i believe this is along the y axis?
        type: f4
        repeat: expr
        repeat-expr: 5
      - id: view_rotate2    # and i believe this is along the xz plane (so either x or z). defaults to pi/8 (22.5 degrees)
        type: f4
        repeat: expr
        repeat-expr: 5
        
      - id: somedata5
        type: f4
        repeat: expr
        repeat-expr: 21
      
      - id: num_frames  # how long the animation should be
        type: u4
      
      - id: unknown
        size: 12
      
      - id: font_default
        type: sstr
      
      - id: fontunk1
        type: u1
      - id: num_fontentries
        type: u1
        
      - id: fontunk3
        type: u4
        if: fontunk1 != 0
        
      - id: fontentries
        size: 36
        repeat: expr
        repeat-expr: num_fontentries
      
      - id: unk2    # might be a flag to enable this part
        size: 1
      - id: frames_per_second
        type: f4
      - id: num_layers
        type: u4
      - id: layers
        type: layer
        repeat: expr
        repeat-expr: num_layers
      - id: unk6
        type: s4


      - id: num_materials
        type: u4
      - id: materials
        type: material
        repeat: expr
        repeat-expr: num_materials

      - id: num_objects
        type: u4
      - id: objects
        type: objekt
        repeat: expr
        repeat-expr: num_objects
        #repeat-expr: 33
        if: true
      
      - id: magicend
        contents: [0x63]
  layer:
    seq:
      - id: name
        type: sstr
      - id: enabled
        type: u1
      - id: material_index
        type: u4

  rgbimage:
    seq:
      - id: width
        type: u4
      - id: height
        type: u4
      - id: data
        size: width*height*3
  mat4:
    seq:
      - id: elements
        type: f4
        repeat: expr
        repeat-expr: 16
  material:
    seq:
      - id: index   # this index is useless, beacuse objects refer to materials by the index they appear in the file. files such as 558-Eyes.3sp have this issue.
        type: u4
      - id: is_mirror  # the material is reflective, like a mirror
        type: u1
      - id: name
        type: sstr
      - id: texture_filename
        type: sstr
      - id: unk1   # always seems to be 0
        type: u1
      - id: unk_filename
        type: sstr
      - id: num_anim_keyframes
        type: u4
      - id: frames
        type: material_frame
        repeat: expr
        repeat-expr: 'num_anim_keyframes < 1 ? 1 : (num_anim_keyframes)'
  material_frame:
    seq:
      - id: ambient
        type: rgba4
      - id: diffuse
        type: rgba4
      - id: specular
        type: rgba4
      - id: emissive
        type: rgba4
      - id: shininess         # 0 to 1
        type: f4
      - id: transparency      # 0 to 1
        type: f4
      - id: refractive_index  # 0 to 10
        type: f4
      - id: frame_number
        type: u4
  objekt:
    seq:
      - id: type
        type: u1
        enum: objtype
      - id: visible
        type: u1
      - id: material_index
        type: s4
      - id: layer_index
        type: s4
      - id: name
        type: sstr
      - id: has_transform_matrix
        type: u1
      - id: transform_matrix
        type: mat4
        if: has_transform_matrix != 0
      # 3space crashes if there's animation but no transform matrix
      # despite this, the animation ignores the transform matrix.
      # 3space will use the transform matrix on file load, but animation overrides it the moment a frame is played.
      - id: has_animation
        type: u1
      - id: animation_data
        type: animation_data
        if: has_animation != 0
      - id: unkdata
        type: object_unknown_data
      - id: data
        type:
          switch-on: type
          cases:
            'objtype::point_light': object_point_light_data
            'objtype::spot_light': object_spot_light_data
            'objtype::distant_light': object_distant_light_data
            'objtype::indexed_face_set': object_indexed_face_set_data
            'objtype::triangle_set': object_triangle_set_data
            'objtype::line': object_line_data
            'objtype::point': object_point_data
            'objtype::cylinder': object_cylinder_data
            'objtype::cube': object_cube_data
            'objtype::sphere': object_sphere_data
            'objtype::cone': object_cone_data
            'objtype::torus': object_torus_data
            'objtype::text': object_text_data
            'objtype::character': object_character_data
      - id: magic_end
        size: 4
        contents: [0x10, 0x32, 0x34, 0x12]
  object_point_light_data:
    seq:
      - id: pos
        type: vec3
      - id: unk1
        type: f4
      - id: color
        type: rgba4
      - id: unk2
        size: 2
  object_spot_light_data:
    seq:
      - id: pos
        type: vec3
      - id: color
        type: rgba4
      - id: unk2
        size: 2
      # relative to "pos". not normalized. length possibly indicates falloff?
      - id: lookat_vector
        type: vec3
      - id: unk3
        type: f4
      - id: unk4
        type: f4
  object_distant_light_data:
    seq:
      - id: pos
        type: vec3
      - id: unk
        type: f4
      - id: color
        type: rgba4
      - id: unk2
        size: 2
  object_cylinder_data:
    # cylinder is oriented on the XY plane. extrudes along positive-Z axis.
    # tubes and disks are also cylinders
    seq:
      - id: pos
        type: vec3
      - id: radius
        type: f4
      - id: height
        type: f4
      
      # a standard cylinder sets: (1,1,1)
      # a tube sets: (0,0,1)
      # a disk sets: (1,0,0) - height is 0
      - id: has_cap_at_height
        type: u1
      - id: has_cap_at_origin  # i.e. the cap that touches "pos"
        type: u1
      - id: has_outer
        type: u1
  object_torus_data:
    # torus is oriented on the XY plane
    seq:
      - id: pos
        type: vec3
      # measures the same way as blender
      - id: major_radius
        type: f4
      - id: minor_radius
        type: f4
  animation_data:
    seq:
      - id: unk   # always seems to be 0
        type: f4
      - id: pos
        type: vec3
      - id: num_keyframes
        type: u4
      - id: keyframes
        type: keyframe_data
        repeat: expr
        repeat-expr: num_keyframes
      - id: has_custom_tangents   # always seems to be 1
        type: u1
      - id: num_tangent_keyframes   # always seems to be equal to num_keyframes
        type: u4
        if: has_custom_tangents != 0
      - id: tangent_keyframes
        type: tangent_data
        repeat: expr
        repeat-expr: num_tangent_keyframes
        if: has_custom_tangents != 0
        
  keyframe_data:
    seq:
      - id: frame_number
        type: u4
      # 3space displays the matrix below on the keyframe and ignores scale/shear/rotate/translate
      # in-between frames don't use the matrix and instead rely on scale/shear/rotate/translate
      # in other words: the matrix is pre-computed for the keyframe and _should_ be the same as composing the scale/shear/rotate/translate
      # composition order is, local to world: scale, shear, rotate, translate (same order as Maya)
      
      # scale, rotate and shear are linearly interpolated.
      # translate is the exception, which is interpolated by tangents.
      # translate is IGNORED here. use the tangent data for translations!
      
      # rotations are interpolated with quaternions. the rotate value here is an euler XYZ, but 3space converts it to a quaternion for interpolation purposes
      # note: -pi/2 and +3pi/2 (-90 and +270 ) are equivalent rotations, and interpolate to "0" the exact same way.
      # 3space refuses to interpolate angles >= 120 degrees or <= -120 degrees (+-2pi/3 radians). If these exist in the file, it will hold the rotation until the next keyframe.
      #   the resulting quaternion I think would have its W component constrained to 0.5 <= w <= 1.0
      
      - id: matrix
        type: mat4
      - id: translate
        type: vec3
      - id: scale
        type: vec3
      # rotation is Euler XYZ, in radians.
      - id: rotate
        type: vec3
      # shear is XY, XZ, YZ (same order as Maya)
      - id: shear
        type: vec3
  tangent_data:
    seq:
      - id: endpoint
        type: vec3
      - id: prev_cpoint
        type: vec3
      - id: next_cpoint
        type: vec3
      - id: frame_number
        type: u4
  object_unknown_data:
    seq:
      - id: unk1
        type: u1
      - id: unk2
        type: u1
      - id: unk2data
        type: object_unk2data
        if: unk2 != 0
      - id: unk3
        type: u1
      - id: unk3data
        type: f4
        repeat: expr
        repeat-expr: 3
        if: unk3 != 0
        
  # // 00-03 is a float
  # // 04-07 is a float
  # // 08-0b is a float
  # // 0c-17 appears to always be 0
  # // 18-1b is a float
  # // 1c-1e appears to always be 0
  # // 1f is either 0 or 0x80
  # // 20 is either a 3 or a 0
  # // 21-2b appears to always be 0
  object_unk2data:
    seq:
      - id: u1
        type: f4
      - id: u2
        type: f4
      - id: u3
        type: f4
      - id: u4_zero
        size: 12
      - id: u5
        type: f4
      - id: u6_zero
        size: 3
      - id: u7
        type: u1
      - id: u8
        type: u1
      - id: u9
        size: 11
  object_point_data:
    seq:
      - id: pos
        type: vec3
  object_line_data:
    seq:
      - id: p0
        type: vec3
      - id: p1
        type: vec3
  object_cube_data:
    seq:
      # pos is a corner of the cube (NOT the center)
      - id: pos
        type: vec3
      # the other corner is pos + size (grows positively)
      - id: size
        type: vec3
  object_sphere_data:
    seq:
      - id: pos
        type: vec3
      - id: radius
        type: f4
  object_cone_data:
    seq:
      - id: pos
        type: vec3
      - id: radius
        type: f4
      - id: height
        type: f4
  object_text_data:
    seq:
      - id: text
        type: sstr
      - size: 28
      - id: font
        type: sstr
  object_character_data:
    seq:
      - id: character
        type: str
        size: 1
        encoding: ASCII
      - size: 0x8e
      - id: font
        type: sstr
        
      - id: enable1
        type: u1
      - id: mesh1
        type: object_character_data_mesh1
        if: enable1 != 0

      - id: enable2
        type: u1
      - id: mesh2
        type: object_character_data_mesh2
        if: enable2 != 0

  object_character_data_mesh1:
    seq:
      - id: len_unk2
        type: u4
      - id: unk2data
        type: f4
        repeat: expr
        repeat-expr: len_unk2*3
      - id: num_unk3
        type: u4
      - id: num_unk3data
        type: u4
      - id: unk3data
        type: s4
        repeat: expr
        repeat-expr: num_unk3data
        
  object_character_data_mesh2:
    seq:
      - id: num_verts
        type: u4
      - id: verts
        type: f4
        repeat: expr
        repeat-expr: num_verts*3
      - id: num_faces
        type: u4
      - id: num_face_indices
        type: u4
      - id: face_indices
        type: s4
        repeat: expr
        repeat-expr: num_face_indices
      - id: num_normals
        type: u4
      - id: normals
        type: f4
        repeat: expr
        repeat-expr: num_normals*3
      - id: someother
        type: u4
      - size: 1
      - id: num_normal_indices
        type: u4
      - id: normal_indices
        type: s4
        repeat: expr
        repeat-expr: num_normal_indices
        
      - id: num_unk5data
        type: u4
      - id: unk5data
        type: f4
        repeat: expr
        repeat-expr: num_unk5data
      - id: num_unk6
        type: u4
      - id: num_unk7data
        type: u4
      - id: unk7data
        type: s4
        repeat: expr
        repeat-expr: num_unk7data
        
  object_indexed_face_set_data:
    seq:
      - {id: unk1, type: f4}
      - {id: unk2, type: f4}
      - {id: unk3, type: f4}
      - {id: unk4, type: f4}
      - {id: unk5, type: f4}
      - {id: unk6, type: f4}
      - id: unk7
        type: u1
      - id: num_verts
        type: u4
      - id: verts
        type: f4
        repeat: expr
        repeat-expr: num_verts*3
      - id: num_faces
        type: u4
      - id: num_face_indices
        type: u4
      - id: face_indices
        type: s4
        repeat: expr
        repeat-expr: num_face_indices
      - id: num_normals
        type: u4
      - id: normals
        type: f4
        repeat: expr
        repeat-expr: num_normals*3
        
      - id: someother
        type: u4
      - size: 1
      - id: num_normal_indices
        type: u4
      - id: normal_indices
        type: s4
        repeat: expr
        repeat-expr: num_normal_indices
      - id: unk8
        size: 12
  object_triangle_set_data:
    seq:
      - id: num_verts
        type: u4
      - id: verts
        type: f4
        repeat: expr
        repeat-expr: num_verts * 3
      - id: num_faces
        type: u4
      - id: faces
        type: object_triangle_face
        repeat: expr
        repeat-expr: num_faces
      - id: num_normals
        type: u4
      - id: normals
        type: f4
        repeat: expr
        repeat-expr: num_normals*3
      - id: someother
        type: u4
  object_triangle_face:
    seq:
      - id: vert1
        type: u4
      - id: vert2
        type: u4
      - id: vert3
        type: u4
      - id: unk     # this always seems to be 7
        type: u1
  
  sstr:
    seq:
      - id: len
        type: u1
      - id: value
        type: str
        size: len
        encoding: ASCII
  vec3:
    seq:
      - id: x
        type: f4
      - id: y
        type: f4
      - id: z
        type: f4
  rgba4:
    seq:
      - id: r
        type: f4
      - id: g
        type: f4
      - id: b
        type: f4
      - id: a
        type: f4
enums:
  filetype:
    0x01: scene
    0x02: material
  gridfloor:
    0x00: xy
    0x01: xz
    0x02: yz
    
  objtype:
    0x02: cylinder
    0x04: line
    0x06: point
    0x0b: sphere
    0x0f: triangle_set
    0x10: text
    0x11: group_start
    0x12: group_finish
    0x14: spot_light
    0x15: distant_light
    0x16: point_light
    0x1c: indexed_face_set
    0x1f: cube
    0x20: cone
    0x22: torus
    0x23: character
