import random

def play_game():
    choices = ['rock', 'paper', 'scissors']
    user_score = 0
    computer_score = 0

    print("=======================================")
    print("   Welcome to Rock-Paper-Scissors!   ")
    print("=======================================")
    print("Instructions:")
    print("- Type 'rock', 'paper', or 'scissors' to make your move.")
    print("- Type 'quit' anytime to end the game.\n")

    while True:
        user_choice = input("Your choice: ").strip().lower()

        if user_choice == 'quit':
            print("\n=======================================")
            print("             Final Score               ")
            print(f"        You: {user_score} | Computer: {computer_score}        ")
            print("         Thanks for playing!           ")
            print("=======================================\n")
            break

        if user_choice not in choices:
            print("Invalid input. Please choose rock, paper, or scissors.\n")
            continue

        computer_choice = random.choice(choices)
        
        print(f"\n=> You chose: {user_choice}")
        print(f"=> Computer chose: {computer_choice}")

        if user_choice == computer_choice:
            print("\n   Result: It's a tie! 🤝")
        elif (user_choice == 'rock' and computer_choice == 'scissors') or \
             (user_choice == 'scissors' and computer_choice == 'paper') or \
             (user_choice == 'paper' and computer_choice == 'rock'):
            print("\n   Result: You win! 🎉")
            user_score += 1
        else:
            print("\n   Result: You lose! 😢")
            computer_score += 1
            
        print(f"\n--- Score --- You: {user_score} | Computer: {computer_score} ---\n")
        
        play_again = input("Do you want to play another round? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("\n=======================================")
            print("             Final Score               ")
            print(f"        You: {user_score} | Computer: {computer_score}        ")
            print("         Thanks for playing!           ")
            print("=======================================\n")
            break
        print("-" * 39 + "\n")

if __name__ == "__main__":
    play_game()
