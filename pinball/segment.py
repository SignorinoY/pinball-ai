from pinball.draw import draw_line

class Segment(object):
    
    def __init__(self, p1, p2, color=(255, 255, 255)):
        self.p1 = p1
        self.p2 = p2
        self.color = color

    def draw(self, screen):
        draw_line(screen, self.p1, self.p2, self.color)

    def is_left(self, point):
        return (self.p2.x - self.p1.x) * (point.y - self.p1.y) - (self.p2.y - self.p1.y) * (point.x - self.p1.x) < 0
