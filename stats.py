from pathlib import Path
import ast

import pandas as pd
import plotly.express as px

from main import GAME_TURNS, MAX_GAMES

LOG_FILE = Path("main.log")


def main():
    completed_turns_count = [0] * (GAME_TURNS + 1)

    with LOG_FILE.open() as f:
        for line in f:
            game_stats = ast.literal_eval(line)
            completed_turns = game_stats["completed_turns"]
            completed_turns_count[completed_turns] += 1

    completed_turns_count.pop(0)

    sum = 0
    for index, count in enumerate(completed_turns_count):
        sum += count * (index + 1)

    expected_turns = sum / MAX_GAMES
    win_rate = completed_turns_count[-1] / MAX_GAMES

    df = pd.DataFrame(
        {
            "Completed turns": list(range(1, len(completed_turns_count) + 1)),
            "Frequency": completed_turns_count,
        }
    )

    fig = px.bar(
        df,
        x="Completed turns",
        y="Frequency",
        title="Histogram of completed turns",
        labels={"Completed turns": "Completed turns", "Frequency": "Frequency"},
        template="plotly_dark",
    )

    fig.show()
    print(f"Expected turns: {expected_turns}")
    print(f"Win rate: {win_rate}")
    fig.write_image("histogram.svg")

    return


if __name__ == "__main__":
    main()
