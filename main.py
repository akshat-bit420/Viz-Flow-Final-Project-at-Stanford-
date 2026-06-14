"""
viz-flow — Real-time sorting algorithm visualizer

Run this file to launch the visualizer.

Controls:
  - Click an algorithm in the sidebar menu to run it (Bubble, Insertion,
    Merge, or Quick Sort).
  - "Shuffle Array" generates a new random array.
  - "+" adds 2 bars to the canvas, "-" removes 1 bar.

Note: the animation delay is intentionally generous for visibility, so
sorts with a higher bar count can run slowly. Lower bar counts are
recommended for the smoothest experience.
"""

import time
from graphics import Canvas

from visualizer import Visualizer, make_array, WIN_W, WIN_H, DEFAULT_BAR_COUNT
from sorting_algorithms import bubble_sort, insertion_sort, merge_sort, quick_sort


def main():
    arr = make_array(DEFAULT_BAR_COUNT)
    win = Canvas(WIN_W, WIN_H)
    vis = Visualizer(win, arr)

    while not getattr(win, "closed", False):
        try:
            click_pt = win.get_last_click()
            if click_pt:
                mx = click_pt[0]
                my = click_pt[1]

                choice = vis.check_menu_click(mx, my)

                if choice and not vis.is_sorting:
                    if choice == "Shuffle Array":
                        vis.reset_with_new_array()
                    elif choice == "PLUS_BAR":
                        vis.change_bar_count(2)
                    elif choice == "MINUS_BAR":
                        vis.change_bar_count(-1)
                    else:
                        vis.is_sorting = True
                        if choice == "Bubble Sort":
                            bubble_sort(vis)
                        elif choice == "Insertion Sort":
                            insertion_sort(vis)
                        elif choice == "Merge Sort":
                            merge_sort(vis)
                        elif choice == "Quick Sort":
                            quick_sort(vis)
                        vis.is_sorting = False

            time.sleep(0.02)
        except Exception:
            break


if __name__ == "__main__":
    main()
