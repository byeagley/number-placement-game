"""A simple number placement game.

You are given an empty board with N slots to place numbers.
The game lasts N turns.
Each turn, a unique random number is generated within a predefined range (X <= random number < Y).
You may place the random number in any slot on the board as long as:
    1) All preceding slots contain a number less than the random number (or are empty)
    2) All following slots contain a number greater than the random number (or are empty)

You've won the game if you fill all slots, which means you placed all N numbers in ascending order.
You lose if you have no more valid slots to place the random number.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable
import logging
import math
import random

MAX_TURNS = 21
NUMBER_RANGE = (0, 1000)
SIMULATIONS = 1_000_000

logger = logging.getLogger(__name__)


@dataclass
class GameStats:
    """Store relevant game statistics.

    Parameters
    ----------
    turns: int
        the total number of turns defined before the game starts
    completed_turns: int
        the number of turns achieved in the game
    final_board: list[int | None]
        the final state of the game board
    """

    turns: int
    completed_turns: int
    final_board: list[int | None]


def user_input(
    x: int, game_board: list[int | None], number_range: tuple[int, int]
) -> int:
    print(f"Number: {x}")
    print(f"Game board: {game_board}")
    chosen_index = int(
        input(
            "Please choose the index for the new number (-1 if no available choice):\n"
        )
    )
    return chosen_index


def ideal_spacing(
    x: int, game_board: list[int | None], number_range: tuple[int, int]
) -> int:
    """A placement strategy that puts the number as close to its ideal location as possible.

    Parameters
    ----------
    x: int
        the number to place
    game_board: list[int | None]
        the current game board. 'None' represents an empty slot
    number_range: tuple[int, int]
        the minimum and maximum number possible

    Returns
    -------
    int
        the index to place the number at (-1 if no placement is possible)
    """
    max_index = len(game_board)
    previous_placement_attempts = set()
    ideal_window_size = (number_range[1] - number_range[0]) / max_index
    ideal_placement = math.floor(x / ideal_window_size)

    while 0 <= ideal_placement < max_index:
        if not game_board[ideal_placement]:
            return ideal_placement

        if ideal_placement in previous_placement_attempts:
            msg = f"Can't place {x}: no space between previous placements"
            logger.debug(msg=msg)
            return -1

        previous_placement_attempts.add(ideal_placement)
        ideal_placement += 1 if x > game_board[ideal_placement] else -1

    msg = f"Can't place {x}: no longer within bounds"
    logger.debug(msg=msg)
    return -1


def play(
    number_range: tuple[int, int],
    turns: int,
    placement_strategy: Callable[[int, list[int | None], tuple[int, int]], int],
) -> GameStats:
    """Play the number placement game.

    Parameters
    ----------
    placement_strategy: Callable[[int, list[int | None], tuple[int, int]], int]
        the placement strategy to use. it requires
            \n- the number to place
            \n- the current game board
            \n- the minimum and maximum number possible

        it returns the index to place the number at (or -1 if no placement is possible)

    Returns
    -------
    GameStats
        the final stats for the game
    """
    generated_numbers = set()
    game_board: list[int | None] = [None] * turns

    for turn in range(turns):
        random_number = random.randint(number_range[0], number_range[1] - 1)

        # Ensure the randomly generated number is unique
        while random_number in generated_numbers:
            random_number = random.randint(*number_range)

        generated_numbers.add(random_number)
        placement_index = placement_strategy(random_number, game_board, number_range)

        if not 0 <= placement_index < turns:
            return GameStats(turns=turns, completed_turns=turn, final_board=game_board)

        game_board[placement_index] = random_number

    return GameStats(turns=turns, completed_turns=turn + 1, final_board=game_board)


def main():
    for i in range(2, MAX_TURNS):
        logging.basicConfig(
            filename=Path(f"game-{i}.log"),
            level=logging.INFO,
            format="%(message)s",
            filemode="w",
            force=True,
        )

        for game in range(SIMULATIONS):
            logger.debug(f"Starting game #{game}")
            game_stats = play(
                turns=i, number_range=NUMBER_RANGE, placement_strategy=ideal_spacing
            )
            logger.info(asdict(game_stats))


if __name__ == "__main__":
    main()
