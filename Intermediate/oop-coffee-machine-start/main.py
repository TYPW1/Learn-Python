from menu import Menu, MenuItem
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

menu = Menu()
item = MenuItem
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

is_on = True
products = menu.get_items().split('/')

while is_on:
    u_c = input("What would you like 'latte, espresso, cappuccino': ")
    user_choice = u_c.lower()

    if user_choice == "off":
        is_on = False
    elif user_choice == "report":
        coffee_maker.report()
        money_machine.report()
    elif user_choice not in products:
        print("wrong input")
    else:
        drink = menu.find_drink(user_choice)
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
            coffee_maker.make_coffee(drink)
