from ursina import *
from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume
import gltf

app = Ursina()

Entity(model='cube', color=color.red, position=(2, 0.5, 5))
Entity(model='plane', scale=40, color=color.gray, y=-0.01)

holder = Entity(position=(0, 0, 5))
actor = Actor('player_all.glb')
actor.reparent_to(holder)
print(actor.getAnimNames())   # expect ['idle', 'jogging', 'running']
actor.reparent_to(holder)
actor.setScale(100)
actor.node().setBounds(OmniBoundingVolume())
actor.node().setFinal(True)
actor.setTwoSided(True)

actor.loop('idle')
current = 'idle'

def set_anim(name):
    global current
    if name != current:
        current = name
        actor.loop(name)
    # unwrap to the Panda3D texture
def update():
    if held_keys['w']:
        print(actor.findAllTextures())
        running = held_keys['shift']
        set_anim('running' if running else 'jogging')
        holder.position += -holder.forward * time.dt * (6 if running else 3)
    elif held_keys['space']:
        set_anim('jump')
        holder.position  += holder.up * time.dt * 1
    else:
        set_anim('idle')
    holder.rotation_y += (held_keys['d'] - held_keys['a']) * 120 * time.dt

DirectionalLight(rotation=(45, -45, 0))
AmbientLight(color=color.rgba(150, 150, 150, 255))

camera.position = (0, 3, -6)
camera.look_at(holder)

app.run()