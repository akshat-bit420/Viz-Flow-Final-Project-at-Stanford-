"""
viz-flow — Visualizer module

Handles all rendering: the neon background, sidebar menu, bar count
controls, color legend, and the live bar chart that represents the
array being sorted.
"""

import numpy as np
import random
import time

# ─── config ───────────────────────────────────────────────
DEFAULT_BAR_COUNT = 8
BASE_DELAY = 0.33           # Standard animation speed

WIN_W = 600
WIN_H = 400
SIDEBAR_W = 180     # Under 30% of screen width

PLOT_TOP_PAD = 75
PLOT_BOTTOM_PAD = 65
PLOT_LEFT_PAD = 30
PLOT_RIGHT_PAD = 30
# ──────────────────────────────────────────────────────────

# Higher contrast palette configured to pop against the dark neon gradient backdrop
COL_UNSORTED = "#ffffff"   # Clean White for maximum legibility on dark areas
COL_COMPARING = "#00ffff"  # Bright Electric Cyan
COL_SWAPPING = "#ff007f"   # Neon Pink / Magenta
COL_SORTED = "#39ff14"     # Radioactive Neon Green


def make_array(n):
    arr = np.linspace(1, n, n, dtype=int)
    lst = arr.tolist()
    random.shuffle(lst)
    return lst


class Visualizer:
    def __init__(self, win, arr):
        self.win = win
        self.arr = arr
        self.n = len(arr)
        self.is_sorting = False
        self.delay = BASE_DELAY

        self._bar_ids = []
        self._stat_ids = []

        # ─── NEON ARC GLOW BACKGROUND ENGINE ──────────────────────────────
        self.win.create_rectangle(0, 0, WIN_W, WIN_H, "#08040c")

        center_x = WIN_W / 2
        center_y = -30

        steps = 70
        for i in range(steps, 0, -1):
            ratio = i / steps

            if ratio < 0.25:
                r, g, b = 8, 4, 12
            elif ratio < 0.65:
                p_ratio = (ratio - 0.25) / 0.40
                r = int(8 * (1 - p_ratio) + 90 * p_ratio)
                g = int(4 * (1 - p_ratio) + 20 * p_ratio)
                b = int(12 * (1 - p_ratio) + 190 * p_ratio)
            else:
                f_ratio = (ratio - 0.65) / 0.35
                r = int(90 * (1 - f_ratio) + 195 * f_ratio)
                g = int(20 * (1 - f_ratio) + 115 * f_ratio)
                b = int(190 * (1 - f_ratio) + 145 * f_ratio)

            hex_col = f"#{r:02x}{g:02x}{b:02x}"

            radius_x = int(ratio * 380)
            radius_y = int(ratio * 255)

            self.win.create_oval(
                center_x - radius_x, center_y - radius_y,
                center_x + radius_x, center_y + radius_y,
                hex_col
            )
        # ───────────────────────────────────────────────────────────────────

        # Clean sidebar dividing line
        self.win.create_line(SIDEBAR_W, 0, SIDEBAR_W, WIN_H, "#5b4c74")

        # ─── VECTOR GEOMETRIC "CIP" LOGO DESIGN ───────────────────────────
        plot_center_x = SIDEBAR_W + (WIN_W - SIDEBAR_W) / 2
        logo_y = 20

        self.win.create_rectangle(plot_center_x - 38, logo_y + 1, plot_center_x + 38, logo_y + 19, "#000000")
        self.win.create_rectangle(plot_center_x - 40, logo_y, plot_center_x + 40, logo_y + 18, "#251b35")

        self.win.create_line(plot_center_x - 30, logo_y + 4, plot_center_x - 15, logo_y + 4, "#ff007f")
        self.win.create_line(plot_center_x - 30, logo_y + 4, plot_center_x - 30, logo_y + 14, "#ff007f")
        self.win.create_line(plot_center_x - 30, logo_y + 14, plot_center_x - 15, logo_y + 14, "#ff007f")

        self.win.create_line(plot_center_x - 5, logo_y + 4, plot_center_x + 5, logo_y + 4, "#00ffff")
        self.win.create_line(plot_center_x, logo_y + 4, plot_center_x, logo_y + 14, "#00ffff")
        self.win.create_line(plot_center_x - 5, logo_y + 14, plot_center_x + 5, logo_y + 14, "#00ffff")

        self.win.create_line(plot_center_x + 15, logo_y + 4, plot_center_x + 15, logo_y + 14, "#39ff14")
        self.win.create_line(plot_center_x + 15, logo_y + 4, plot_center_x + 28, logo_y + 4, "#39ff14")
        self.win.create_line(plot_center_x + 28, logo_y + 4, plot_center_x + 28, logo_y + 9, "#39ff14")
        self.win.create_line(plot_center_x + 15, logo_y + 9, plot_center_x + 28, logo_y + 9, "#39ff14")

        self.win.create_line(plot_center_x - 40, logo_y + 24, plot_center_x + 40, logo_y + 24, "#ffb300")
        # ───────────────────────────────────────────────────────────────────

        # Left-aligned menu title text column
        self.win.create_text(24, 20, "--- Menu ---", color="#ffffff")

        self.buttons = {}
        algos = ["Shuffle Array", "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
        y_pos = 50
        for algo in algos:
            self.win.create_rectangle(24, y_pos - 9, SIDEBAR_W - 15, y_pos + 9, "#251b35")
            # Lifted text positioning coordinate up (y_pos - 3) to sit perfectly balanced inside the box
            self.win.create_text(36, y_pos - 3, algo, color="#ffffff")
            self.buttons[algo] = (y_pos - 9, y_pos + 9)
            y_pos += 26

        # ─── CENTER PANE COUNTER BUTTONS ──────────────────────────────────
        self.btn_minus_y0, self.btn_minus_y1 = 355, 385
        self.btn_plus_y0, self.btn_plus_y1 = 355, 385

        mid_pane_center_x = SIDEBAR_W + (WIN_W - SIDEBAR_W) / 2
        self.btn_minus_x0, self.btn_minus_x1 = mid_pane_center_x - 50, mid_pane_center_x - 10
        self.btn_plus_x0, self.btn_plus_x1 = mid_pane_center_x + 10, mid_pane_center_x + 50

        self.win.create_rectangle(self.btn_minus_x0, self.btn_minus_y0, self.btn_minus_x1, self.btn_minus_y1, "#251b35")
        self.win.create_text((self.btn_minus_x0 + self.btn_minus_x1) / 2, self.btn_minus_y0 + 7, "-", color="#ffffff")

        self.win.create_rectangle(self.btn_plus_x0, self.btn_plus_y0, self.btn_plus_x1, self.btn_plus_y1, "#251b35")
        self.win.create_text((self.btn_plus_x0 + self.btn_plus_x1) / 2, self.btn_plus_y0 + 7, "+", color="#ffffff")
        # ───────────────────────────────────────────────────────────────────

        # Left-aligned colors header text column
        self.win.create_text(24, 285, "Colors", color="#ffffff")
        self.legend = [
            ("Unsorted", COL_UNSORTED),
            ("Comparing", COL_COMPARING),
            ("Swapping", COL_SWAPPING),
            ("Sorted", COL_SORTED),
        ]

        y = 310
        swatch_w = 12
        for name, col in self.legend:
            swatch_left = 24
            swatch_right = swatch_left + swatch_w
            self.win.create_rectangle(swatch_left, y - 5, swatch_right, y + 7, col)
            self.win.create_text(swatch_right + 10, y, name, color="#dcdcdc")
            y += 20

        self._update_stats_and_bars("Idle", 0, 0, set(), set(), set())

    def _bar_geometry(self, idx, val, max_val):
        plot_left = SIDEBAR_W + PLOT_LEFT_PAD
        plot_right = WIN_W - PLOT_RIGHT_PAD
        plot_w = max(1, plot_right - plot_left)

        plot_top = PLOT_TOP_PAD
        plot_bottom = WIN_H - PLOT_BOTTOM_PAD
        usable_h = max(1, plot_bottom - plot_top)

        bar_space = plot_w / self.n
        bar_w = max(1, bar_space * 0.85)
        x0 = plot_left + idx * bar_space + (bar_space - bar_w) / 2
        x1 = x0 + bar_w

        h = (val / max_val) * usable_h
        y1 = plot_bottom
        y0 = y1 - h
        return x0, y0, x1, y1

    def _color_for(self, idx, comparing, swapping, sorted_set):
        if idx in swapping:
            return COL_SWAPPING
        if idx in comparing:
            return COL_COMPARING
        if idx in sorted_set:
            return COL_SORTED
        return COL_UNSORTED

    def _update_stats_and_bars(self, algo_name, comps, swaps, comparing, swapping, sorted_set):
        for cid in self._stat_ids:
            self.win.delete(cid)
        self._stat_ids.clear()

        s1 = self.win.create_text(24, 195, "Status: " + algo_name, color="#ff6600")
        s2 = self.win.create_text(24, 220, "Comparisons: " + str(comps), color="#ff6600")
        s3 = self.win.create_text(24, 245, "Swaps: " + str(swaps), color="#ff6600")
        self._stat_ids.extend([s1, s2, s3])

        for bid in self._bar_ids:
            self.win.delete(bid)
        self._bar_ids.clear()

        max_val = max(self.arr) if self.arr else 1
        for i, v in enumerate(self.arr):
            x0, y0, x1, y1 = self._bar_geometry(i, v, max_val)
            col = self._color_for(i, comparing, swapping, sorted_set)
            bid = self.win.create_rectangle(x0, y0, x1, y1, col)
            self._bar_ids.append(bid)

    def render(self, algo_name, comps, swaps, comparing=None, swapping=None, sorted_set=None) -> bool:
        if getattr(self.win, "closed", False):
            return False

        comparing = set(comparing or [])
        swapping = set(swapping or [])
        sorted_set = set(sorted_set or [])

        try:
            self._update_stats_and_bars(algo_name, comps, swaps, comparing, swapping, sorted_set)
            time.sleep(self.delay)
            return True
        except Exception:
            return False

    def check_menu_click(self, mouse_x, mouse_y):
        if self.btn_minus_x0 <= mouse_x <= self.btn_minus_x1 and self.btn_minus_y0 <= mouse_y <= self.btn_minus_y1:
            return "MINUS_BAR"
        if self.btn_plus_x0 <= mouse_x <= self.btn_plus_x1 and self.btn_plus_y0 <= mouse_y <= self.btn_plus_y1:
            return "PLUS_BAR"

        if mouse_x < 24 or mouse_x > SIDEBAR_W - 15:
            return None
        for algo, (y0, y1) in self.buttons.items():
            if y0 <= mouse_y <= y1:
                return algo
        return None

    def change_bar_count(self, amount):
        new_n = self.n + amount
        if 5 <= new_n <= 100:
            self.n = new_n
            self.delay = 0.02 if new_n > 35 else BASE_DELAY
            self.reset_with_new_array()

    def reset_with_new_array(self):
        self.arr = make_array(self.n)
        self._update_stats_and_bars("Idle", 0, 0, set(), set(), set())
