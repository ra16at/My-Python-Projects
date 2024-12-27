from random import randint

def guess_game():
    comuputer_num = randint(1, 100)
    your_num = int(input("Enter your number: "))
    
    while True:
        if your_num == comuputer_num:
            print("You won!")
            break
        elif your_num < comuputer_num:
            print("Your number is less than the computer number")
            your_num = int(input("Try again: "))
        elif your_num > comuputer_num:
            print("Your number is greater than the computer number")
            your_num = int(input("Try again: "))

while True:
    guess_game()
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again != 'y':
        break