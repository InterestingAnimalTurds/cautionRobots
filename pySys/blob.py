class Blob:

    def __init__(self,_x,_y,_w,_h):
        self.x = _x
        self.y = _y
        self.w = _w
        self.h = _h
        self.centerX = self.x + self.w/2
        self.centerY = self.y + self.h/2
    
    
    
    def distance_to(self, otherX, otherY):
        return ((self.centerX - otherX) ** 2 + (self.centerY - otherY) ** 2) ** 0.5

    def update(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.centerX = self.x + self.w/2
        self.centerY = self.y + self.h/2

# a frame get contorus -> contour -> near