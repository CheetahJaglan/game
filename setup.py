from player import *

app = Ursina()




Entity.default_shader = lit_with_shadows_shader

ground = Entity(model='plane', collider='box', scale=256, texture='grass', texture_scale=(4,4))
player = Player()
editor_camera = EditorCamera(enabled=False, ignore_paused=True)



shootables_parent = Entity()
mouse.traverse_target = shootables_parent

def makemap():
    hole_half = 16
    half = 64

    for x in range(-half, half):
        for z in range(-half, half):

        # Skip the middle 64x64 area
            if -hole_half <= x < hole_half and -hole_half <= z < hole_half:
                continue

            if random.random() < 0.02:  # 5% chance to spawn a block

                Entity(
                model='cube',
                origin_y=-.5,
                scale=2,
                texture='brick',
                texture_scale=(1,2),
                x=x * 2,     # spacing (match scale=2)
                z=z * 2,
                collider='box',
                scale_y=random.uniform(2, 3),
                color=color.hsv(0, 0, random.uniform(.9, 1))
                )



class Enemy(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=shootables_parent, model=load_model('assets/models/enemy.obj') ,scale=(1), origin_y=-0.05, color=color.light_gray, collider='box',texture='assets/models/enemy.png', **kwargs)
        self.health_bar = Entity(parent=self, y=3.25, model='cube', color=color.red, world_scale=(1.5,.1,.1))
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):

        dist = distance_xz(player.position, self.position)
        if dist > 80:
            return

        self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


        self.look_at_2d(player.position, 'y')
        hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
        # print(hit_info.entity)
        if hit_info.entity == player:
            if dist > 2:
                self.position += self.forward * time.dt * 5

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        global wave , score
        self._hp = value
        if value <= 0:
            ParticleSystem(world_position=self.world_position+Vec3(0,1,0), color=color.blue)
            destroy(self)
            score += 5


            return

        self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
        self.health_bar.alpha = 1



