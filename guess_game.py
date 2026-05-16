import random

def play_game():
    secret_number  = random.randint(1,100)
    attempts = 0
    max_attempts = 7

    print("Welcome to the game")
    print("I have selected a random number")
    print("Try your guess")

    while True:
        print(f"{attempts+1} of {max_attempts}")

        try:
            guess = int(input("Guess: "))
        except ValueError:
            print("Please enter a whole number")
            continue

        if not (1 <= guess <=100):
            print("Please guess between 1 and 100")
            continue

        attempts += 1

        if guess == secret_number:
            print(f"Congrats! You have guessed it right. The secret number was {secret_number}")
            print(f"It took you {attempts} attempts")
            return
        elif guess < secret_number:
            print("Too low. Try higher")
        else:
            print("Too high. Try lower")

        if attempts >= max_attempts:
            print(f"Game over! The number was {secret_number}")
            return

def main():
    while True:
        play_game()
        
        again = input("Play again? (y/n): ").strip().lower()

        if (again != 'y'):
            print("Goodbye! See you again.")
            break


main()