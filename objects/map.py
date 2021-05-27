import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .students import student
from . import wall

class Map:
    def __init__(self, w, h, count, incount, per=0.15):
        self.w = w
        self.h = h

        self.students = [student.Student(w, h) for _ in range(count)]
        self.infectionRaduis = 5. # 감염 거리
        self.studentSpeed = 100 # 이동 속도

        for i in range(incount): # 감염자 설정
            self.students[i].GetInfection()
        
        self.drawer = Drawer(w, h, self.students, self.update)
    
    def update(self):
        for s in self.students:
            s.update(self.studentSpeed, self.w, self.h)

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
