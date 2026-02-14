import random
import os
import re

# ================================
# Colors for terminal output
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
# Regex to handle ANSI codes (for pretty print)
# ================================
ANSI_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

def visible_length(text: str) -> int:
    """Calculate length of the string ignoring any ANSI color codes."""
    return len(ANSI_PATTERN.sub('', text))


# ================================
# Game constants and settings
# ================================
CHOICES = ("rock", "paper", "scissors")

# Quick lookup for shorthand commands
SHORTCUTS = {
    "r": "rock",
    "p": "paper",
    "s": "scissors"
}

# Who beats whom in the game
BEATS = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

# Reverse lookup for efficient counter choices (avoiding list search)
LOSES_TO = {v: k for k, v in BEATS.items()}

# ================================
# Game state
# ================================
game_status = {
    "player_score": 0,
    "computer_score": 0,
    "rounds_played": 0
}

# This flag tracks if cheat mode is on or off
cheat_mode = False


# ================================
# Utility Functions
# ================================
def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def play_sound() -> None:
    """Play a simple beep sound to signal results."""
    print("\a", end="")


# ================================
# UI Helpers
# ================================
def draw_box(text: str, color: str = RESET) -> None:
    """Draw a nice bordered box around the provided text."""
    lines = text.split("\n")
    width = max(visible_length(line) for line in lines)

    horizontal = "─" * (width + 2)

    print(color + f"┌{horizontal}┐" + RESET)
    for line in lines:
        padding = width - visible_length(line)
        print(color + "│ " + RESET + line + " " * padding + color + " │" + RESET)
    print(color + f"└{horizontal}┘" + RESET)


def show_help() -> None:
    """Display the help instructions to the user."""
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
# Game Logic Functions
# ================================
def get_computer_choice(player_choice: str) -> str:
    """
    Determines the computer's choice. If cheat mode is active, 
    it can be biased toward the player.
    """
    if cheat_mode:
        roll = random.random()
        if roll < 0.6:
            return BEATS[player_choice]       # player wins
        elif roll < 0.8:
            return player_choice              # tie
        else:
            return LOSES_TO[player_choice]    # computer wins

    return random.choice(CHOICES)


def determine_winner(player: str, computer: str) -> str:
    """Decide who wins the round."""
    if player == computer:
        return "tie"
    return "player" if BEATS[player] == computer else "computer"


def normalize_input(user_input: str) -> str | None:
    """Normalize user input into a valid game choice (e.g., 'rock')."""
    if user_input in SHORTCUTS:
        return SHORTCUTS[user_input]
    if user_input in CHOICES:
        return user_input
    return None


def update_scores(winner: str) -> None:
    """Update the game scores based on who won."""
    game_status["rounds_played"] += 1

    if winner == "player":
        game_status["player_score"] += 1
    elif winner == "computer":
        game_status["computer_score"] += 1


def build_status_block() -> str:
    """Create a string showing the current status of the game."""
    return (
        f"\n{BOLD}Game Status{RESET}\n"
        f"Rounds played: {game_status['rounds_played']}\n"
        f"Your score: {game_status['player_score']}\n"
        f"Computer score: {game_status['computer_score']}"
    )


def play_round(player_input: str) -> str:
    global cheat_mode

    # ===== Handle cheat mode (hidden from normal gameplay) =====
    if player_input == "godmode":
        cheat_mode = True
        play_sound()
        return f"{MAGENTA}{BOLD}God Mode activated 😈 — luck is on your side!{RESET}"

    if player_input == "nogod":
        cheat_mode = False
        return f"{YELLOW}Back to normal mode. Fair game now 🙂{RESET}"

    # ===== Handle player input =====
    player_choice = normalize_input(player_input)
    if not player_choice:
        return f"{RED}Oops! That doesn't look like a valid choice. Type 'help' for guidance.{RESET}"

    # ===== Determine the computer's choice =====
    computer_choice = get_computer_choice(player_choice)
    winner = determine_winner(player_choice, computer_choice)

    # ===== Update scores =====
    update_scores(winner)

    # ===== Display result message =====
    if winner == "player":
        play_sound()
        result_msg = f"{GREEN}{BOLD}Nice! You won this round 🎉{RESET}"
    elif winner == "computer":
        play_sound()
        result_msg = f"{RED}{BOLD}Oops! Computer wins this time 🤖{RESET}"
    else:
        result_msg = f"{YELLOW}It's a tie — both chose wisely! 🙂{RESET}"

    # ===== Return round summary =====
    return (
        f"{CYAN}You chose:{RESET} {player_choice}\n"
        f"{CYAN}Computer chose:{RESET} {computer_choice}\n\n"
        f"{result_msg}"
        f"{build_status_block()}"
    )


# ================================
# Game Loop
# ================================
def main() -> None:
    clear_screen()

    # Welcome message
    draw_box(
        f"{BOLD}{CYAN}Welcome to Rock–Paper–Scissors! 🎮\n"
        f"Simple. Fast. Fun!{RESET}",
        MAGENTA
    )

    # Show help on startup
    show_help()

    while True:
        # Get user input
        user_input = input(f"\n{BOLD}Your move → {RESET}").strip().lower()

        if user_input in ("q", "exit"):
            # Exit the game
            clear_screen()
            draw_box(
                f"{GREEN}Thanks for playing — see you next time! 👋{RESET}",
                GREEN
            )
            break

        if user_input == "help":
            # Show help
            clear_screen()
            show_help()
            continue

        # Play a round of the game
        clear_screen()
        draw_box(play_round(user_input), CYAN)


if __name__ == "__main__":
    main()
