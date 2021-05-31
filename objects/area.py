class Area:
    def __init__(self, x=0, y=0, w=100, h=100, soild=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.isSoild = soild
    
    def GetBox(self):
        return [self.x, self.y, self.x+self.w, self.y+self.h]
    
    