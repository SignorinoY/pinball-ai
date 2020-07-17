from pinball.draw import draw_circle
from pinball.vector import Vector

import math

class Ball(object):
    
    def __init__(self, center, radius, color, score):
        self.center = center
        self.radius = radius
        self.color = color
        self.score = score

    def draw(self, screen):
        draw_circle(screen, self.color, self.center, self.radius)

    def hit(self, enemy):
        return math.sqrt((self.center.x - enemy.center.x) ** 2 + (self.center.y - enemy.center.y) ** 2) <= self.radius + enemy.radius

    def collision(self, segment):
        v1 = Vector(self.center.x - segment.p1.x, self.center.y - segment.p1.y,)
        v2 = Vector(self.center.x - segment.p2.x, self.center.y - segment.p2.y,)
        w = Vector(segment.p2.x - segment.p1.x, segment.p2.y - segment.p1.y,)
        if v1.dot(w) < 0:
            t = v1
        elif v2.dot(w) > 0:
            t = v2
        elif segment.is_left(self.center):
            t = w.left_normal_vector().project_vector(v1)
        else:
            t = w.right_normal_vector().project_vector(v1)

        return t.len() <= self.radius

    def rebound(self, segment, speed_x, speed_y):
        vector = Vector(speed_x, speed_y)
        w = Vector(segment.p2.x - segment.p1.x, segment.p2.y - segment.p1.y)
        
        w_project = w.unit().project_vector(vector)


        if segment.is_left(self.center):
            n_project = w.right_normal_vector().project_vector(vector)
        else:
            n_project = w.left_normal_vector().project_vector(vector)
        
        n_project.x *= -1
        n_project.y *= -1
        
        return w_project.x + n_project.x, w_project.y + n_project.y
