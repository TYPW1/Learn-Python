class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)


def ring(self):
    return 2 * (self.width + self.height)


rect = Rectangle(10, 5)
radius = 7 * 5
print("Area:", rect.area())
print("Perimeter:", rect.perimeter())
