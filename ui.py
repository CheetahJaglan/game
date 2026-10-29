    
from setup import *

# A global list to keep track of each inventory slot.
inventory_slots = []

def add_ui():
    Entity(
        parent=camera.ui,
        model='quad',
        color=color.rgb32(200, 200, 200),
        scale=(0.04, 0.003)
    )
    Entity(
        parent=camera.ui,
        model='quad',
        color=color.rgb32(200, 200, 200),
        scale=(0.003, 0.04)
    )
