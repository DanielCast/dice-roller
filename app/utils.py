# utils.py
# Utility functions for dice rolling with optional quantum randomness,
# history tracking, and dice notation parsing.

import secrets
import requests
from tkinter import messagebox

# API endpoint for quantum random numbers
QUANTUM_API = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"

# Supported dice types (for GUI/index-based selection)
DICE_TYPES = [4, 6, 8, 10, 12, 20]

# Global history store and current user placeholder
historyScope = []
user = ""


# -------------------------------
# Dice Rolling
# -------------------------------
def safe_quantum_roll(n: int, sides: int, timeout: float = 1.0) -> int:
    """
    Attempt to roll a die using the ANU Quantum RNG API.
    Falls back to Python's secrets module if the API fails.

    Args:
        n (int): Not used directly (kept for compatibility).
        sides (int): Number of sides on the die.
        timeout (float): Timeout for the API request in seconds.

    Returns:
        int: A random integer between 1 and `sides`.
    """
    try:
        resp = requests.get(QUANTUM_API, timeout=timeout)
        data = resp.json()
        value = data["data"][0]
        return (value % sides) + 1
    except Exception:
        # Fallback: cryptographically secure local random
        return secrets.randbelow(sides) + 1


def roll_dice(diceindex: int):
    """
    Roll a single die chosen by index from DICE_TYPES.

    Args:
        diceindex (int): Index into DICE_TYPES (e.g., 0 -> d4, 1 -> d6).

    Side effects:
        - Prints the result to console.
        - Updates global historyScope with the roll.
    """
    sides = DICE_TYPES[diceindex]
    results = []
    total = 0

    try:
        roll = safe_quantum_roll(1, sides)
    except Exception as e:
        # Fallback to secrets if quantum fails
        roll = secrets.randbelow(sides) + 1
        print(f"Quantum roll failed ({e}), fallback to secrets")

    results.append(roll)
    total += roll

    print(f"Rolled a d{sides}: {results} (Total: {total})")
    history = get_history(historyScope)
    add_to_history(history, user, f"d{sides}", results)


def roll_multiple(n: int, sides: int):
    """
    Roll multiple dice of the same type.

    Args:
        n (int): Number of dice to roll.
        sides (int): Number of sides on the dice.

    Returns:
        list[int]: List of individual roll results.

    Side effects:
        - Prints the result to console.
        - Updates global historyScope with the roll.
    """
    results = []
    total = 0

    for _ in range(n):
        try:
            roll = safe_quantum_roll(1, sides)
            results.append(roll)
            total += roll
        except Exception as e:
            messagebox.showerror("Error", str(e))

    print(f"Rolled {n}d{sides}: {results} (Total: {total})")
    history = get_history(historyScope)
    add_to_history(history, user, f"{n}d{sides}", results)
    return results


# -------------------------------
# History Management
# -------------------------------
def add_to_history(history: list, user: str, dice: str, results: list[int]):
    """
    Add a roll entry to the history.

    Args:
        history (list): The history list to append to.
        user (str): Username of the roller.
        dice (str): Dice notation (e.g., '2d6').
        results (list[int]): List of roll results.
    """
    entry = {"user": user, "dice": dice, "results": results}
    history.append(entry)


def get_history(history: list, limit: int = None):
    """
    Retrieve the most recent entries from history.

    Args:
        history (list): The history list.
        limit (int, optional): Number of most recent entries to return.

    Returns:
        list: The requested slice of history.
    """
    return history[-limit:] if limit else history


def clear_history(history: list):
    """
    Clear all entries from the history.
    """
    history.clear()


def print_history():
    """
    Print the global historyScope to console.
    """
    print(historyScope)


# -------------------------------
# Dice Notation Parsing
# -------------------------------
def parse_dice_notation(notation: str) -> tuple[int, int]:
    """
    Parse a dice notation string like '3d6' into (3, 6).

    Args:
        notation (str): Dice notation string.

    Returns:
        tuple[int, int]: Number of dice, number of sides.

    Raises:
        ValueError: If the notation is invalid.
    """
    try:
        n, sides = notation.lower().split("d")
        return int(n), int(sides)
    except Exception:
        raise ValueError("Invalid dice notation. Use format like '2d20'.")
