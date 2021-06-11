import numpy as np

class Person:
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
    
    def MoveToPos(self, speed, x, y):
        dis = np.sqrt((x-self.x)*(x-self.x)+(y-self.y)*(y-self.y))

        if dis<speed:
            self.x = x
            self.y = y

            return True
        else:
            dir = np.arctan2(y-self.y, x-self.x)
            self.dx = np.cos(dir)
            self.dy = np.sin(dir)
            self.move(self.dx * speed, self.dy * speed)

            return False
    
    def GetInfection(self, time, reper):
        if self.status == 0 or (self.status == 2 and np.random.rand() < reper):
            self.status = 1
            self.recoverTime = time
            return True
            
        return False

class Student(Person):
    def __init__(self, map, number):
        super().__init__(map)
        self.number = number
        self.type = 0 # 1: 무리 짓기 2:
        self.fx = 0
        self.fy = 0
    
    def update(self, speed):
        super().update(0)

        self.MoveToPos(speed, self.fx, self.fy)

class Eater(Person):
    def __init__(self, map):
        super().__init__(map)

        self.targetw = None

        self.waiting = None
        self.isWait = True

        self.isFinish = False

    def update(self, speed):
        super().update(0)
        
        if self.waiting:
            if self.status == 2:
                print(self.waiting)
            self.isWait = self.MoveToPos(speed, self.waiting.x, self.waiting.y)
            if self.isWait and self.waiting == self.map.exit:
                self.waiting.person = None
                self.targetw = None
                self.waiting = None
                # todo : logging
                self.status = 2
                return
            if self.isWait and not self.waiting.next.person:
                if self.targetw != self.waiting and not self.waiting.force:
                    self.waiting.next.SetPerson(self)
                    self.waiting.person = None
                    self.waiting = self.waiting.next
                    self.isWait = False
                elif self.waiting.Check():
                    self.isWait = True
                    if self.targetw != self.waiting:
                        self.waiting.next.SetPerson(self)
                        self.waiting.person = None
                        self.waiting = self.waiting.next
                        self.isWait = False
                    else:
                        self.waiting.isTarget = False
                        if self.waiting.time == 300:
                            self.isFinish = True
                            self.waiting.next.SetPerson(self)
                            self.waiting.person = None
                            self.waiting = self.waiting.next
                            self.isWait = False
                else:
                    self.isWait = True
        else:
            self.isWait = True

class Waiting:
    def __init__(self, x, y, time=0, force=False):
        self.x = x
        self.y = y
        self.time = time
        self.current = 0
        self.person = None

        self.isTarget = False

        self.force = force

        self.next = None
    
    def SetNext(self, next):
        self.next = next

    def SetPerson(self, person):
        self.person = person
        self.current = 0

    def Check(self):
        if not self.person:
            return None
        if not self.person.isWait:
            return None

        if self.current < self.time:
            self.current += 1
            return None
        else:
            return self.next