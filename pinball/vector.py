import math

class Vector(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def unit(self):
        len = self.len()
        return Vector(self.x / len, self.y / len)

    def project_vector(self, vector):
        dot = self.dot(vector)
        unit_vector = self.unit()
        return Vector(dot * unit_vector.x, dot * unit_vector.y)

    def right_normal_vector(self):
        unit_vector = self.unit()
        return Vector(-unit_vector.y, unit_vector.x)

    def left_normal_vector(self):
        unit_vector = self.unit()
        return Vector(unit_vector.y, -unit_vector.x)

    def dot(self, vector):
        return vector.x * self.x + vector.y * self.y