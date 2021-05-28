import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .students import student
from . import wall
from pyqtree import Index

class Map:
    def __init__(self, w, h, count=1, incount=1, recount=0, per=0.15, radius=3, retime=60, speed=1):
        self.w = w
        self.h = h

        self.students = [student.Student(w, h) for _ in range(count)]
        self.infectionRadius = radius # 감염 거리 - 주의, 이동 속도의 두 배 이상이어야 함
        self.infectionPercent = per
        self.recoverTime = retime
        self.studentSpeed = speed # 이동 속도

        for i in range(incount + recount): # 감염자 설정
            if i > count:
                break
            if i > incount:
                self.students[i].status = 2
            else:
                self.students[i].GetInfection(self.recoverTime)
        
        self.drawer = Drawer(w, h, self.students, self.update)
    
    def update(self):
        qt = Index(bbox=(0, 0, self.w, self.h), max_items=5)

        for i in range(len(self.students)):
            s = self.students[i]
            qt.insert(i, (s.x, s.y, s.x, s.y))
            s.update(self.studentSpeed, self.w, self.h)

        for s in self.students:
            if s.status == 1:
                for i in qt.intersect((s.x-self.infectionRadius, s.y-self.infectionRadius, s.x+self.infectionRadius, s.y+self.infectionRadius)):
                    if self.students[i].status == 0 and np.random.rand() < self.infectionPercent:
                        self.students[i].GetInfection(self.recoverTime)

class Drawer:
    def __init__(self, w, h, students, updateStudent):
        fig, ax = plt.subplots()
        self.fig = fig
        
        self.susceptible, = plt.plot([], [], 'bo', ms=6) # 일반인
        self.infectious, = plt.plot([], [], 'ro', ms=6) # 감염자
        self.recovered, = plt.plot([], [], 'go', ms=6) # 완치자

        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(False)

        ax.set_xlim(0, w) # 맵 크기 설정
        ax.set_ylim(0, h)

        def update(frame, students):
            updateStudent()
            return self.update(students)

        anime = FuncAnimation(fig, update, fargs=(students, ), interval=60, blit=True)
        plt.show()

    # 초기화 작업
    def init(self):
        self.susceptible.set_data([], [])
        self.infectious.set_data([], [])
        self.recovered.set_data([], [])
        
        return self.susceptible, self.infectious, self.recovered,

    # 프레임
    def update(self, students):
        self.susceptible.set_data([s.x for s in students if s.status == 0], [s.y for s in students if s.status == 0])
        self.infectious.set_data([s.x for s in students if s.status == 1], [s.y for s in students if s.status == 1])
        self.recovered.set_data([s.x for s in students if s.status == 2], [s.y for s in students if s.status == 2])

        return self.susceptible, self.infectious, self.recovered,
