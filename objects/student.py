import numpy as np

class Student:
    def __init__(self, map):
        self.map = map
        self.x = np.random.rand()*map.w
        self.y = np.random.rand()*map.h
        dir = np.random.rand()*np.pi*2
        self.dx = np.cos(dir)
        self.dy = np.sin(dir)
        self.status = 0
        self.recoverTime = -1

    def update(self, speed):
        if self.recoverTime > 0:
            self.recoverTime -= 1
        elif self.recoverTime == 0:
            self.status = 2
            self.recoverTime = -1

        self.move(self.dx * speed, self.dy * speed)        
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        if self.x<0:
            self.x*=-1
            self.dx*=-1
        if self.y<0:
            self.y*=-1
            self.dy*=-1
        if self.x>self.map.w:
            self.x=-self.x+self.map.w*2
            self.dx*=-1
        if self.y>self.map.h:
            self.y=-self.y+self.map.h*2
            self.dy*=-1
    
    def GetInfection(self, time, reper):
        if self.status == 0 or (self.status == 2 and np.random.rand() < reper):
            self.status = 1
            self.recoverTime = time
            return True
            
        return False
    
