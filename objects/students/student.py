import numpy as np

class Student:
    def __init__(self, w, h):
        self.x = np.random.rand()*w
        self.y = np.random.rand()*h
        dir = np.random.rand()*np.pi*2
        self.dx = np.cos(dir)
        self.dy = np.sin(dir)
        self.status = 0
        self.recoverTime = -1

    def update(self, speed, w, h):
        if self.recoverTime > 0:
            self.recoverTime -= 1
        elif self.recoverTime == 0:
            self.status = 2
            self.recoverTime = -1

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
    
    def GetInfection(self, time):
        if self.status == 0:
            self.status = 1
            self.recoverTime = time
            return True
        return False
    
