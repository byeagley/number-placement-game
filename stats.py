from collections import defaultdict
from pathlib import Path
import ast
import logging
import re

import pandas as pd
import plotly.express as px

from main import MAX_TURNS, SIMULATIONS

RESULTS_FILE = Path("logs/results.log")

logger = logging.getLogger(__name__)


def compute_stats(max_turns: int, simulations: int):
    log_file = Path(f"logs/game-{max_turns}.log")
    turn_count = defaultdict(int)

    with log_file.open() as f:
        for line in f:
            game_stats = ast.literal_eval(line)
            completed_turns = game_stats["completed_turns"]
            turn_count[completed_turns] += 1

    expected_turns = sum(value * key for key, value in turn_count.items()) / simulations
    win_rate = turn_count[max_turns] / simulations

    df = pd.DataFrame(
        {
            "Completed turns": turn_count.keys(),
            "Frequency": turn_count.values(),
        }
    )

    fig = px.bar(
        df,
        x="Completed turns",
        y="Frequency",
        title=f"{max_turns} turn game",
        labels={"Completed turns": "Completed turns", "Frequency": "Frequency"},
        template="plotly_dark",
    )

    logger.info(f"{max_turns=},{simulations=},{expected_turns=},{win_rate=}")
    fig.write_image(f"histograms/histogram-{max_turns}.svg")

    return


def win_rate_plot():
    x = list(range(2, MAX_TURNS))
    y = []

    with RESULTS_FILE.open() as f:
        for line in f:
            # Win rate can be in either decimal or scientific notation
            match = re.search(r"win_rate=([-+]?\d*\.?\d+([eE][-+]?\d+)?)", line)

            if match:
                y.append(float(match.group(1)))
            else:
                print("Win Rate not found.")

    fig = px.line(
        x=x,
        y=y,
        title=f"Average win rate ({SIMULATIONS} simulations)",
        template="plotly_dark",
    )
    fig.update_layout(
        xaxis_title="Max game turns",
        yaxis_title="Win rate",
        yaxis=dict(tickformat=".0%"),
    )
    fig.write_image(f"expected_win_rate-{SIMULATIONS}.svg")


def main():
    # for i in range(2, MAX_TURNS):
    #     logging.basicConfig(
    #         filename=RESULTS_FILE, level=logging.INFO, format="%(message)s", force=True
    #     )
    #     compute_stats(max_turns=i, simulations=SIMULATIONS)

    win_rate_plot()


if __name__ == "__main__":
    main()
