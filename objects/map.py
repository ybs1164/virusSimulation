import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from . import student
from . import area
from pyqtree import Index

class Map:
    def __init__(self, w, h, 
                 count=100,
                 incount=0,
                 recount=0,
                 per=0.15,
                 reper=0,
                 radius=3,
                 retime=-1,
                 speed=0.5,
                 distanceRadius=0):
        self.w = w
        self.h = h

        self.students = [student.Student(self) for _ in range(count)]
        
        self.areas = []

        self.infectionRadius = radius # 감염 거리 - 주의, 이동 속도의 두 배 이상이어야 함
        self.infectionPercent = per # 감염 확률
        self.reinfectionPercent = reper # 재감염 확률
        self.recoverTime = retime # 치유 시간
        self.studentSpeed = speed # 이동 속도
        self.distanceRadius = distanceRadius # 거리두기 거리

        # result values
        self.susceptibleCount = count - incount - recount
        self.infectiousCount = incount
        self.recoveredCount = recount

        self.result = [(self.susceptibleCount, self.infectiousCount, self.recoveredCount)]

        for i in range(incount + recount): # 감염자 & 완치자 설정
            if i >= count:
                break
            if i >= incount:
                self.students[i].status = 2
            else:
                self.students[i].GetInfection(self.recoverTime, 0)
        
        self.logger = Logger(self.result, count)
        self.drawer = Drawer(w, h, self.students, self.update)

        plt.show()
    
    def update(self):
        qt = Index(bbox=(0, 0, self.w, self.h), max_items=5)

        for i in range(len(self.students)):
            s = self.students[i]
            qt.insert(i, (s.x, s.y, s.x, s.y))
            s.update(self.studentSpeed)

        for s in self.students:
            if self.distanceRadius > 0: # 사회적 거리두기
                distance = self.distanceRadius

                for i in qt.intersect((s.x-distance, s.y-distance, s.x+distance, s.y+distance)):
                    other = self.students[i]
                    if np.sqrt((s.x-other.x)*(s.x-other.x)+(s.y-other.y)*(s.y-other.y))>distance:
                        continue
                        
                    if s != self.students[i]:
                        direct = np.arctan2(s.y-self.students[i].y, s.x-self.students[i].x)
                        s.dx += np.cos(direct) * 2
                        s.dy += np.sin(direct) * 2

                mag = np.sqrt(s.dx*s.dx+s.dy*s.dy)
                s.dx /= mag
                s.dy /= mag

            for i in qt.intersect((s.x-self.infectionRadius, s.y-self.infectionRadius, s.x+self.infectionRadius, s.y+self.infectionRadius)):
                other = self.students[i]
                if np.sqrt((s.x-other.x)*(s.x-other.x)+(s.y-other.y)*(s.y-other.y))>self.infectionRadius:
                    continue

                if s.status == 1 and np.random.rand() < self.infectionPercent:
                    self.students[i].GetInfection(self.recoverTime, self.reinfectionPercent)
        
        self.setLogData()
    
    def setLogData(self):
        self.susceptibleCount = 0
        self.infectiousCount = 0
        self.recoveredCount = 0

        for s in self.students:
            if s.status == 0:
                self.susceptibleCount += 1
            elif s.status == 1:
                self.infectiousCount += 1
            elif s.status == 2:
                self.recoveredCount += 1
        
        self.result.append((self.susceptibleCount, self.infectiousCount, self.recoveredCount))

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

        ax.set_aspect('equal')

        self.play = True

        self.fig.canvas.mpl_connect('button_press_event', self.pause)

        self.anime = FuncAnimation(fig, self.update, fargs=(students, updateStudent, ), interval=1000/60, blit=True)

    # 프레임
    def update(self, frame, students, studentsMethod):
        studentsMethod()

        self.susceptible.set_data([s.x for s in students if s.status == 0], [s.y for s in students if s.status == 0])
        self.infectious.set_data([s.x for s in students if s.status == 1], [s.y for s in students if s.status == 1])
        self.recovered.set_data([s.x for s in students if s.status == 2], [s.y for s in students if s.status == 2])

        return self.susceptible, self.infectious, self.recovered,

    def pause(self, event):
        if not event.dblclick:
            return
        if self.play:
            self.anime.event_source.stop()
            self.play = False
        else:
            self.anime.event_source.start()
            self.play = True

class Logger:
    def __init__(self, value, count):
        self.value = value

        fig, ax = plt.subplots()
        
        self.fig = fig
        self.ax = ax
        
        self.sgraph, = plt.plot([], [], 'b', ms=6) # 일반인
        self.igraph, = plt.plot([], [], 'r', ms=6) # 감염자
        self.rgraph, = plt.plot([], [], 'g', ms=6) # 완치자

        ax.axes.xaxis.set_visible(False)

         # 맵 크기 설정
        ax.set_ylim(0, count)

        self.play = True

        self.anime = FuncAnimation(fig, self.update, interval=1000/60, blit=True)
    
    def update(self, frame):
        self.ax.set_xlim(0, max(len(self.value), 200))

        self.igraph.set_data(range(len(self.value)), [v[1] for v in self.value])
        self.sgraph.set_data(range(len(self.value)), [v[1]+v[0] for v in self.value])

        return self.sgraph, self.igraph, self.rgraph,  