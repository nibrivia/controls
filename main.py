import math


class Vec:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vec(x=self.x + other.x, y=self.y + other.y, z=self.z + other.z)

    def __sub__(self, other):
        return Vec(x=self.x - other.x, y=self.y - other.y, z=self.z - other.z)

    def __truediv__(self, num):
        assert isinstance(num, float) or isinstance(num, int), "Can't divide a vector by non-float"
        return Vec(x=self.x/num, y=self.y/num, z=self.z/num)

    def __mul__(self, num):
        assert isinstance(num, float) or isinstance(num, int), "Can't multiply a vector by non-float"

        return Vec(x=num*self.x, y=num*self.y, z=num*self.z)

    def __rmul__(self, num):
        return self*num

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        return self/abs(self)

    def __str__(self):
        return f"({round(self.x, ndigits=3)}, {round(self.y, ndigits=3)}, {round(self.z, ndigits=3)})"


class Point:
    def __init__(self, mass=1, pos=Vec(0, 0, 0), vel=Vec(0, 0, 0)):
        self.mass = mass
        self.position = pos
        self.velocity = vel

    def push(self, force):
        self.velocity += 0.01*force/self.mass

    def evolve(self, t=0.01):
        self.position = self.position + (self.velocity*t)

    def __str__(self):
        return f"pt at {self.position} with mass {self.mass}, velocity {self.velocity}"


def bangbang(pt, target):
    if pt.position.x < target.x:
        pt.push(Vec(1, 0, 0))
    if pt.position.x > target.x:
        pt.push(Vec(-1, 0, 0))


def pid(pt, target, i_error):
    p = 1
    i = 0.1
    d = 1

    error = target - pt.position
    p_contribution = p * error

    d_error = target - (pt.position + pt.velocity)
    d_contribution = d * d_error

    i_error = error + 0.9*i_error
    i_contribution = i * i_error

    pt.push(p_contribution + d_contribution + i_contribution)

    return i_error


def main():
    pt = Point()
    i_error = Vec(0, 0, 0)

    for _ in range(1000):
        i_error = pid(pt, Vec(0.3, 0, 0), i_error)
        pt.evolve()
        if abs(pt.velocity) > 1:
            pt.velocity = pt.velocity.normalize()
        print(pt)

    print(f"{pt}")


if __name__ == "__main__":
    main()
    print("done")
