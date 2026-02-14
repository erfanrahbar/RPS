import random
import os  # for clearing the terminal

# Stickers & reactions
stickers = {"rock": "🪨", "paper": "📄", "scissors": "✂️", "cat": "🐱", "computer": "🤖"}
cat_moods = ["😸 Happy Cat!", "😿 Sad Cat!", "😹 Excited Cat!", "🙀 Shocked Cat!", "😼 Sassy Cat!"]

# Game state
game_status = {"player_score": 0, "computer_score": 0, "rounds_played": 0}
shortcuts = {"r": "rock", "p": "paper", "s": "scissors"}
cheat_mode = False
beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_help():
    print("\n--- HELP ---")
    print("Type: rock/r, paper/p, scissors/s, q/exit, help\n")

def get_computer_choice(player_choice):
    if cheat_mode:
        roll = random.random()
        if roll < 0.6:  # player win
            return beats[player_choice]
        elif roll < 0.8:  # tie
            return player_choice
        else:  # computer win
            return [k for k,v in beats.items() if v == player_choice][0]
    return random.choice(["rock", "paper", "scissors"])

def determine_winner(player, computer):
    if player == computer:
        return "tie"
    return "player" if beats[player] == computer else "computer"

def play_round(player_input):
    global cheat_mode

    if player_input == "godmode":
        cheat_mode = True
        return "😈✨ GOD MODE ACTIVATED! Lucky cat energy! 🐱🔥"
    elif player_input == "nogod":
        cheat_mode = False
        return "🐱✨ God Mode deactivated. Back to normal luck!"

    if player_input in shortcuts:
        player_choice = shortcuts[player_input]
    elif player_input in ["rock", "paper", "scissors"]:
        player_choice = player_input
    else:
        return "Invalid input! Type 'help' to see options. 🙀"

    computer_choice = get_computer_choice(player_choice)
    winner = determine_winner(player_choice, computer_choice)

    # Update scores
    game_status['rounds_played'] += 1
    if winner == "player": game_status['player_score'] += 1
    elif winner == "computer": game_status['computer_score'] += 1

    # Build output
    output = []
    output.append(f"You chose {player_choice} {stickers[player_choice]}")
    output.append(f"Computer chose {computer_choice} {stickers[computer_choice]}")
    if winner == "tie": output.append("It's a tie! 😺🤖")
    elif winner == "player": output.append("You win! 🎉😸")
    else: output.append("Computer wins! 🤖💥")
    output.append(random.choice(cat_moods))
    output.append(f"\n--- Game Status ---\nRounds: {game_status['rounds_played']}, Player: {game_status['player_score']} {stickers['cat']}, Computer: {game_status['computer_score']} {stickers['computer']}\n-------------------")
    return "\n".join(output)

# Welcome
clear_screen()
print("Welcome to Cute Rock-Paper-Scissors! 🐱🎮")
show_help()

while True:
    user_input = input("Your choice: ").lower()
    if user_input in ["q", "exit"]:
        clear_screen()
        print("Thanks for playing! Bye! 😸")
        break
    elif user_input == "help":
        clear_screen()
        show_help()
        continue

    # Clear previous round output
    clear_screen()
    print(play_round(user_input))
