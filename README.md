# Number placement game

## Background

![Game screenshot](assets/number-placement-screenshot.png)

This project implements a simulation of the game played by instagram account [@breadbasket303](https://www.instagram.com/breadbasket303) (seen above).

You are given an empty board with 20 slots to place numbers.

Each turn, a unique random number (N) is generated between 0 and 1,000.

You may place N in any slot on the board as long as:

1. All preceding slots contain a number less than N (or are empty)
2. All subsequent slots contain a number greater than N (or are empty)

You've won the game if you fill all slots, which means you placed all 20 numbers in ascending order.
You lose if you have no more valid slots to place N.

## Methodology

### Placement strategy

**breadbasket** relies primarily on what I'd call the _ideal window strategy_. Since the board contains 20 slots and all numbers are between 0 and 1,000, each slot can be assigned a range of 50 numbers: slot 1 for numbers 0-49, slot 2 for numbers 50-99, etc.

You first attempt to place the current number in it's preferred location. For example, if you had the number 541, you'd try to place it in slot 11. If there is already a number there and your number is smaller, try the previous slot. If yours is larger, try the next slot. Repeat until you've found a slot for your number. If there is no longer space for it, you've lost.

I've translated this strategy into a program and run it for 1,000,000 simulations. I went ahead and simulated games with different slot counts as well for comparison.

### Assumptions

I've assumed a uniform distribution -- every number between 0 and 1,000 is equally likely in my simulation. It's unclear whether the real game uses a uniform distribution as well.

## Results

### Simulation statistics

| Game size | Win rate (%) | Average completed turns |
| --------: | ------------ | ----------------------- |
|        20 | 0.0065       | 9.25                    |
|        19 | 0.0118       | 8.92                    |
|        18 | 0.0217       | 8.60                    |
|        17 | 0.0384       | 8.27                    |
|        16 | 0.0640       | 7.93                    |
|        15 | 0.1096       | 7.58                    |
|        14 | 0.1845       | 7.23                    |
|        13 | 0.3135       | 6.87                    |
|        12 | 0.5423       | 6.50                    |
|        11 | 0.9136       | 6.12                    |
|        10 | 1.5809       | 5.73                    |
|         9 | 2.6361       | 5.32                    |
|         8 | 4.4297       | 4.90                    |
|         7 | 7.4505       | 4.46                    |
|         6 | 12.291       | 3.99                    |
|         5 | 20.1889      | 3.50                    |
|         4 | 32.5284      | 2.97                    |
|         3 | 50.7069      | 2.40                    |
|         2 | 75.0349      | 1.75                    |

### Expected win rate plot

![Expected win rate](assets/expected_win_rate-1000000.svg)

### Turn histograms

<details>
<summary>Histograms</summary>

![20 turn game](assets/histograms/histogram-20.svg)
![19 turn game](assets/histograms/histogram-19.svg)
![18 turn game](assets/histograms/histogram-18.svg)
![17 turn game](assets/histograms/histogram-17.svg)
![16 turn game](assets/histograms/histogram-16.svg)
![15 turn game](assets/histograms/histogram-15.svg)
![14 turn game](assets/histograms/histogram-14.svg)
![13 turn game](assets/histograms/histogram-13.svg)
![12 turn game](assets/histograms/histogram-12.svg)
![11 turn game](assets/histograms/histogram-11.svg)
![10 turn game](assets/histograms/histogram-10.svg)
![9 turn game](assets/histograms/histogram-9.svg)
![8 turn game](assets/histograms/histogram-8.svg)
![7 turn game](assets/histograms/histogram-7.svg)
![6 turn game](assets/histograms/histogram-6.svg)
![5 turn game](assets/histograms/histogram-5.svg)
![4 turn game](assets/histograms/histogram-4.svg)
![3 turn game](assets/histograms/histogram-3.svg)
![2 turn game](assets/histograms/histogram-2.svg)

</details>

## Conclusions

**breadbasket**, if they play once a day, should expect to win once every _42.2_ years! Unless the game dev is generous and uses some weird distribution to make players luckier. We have to compensate for Zach and Danny's elevated skill too -- let's say they're 100 times better than this simulation. See you all in 4.2 years!

## Feedback

Create an issue if you have any thoughts or feedback! I'd be curious to know if there is a better strategy to this game, but I'd cautiously call these results the best case scenario.
