from particles import *
from direct.actor.Actor import Actor
from panda3d.core import OmniBoundingVolume
import gltf
class Player(Entity):
    def __init__(self, height=2, **kwargs):
        self.cursor = Entity(parent=camera.ui, model='quad', color=color.pink, scale=.008, rotation_z=45)
        super().__init__()
        self.speed = 8
        self.height = height
        self.camera_pivot = Entity(parent=self, y=self.height+0.5, z=self.z-1)
        self.z = -10
        self.x = 0
        self.y = 100
        self.color = color.white
        self.origin_y = -.5
        self.collider = 'box'
        self.actor = Actor('assets/models/player_all.glb')
        self.actor.reparent_to(self)
        print(self.actor.getAnimNames())   # expect ['idle', 'jogging', 'running']
        self.actor.reparent_to(self)
        self.actor.setScale(100)
        self.actor.node().setBounds(OmniBoundingVolume())
        self.actor.node().setFinal(True)
        self.actor.setTwoSided(True)
        self.actor.clearColor()

        self.actor.loop('idle')
        self.actor.setH(180)
        self.current_animation = 'idle'
        camera.parent = self.camera_pivot
        camera.position = Vec3.zero
        camera.rotation = Vec3.zero
        camera.fov = 125
        mouse.locked = True
        self.mouse_sensitivity = Vec2(40, 40)

        self.gravity = 0.3
        self.grounded = False
        self.jump_height = 8
        self.jump_up_duration =1.9
        self.fall_after = 0.9 # will interrupt jump up
        self.jumping = False
        self.air_time = 0
        self.hp = 100
        self.jump_anim = False      # True only between pressing jump and landing
        self.airborne_time = 0      # seconds spent off the ground
        self.traverse_target = scene     # by default, it will collide with everything. change this to change the raycasts' traverse targets.
        self.ignore_list = [self, ]


        for key, value in kwargs.items():
            setattr(self, key ,value)




    def on_window_ready(self):
        camera.rotation = Vec3.zero


    def update(self):
        self.rotation_y += mouse.velocity[0] * self.mouse_sensitivity[1]
        self.camera_pivot.rotation_x -= mouse.velocity[1] * self.mouse_sensitivity[0]
        self.camera_pivot.rotation_x= clamp(self.camera_pivot.rotation_x, -90, 90)
        self.direction = Vec3(
        self.forward * (held_keys['w'] + held_keys['up_arrow'] - held_keys['s'] - held_keys['down_arrow'])
        + self.right * (held_keys['d'] + held_keys['right_arrow'] - held_keys['a'] - held_keys['left_arrow'])
        ).normalized()

        moving = self.direction.length() > 0
        running = held_keys['shift']

        if not self.grounded:
            self.set_anim('jump', loop=False)
        elif moving:
            self.set_anim('running' if running else 'jogging')
        else:
            self.set_anim('idle')


        feet_ray = raycast(self.position+Vec3(0,0.5,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        head_ray = raycast(self.position+Vec3(0,self.height-.1,0), self.direction, traverse_target=self.traverse_target, ignore=self.ignore_list, distance=.5, debug=False)
        if not feet_ray.hit and not head_ray.hit:
            move_amount = self.direction * time.dt * self.speed

            if raycast(self.position+Vec3(-.0,1,0), Vec3(1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = min(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(-1,0,0), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[0] = max(move_amount[0], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = min(move_amount[2], 0)
            if raycast(self.position+Vec3(-.0,1,0), Vec3(0,0,-1), distance=.5, traverse_target=self.traverse_target, ignore=self.ignore_list).hit:
                move_amount[2] = max(move_amount[2], 0)
            self.position += move_amount

            # self.position += self.direction * self.speed * time.dt


        if self.gravity:
            # gravity
            ray = raycast(self.world_position+(0,self.height,0), self.down, traverse_target=self.traverse_target, ignore=self.ignore_list)

            if ray.distance <= self.height+.1:
                if not self.grounded:
                    self.land()
                self.grounded = True
                # make sure it's not a wall and that the point is not too far up
                if ray.world_normal.y > .7 and ray.world_point.y - self.world_y < .5: # walk up slope
                    self.y = ray.world_point[1]
                return
            else:
                self.grounded = False

            # if not on ground and not on way up in jump, fall
            self.y -= min(self.air_time, ray.distance-.05) * time.dt * 100
            self.air_time += time.dt * .25 * self.gravity


    def input(self, key):
        if key == 'space' :
            self.jump()


    def jump(self):
        if not self.grounded:
            return
        

        self.grounded = False
        self.jump_anim = True
        self.animate_y(self.y+self.jump_height, self.jump_up_duration, resolution=int(1//time.dt), curve=curve.out_expo)
        invoke(self.start_fall, delay=self.fall_after)

    def start_fall(self):
        self.y_animator.pause()
        self.jumping = False
    def set_anim(self, name, loop=True):
        if name != self.current_animation:
            self.current_animation = name
            if loop:
                self.actor.loop(name)
            else:
                self.actor.play(name)   # plays once, then holds the last frame

    def land(self):
        # print('land')
        self.air_time = 0
        self.grounded = True
        self.jump_anim = False
        ParticleSystem(x = self.x, z = self.z)

        
    def on_enable(self):
        mouse.locked = True
        self.cursor.enabled = True
        # restore parent and position/rotation from before disablem in case you moved the camera in the meantime.
        if hasattr(self, 'camera_pivot') and hasattr(self, '_original_camera_transform'):
            camera.parent = self.camera_pivot
            camera.transform = self._original_camera_transform


    def on_disable(self):
        mouse.locked = False
        self.cursor.enabled = False
        self._original_camera_transform = camera.transform  # store original position and rotation
        camera.world_parent = scene
        


