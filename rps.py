import random
import os
import re

# ================================
# Terminal colors (ANSI)
# ================================
RESET = "\033[0m"
BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

# ================================
# ANSI handling (FIXED BOX WIDTH)
# ================================
ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

def visible_length(text):
    """Return printable length (without ANSI codes)."""
    return len(ANSI_PATTERN.sub('', text))


# ================================
# Game state
# ================================
game_status = {"player_score": 0, "computer_score": 0, "rounds_played": 0}
shortcuts = {"r": "rock", "p": "paper", "s": "scissors"}
cheat_mode = False
beats = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


# ================================
# System utilities
# ================================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def play_sound():
    """Simple system beep"""
    print("\a", end="")


# ================================
# UI helpers
# ================================
def draw_box(text, color=RESET):
    lines = text.split("\n")
    width = max(visible_length(line) for line in lines)

    print(color + "┌" + "─" * (width + 2) + "┐" + RESET)
    for line in lines:
        padding = width - visible_length(line)
        print(
            color + "│ " + RESET +
            line +
            " " * padding +
            color + " │" + RESET
        )
    print(color + "└" + "─" * (width + 2) + "┘" + RESET)


def show_help():
    help_text = (
        f"{BOLD}{CYAN}HOW TO PLAY{RESET}\n\n"
        "• Type rock or r\n"
        "• Type paper or p\n"
        "• Type scissors or s\n"
        "• Type help to see this menu\n"
        "• Type q or exit to quit\n"
    )
    draw_box(help_text, BLUE)


# ================================
# Game logic
# ================================
def get_computer_choice(player_choice):
    if cheat_mode:
        roll = random.random()
        if roll < 0.6:
            return beats[player_choice]  # player wins
        elif roll < 0.8:
            return player_choice  # tie
        else:
            return [k for k, v in beats.items() if v == player_choice][0]
    return random.choice(["rock", "paper", "scissors"])


def determine_winner(player, computer):
    if player == computer:
        return "tie"
    return "player" if beats[player] == computer else "computer"


def play_round(player_input):
    global cheat_mode

    # ===== cheat mode =====
    if player_input == "godmode":
        cheat_mode = True
        play_sound()
        return f"{MAGENTA}{BOLD}God Mode activated 😈 — luck is on your side!{RESET}"

    if player_input == "nogod":
        cheat_mode = False
        return f"{YELLOW}Back to normal mode. Fair game now 🙂{RESET}"

    # ===== input handling =====
    if player_input in shortcuts:
        player_choice = shortcuts[player_input]
    elif player_input in ["rock", "paper", "scissors"]:
        player_choice = player_input
    else:
        return f"{RED}Hmm… that doesn't look right. Type 'help'.{RESET}"

    computer_choice = get_computer_choice(player_choice)
    winner = determine_winner(player_choice, computer_choice)

    # ===== update scores =====
    game_status["rounds_played"] += 1
    if winner == "player":
        game_status["player_score"] += 1
    elif winner == "computer":
        game_status["computer_score"] += 1

    # ===== result message =====
    if winner == "player":
        play_sound()
        result_msg = f"{GREEN}{BOLD}Nice! You win this round 🎉{RESET}"
    elif winner == "computer":
        play_sound()
        result_msg = f"{RED}{BOLD}Computer wins this time 🤖{RESET}"
    else:
        result_msg = f"{YELLOW}It's a tie — great minds think alike 🙂{RESET}"

    # ===== output =====
    output = (
        f"{CYAN}You chose:{RESET} {player_choice}\n"
        f"{CYAN}Computer chose:{RESET} {computer_choice}\n\n"
        f"{result_msg}\n"
        f"\n{BOLD}Game Status{RESET}\n"
        f"Rounds played: {game_status['rounds_played']}\n"
        f"Your score: {game_status['player_score']}\n"
        f"Computer score: {game_status['computer_score']}"
    )

    return output


# ================================
# Start game
# ================================
clear_screen()

draw_box(
    f"{BOLD}{CYAN}Welcome to Rock–Paper–Scissors! 🎮\n"
    f"Simple. Fast. A little bit fun 🙂{RESET}",
    MAGENTA
)

show_help()

while True:
    user_input = input(f"\n{BOLD}Your move → {RESET}").lower()

    if user_input in ["q", "exit"]:
        clear_screen()
        draw_box(f"{GREEN}Thanks for playing — see you again! 👋{RESET}", GREEN)
        break

    if user_input == "help":
        clear_screen()
        show_help()
        continue

    clear_screen()
    draw_box(play_round(user_input), CYAN)
