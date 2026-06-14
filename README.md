# viz-flow

A real-time sorting algorithm visualizer built in Python. Watch bubble sort, insertion sort, merge sort, and quick sort compare and swap elements step by step on an interactive canvas.

This project was built as the final project for Stanford's Code in Place program.

## Why I built this

Every great project starts with a problem. Mine started with staring at code that compiled perfectly and still broke.

While learning C and working through sorting algorithms, I kept hitting the same wall every programmer knows: the code runs, no errors, but the output is wrong, with no way to trace what actually happened. I found myself constantly trying to reverse-engineer my own programs.

That frustration is what led to viz-flow: a tool that makes the invisible visible, letting you watch an algorithm think, step by step, swap by swap, instead of guessing.

## Features

- Live, animated visualization of four classic sorting algorithms
- Color-coded bars showing unsorted, comparing, swapping, and sorted states
- Real-time comparison and swap counters
- Adjustable bar count using on-screen `+` / `-` controls
- Shuffle button to generate a new random array at any time
- Custom neon-themed UI built from scratch on a canvas

## Algorithms included

- Bubble Sort
- Insertion Sort
- Merge Sort
- Quick Sort

## Controls

| Action | Description |
|---|---|
| Click an algorithm name | Runs that sort on the current array |
| Shuffle Array | Generates a new random array |
| `+` button | Adds 2 bars to the array |
| `-` button | Removes 1 bar from the array |

*Tip:* *The animation delay is intentionally generous so each step is easy to follow. With a high bar count, sorts can take a while to finish, so lower bar counts (around 8-15) give the smoothest experience.*

## Color legend

| Color | Meaning |
|---|---|
| White | Unsorted |
| Cyan | Currently comparing |
| Pink/Magenta | Currently swapping |
| Green | Sorted |

## Project structure

```
.
├── main.py                # Entry point — sets up the canvas and runs the event loop
├── visualizer.py           # Rendering: UI, bars, legend, and controls
├── sorting_algorithms.py    # Bubble, insertion, merge, and quick sort implementations
└── graphics.py              # Canvas/graphics library (Code in Place course library)
```

## Setup and running

1. Clone the repository:
   ```bash
   git clone https://github.com/akshat-bit420/Viz-Flow-Final-Project-at-Stanford-.git
   cd Viz-Flow-Final-Project-at-Stanford-
   ```

2. Install dependencies:
   ```bash
   pip install numpy
   ```

3. Run the program:
   ```bash
   python main.py
   ```

## Tech stack

- Python
- NumPy (for array generation)
- Custom canvas-based graphics (from Stanford's Code in Place course library)

## Acknowledgements

Built during Stanford's Code in Place program. Huge thanks to the CIP community for the support and feedback throughout the build.
