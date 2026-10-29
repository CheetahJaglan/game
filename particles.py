from libraries import *
class ParticleSystem(Entity):
    def __init__(self, **kwargs):
        # Duration of the particle animation (in seconds)
        self.duration = kwargs.pop('duration', 0.25)
        self.number_of_particles = kwargs.pop('particle_count', 300)
        
        # Compute initial positions and random directions for each particle.
        points = [Vec3(0, 0, 0) for _ in range(self.number_of_particles)]
        directions = [Vec3(random.uniform(-0.5, 0.5),
                           random.uniform(-0.5, 0.5),
                           random.uniform(-0.5, 0.5)) * 0.05
                      for _ in range(self.number_of_particles)]
        
        # Precompute 60 frames (roughly 1 second at 60 FPS) of particle positions.
        self.frames = []
        current_points = points.copy()
        for i in range(60):
            # Advance each particle along its direction.
            current_points = [p + d for p, d in zip(current_points, directions)]
            self.frames.append(current_points.copy())
        
        # Create a mesh using the first frame.
        super().__init__(model=Mesh(vertices=self.frames[0],
                                     mode='point',
                                     static=False,
                                     render_points_in_3d=True,
                                     thickness=40),
                         t=0,
                         duration=self.duration,
                         **kwargs)
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def update(self):
        self.t += time.dt * 4
        if self.t >= self.duration*4:
            destroy(self)
            return
        # Determine the appropriate frame based on elapsed time.
        frame_index = int(self.t * 60)
        if frame_index >= len(self.frames):
            frame_index = len(self.frames) - 1
        self.model.vertices = self.frames[frame_index]
        self.model.generate()
                                                                                