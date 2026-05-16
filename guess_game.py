import random

def play_game():
    secret_number  = random.randint(1,100)
    attempts = 0

    print("Welcome to the game")
    print("I have selected a random number")
    print("Try your guess")

    while True:

        guess = int(input("Your guess: "))
        attempts += 1

        if guess == secret_number:
            print(f"Congrats! You have guessed it right. The secret number was {secret_number}")
            print(f"It took you {attempts} attempts")
            break
        elif guess < secret_number:
            print("Too low. Try higher")
        else:
            print("Too high. Try lower")

def main():
    play_game()
main()