
class Rectangle():

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.v1 = b / 2**.5
        self.v2 = (a/2) * 2 ** .5
        self.count = 0
        self.rng = max(a, b)

    def rectangle_rotation(self):
        for x in range(-self.rng, self.rng):
            top = min(self.fa1(x), self.fb1(x))
            bottom = max(self.fa2(x), self.fb2(x))

            if bottom > top:
                continue

            self.count += abs(int(bottom) - int(top))

            if bottom <= 0 and top >= 0:
                self.count += 1

        return self.count

    def fa1(self, x):
        return x + self.v1

    def fa2(self, x):
        return x - self.v1

    def fb1(self, x):
        return -x + self.v2

    def fb2(self, x):
        return -x - self.v2


def rectangle_rotation(a, b):
    r = Rectangle(a, b)
    return r.rectangle_rotation()


print(rectangle_rotation(34324, 443533))
