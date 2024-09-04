"""# Target is the number up to which we count
def fizz_buzz(target):
    for number in range(1, target + 1):
        if number % 3 == 0 and number % 5 == 0:
            print("FizzBuzz")
        elif number % 3 == 0:
            print("Fizz")
        elif number % 5 == 0:
            print("Buzz")
        else:
            print(number)
fizz_buzz(16)"""


class User:
    def __init__(self):
        self.follower = 0
        self.following = 0

    def follow(self, user):
        user.follower += 1
        self.following += 1


user1 = User()
user2 = User()

user1.follow(user2)
print(user1.follower)
print(user1.following)
print(user2.follower)
print(user2.following)
