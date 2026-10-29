import bpy, sys, os

out, base, *extras = sys.argv[sys.argv.index('--') + 1:]
name_of = lambda p: os.path.splitext(os.path.basename(p))[0].lower()

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=os.path.abspath(base))
arm = next(o for o in bpy.context.scene.objects if o.type == 'ARMATURE')
ad = arm.animation_data_create()
ad.action = None

# texture, after the import so the meshes exist
img = bpy.data.images.load(os.path.abspath('player.png'))
img.pack()
mat = bpy.data.materials.new('skin')
mat.use_nodes = True
nt = mat.node_tree
bsdf = nt.nodes['Principled BSDF']
tex = nt.nodes.new('ShaderNodeTexImage')
tex.image = img
nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])

for o in bpy.context.scene.objects:
    if o.type == 'MESH':
        o.data.materials.clear()
        o.data.materials.append(mat)

for f in extras:
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=os.path.abspath(f))
    new = set(bpy.data.objects) - before
    src = next(o for o in new if o.type == 'ARMATURE')
    action = src.animation_data.action
    name = name_of(f)
    action.name = name
    track = ad.nla_tracks.new()
    track.name = name
    track.strips.new(name, int(action.frame_range[0]), action)
    for o in new:
        bpy.data.objects.remove(o, do_unlink=True)

bpy.ops.export_scene.gltf(filepath=os.path.abspath(out), export_format='GLB',
                          export_animations=True,
                          export_animation_mode='NLA_TRACKS')