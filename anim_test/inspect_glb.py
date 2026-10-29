import json, struct, os, time

path = 'player_all.glb'
print('modified:', time.ctime(os.path.getmtime(path)))

with open(path, 'rb') as f:
    f.read(12)                                   # GLB header
    length, _ = struct.unpack('<II', f.read(8))  # first chunk = JSON
    j = json.loads(f.read(length))

print('images:', j.get('images'))
print('textures:', j.get('textures'))
print('materials:', [(m.get('name'), m.get('pbrMetallicRoughness')) for m in j.get('materials', [])])
for m in j['meshes']:
    for p in m['primitives']:
        print('mesh', m.get('name'), 'attributes:', list(p['attributes']), 'material:', p.get('material'))
print('animations:', [a.get('name') for a in j.get('animations', [])])