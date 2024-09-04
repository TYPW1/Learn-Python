from replit import clear
from art import *

# HINT: You can call clear() to clear the output in the console.
print(logo)

repeat = True
bidders = []
while repeat != False:
    name = input("What is your name: ")
    bid = input("What is your bid: ")

    bidders.append({name: bid})

    select = input("Are they any other bidders? ")

    if select == "yes":
        repeat = True
    else:
        repeat = False

    clear()

track_bid = 0
track_name = ""
for bidder in bidders:
    for name, bid in bidder.items():
        if int(bid) > int(track_bid):
            track_bid = bid
            track_name = name

print(f"The highest bidder is {track_name} with a bid of {track_bid}")
print(bidders)