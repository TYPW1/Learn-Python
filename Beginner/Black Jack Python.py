import random

cards = [11, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]


def comp_select(computer_cards, player_cards):
    computer_cards.append(random.choice(cards))
    if sum(computer_cards) > 21:
        print("Computer Busts! You Win!")
    elif sum(computer_cards) > sum(player_cards):
        print("Computer Wins!")
    else:
        print("You Win!")


def check_win_conditions(player_cards, computer_cards):
    if sum(player_cards) > 21:
        print("You Bust! You Lose!")
    elif sum(computer_cards) > 21:
        print("Computer Busts! You Win!")
    elif sum(player_cards) == sum(computer_cards):
        print("It's a Tie!")
    elif sum(player_cards) > sum(computer_cards):
        print("You Win!")
    else:
        print("You Lose!")


play_input = input("Do you want to play blackjack? (`y` or `n`): ")

if play_input == "y":
    computer_cards = random.sample(cards, 2)
    player_cards = random.sample(cards, 2)
    print(f"Computer's first card: {computer_cards[0]}")
    print(f"Your cards: {player_cards}, current score: {sum(player_cards)}")

    move_input = input("Do you want to draw another card? (`y` or `n`): ")

    while move_input == "y":
        player_cards.append(random.choice(cards))
        print(f"Your cards: {player_cards}, current score: {sum(player_cards)}")

        if sum(player_cards) > 21:
            print("You Bust! You Lose!")
            break

        move_input = input("Do you want to draw another card? (`y` or `n`): ")

    if move_input == "n":
        print(f"Computer's final cards: {computer_cards}, current score: {sum(computer_cards)}")

        while sum(computer_cards) < 17:
            computer_cards.append(random.choice(cards))
            print(f"Computer draws a card. New hand: {computer_cards}, current score: {sum(computer_cards)}")

        check_win_conditions(player_cards, computer_cards)

elif play_input == "n":
    print("Game Ended")
else:
    print("Please enter `y` or `n`")
