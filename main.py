
from ui import *
from commands import *
from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume
import gltf


def update():
    if held_keys['left mouse']:
        #pass
        pass
    if held_keys['space']:
            # self.gravity = 0
            pass
    
    

    
def respawncheck():
    if player.position.y < -50:
        player.position = Vec3(0,350,-10)
    invoke(respawncheck, delay=10)

respawncheck() # start the loop

# ------------------------------
# Command Mode
# ------------------------------
# Variables for command mode.
command_string = ""
command_mode = False
command_field = None


def on_command_submit(text):
    global command_string, command_mode, command_field
    command_string = text
    print("Command entered:", command_string)
    run_command(command_string)

    command_field.disable()
    command_field = None
    command_mode = False
    application.paused = False
    mouse.locked = True


def cancel_command_mode():
    global command_mode, command_field
    if command_field:
        command_field.disable()
        command_field = None
    command_mode = False
    application.paused = False
    mouse.locked = True


def pause_input(key):
    global command_mode, command_field
    if key == 'tab':
    #     if not command_mode:
    #         command_mode = True
    #         application.paused = True
    #         mouse.locked = not application.paused
    #         command_field = InputField(default_value='', position=(-0.3, 0.4), scale=(0.6, 0.1), ignore_paused=True)
    #         command_field.active = True
    #     else:
    #         cancel_command_mode()
    #         mouse.locked = True

    # if command_mode and key == 'enter' and command_field:
    #     on_command_submit(command_field.text)
        editor_camera.enabled = not editor_camera.enabled
        player.cursor.enabled = not editor_camera.enabled
        mouse.locked = not editor_camera.enabled
        editor_camera.position = player.position 



pause_handler = Entity(ignore_paused=True, input=pause_input)

def input(key):

    global player
    # Cycle items
    pass



sun = DirectionalLight()
sun.look_at(Vec3(1,-1,-1))
Sky()

add_ui()

app.run()

