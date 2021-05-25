import numpy as np
import matplotlib.pyplot as plt

class Map:
    def __init__(self, w=1000, h=1000, count=100):
        self.w = w
        self.h = h

        self.students = [Student(w, h) for _ in range(count)]
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

    def update(self, frame):
        for s in self.students:
            s.update(5, self.w, self.h)

        self.particles.set_data([s.x for s in self.students], [s.y for s in self.students])
        
        return self.particles,


class Student:
    def __init__(self, w, h):
        self.x = np.random.rand()*w
        self.y = np.random.rand()*h
        dir = np.random.rand()*np.pi*2
        self.dx = np.cos(dir)
        self.dy = np.sin(dir)
        self.status = 0

    def update(self, speed, w, h):
        self.x += self.dx * speed
        self.y += self.dy * speed

        if self.x<0:
            self.x*=-1
            self.dx*=-1
        if self.y<0:
            self.y*=-1
            self.dy*=-1
        if self.x>w:
            self.x=-self.x+w*2
            self.dx*=-1
        if self.y>h:
            self.y=-self.y+h*2
            self.dy*=-1
    
    def GetInfection(self):
        if self.status == 0:
            self.status += 1
            return True
        return False
    
