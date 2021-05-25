import numpy as np
import matplotlib.pyplot as plt

class Map:
    def __init__(self, w=500, h=500, count=100):
        self.students = [Student() for _ in range(count)]
        self.infectionRaduis = 5.
        self.studentSpeed = .2

        fig, ax = plt.subplots()
        self.fig = fig
        
        self.particles, = plt.plot([], [], 'bo', ms=6)

        ax.set_xlim(0, w)
        ax.set_ylim(0, h)
    
    def GetFigure(self):
        return self.fig
    
    def init(self):
        self.particles.set_data([], [])
        
        return self.particles,

    def update(self):
        for s in self.students:
            s.update()

        self.particles.set_data([s.x for s in self.students], [s.y for s in self.students])
        
        return self.particles,


class Student:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.dir = 0
        self.status = 0

    def update(self, speed):
        self.x += speed * np.cos(self.dir)
        self.y += speed * np.sin(self.dir)
    
    def GetInfection(self):
        if self.status == 0:
            self.status += 1
            return True
        return False
    
