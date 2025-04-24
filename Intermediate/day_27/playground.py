def add(*args):
    sum = 0
    for number in args:
        sum+= number
    return sum
add(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

def calculate(**kwargs):
    sum = 0
    for number in kwargs.values():
        sum+= number
    return sum
result = calculate(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10)

class Person:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.age = kwargs.get('age')
        self.city = kwargs.get('city')
        self.country = kwargs.get('country')
        self.height = kwargs.get('height')

    def walk(self):
        print(f'{self.name} is walking')

person = Person(name='John', age=30, city='New York', country='USA')
print(person.name, person.age, person.city, person.country, person.height)