"""
viz-flow — Sorting algorithms module

Each function takes a Visualizer instance (`vis`) and animates the sort
step by step by calling `vis.render(...)` between comparisons and swaps.

Each function returns early (without finishing) if `vis.render(...)`
returns False, which happens when the visualizer window is closed
mid-sort.
"""


def bubble_sort(vis):
    n = len(vis.arr)
    sorted_set = set()
    comps = swaps = 0

    for i in range(n - 1):
        for j in range(n - 1 - i):
            comps += 1
            if not vis.render("Bubble Sort", comps, swaps, comparing=[j, j + 1], sorted_set=sorted_set):
                return
            if vis.arr[j] > vis.arr[j + 1]:
                vis.arr[j], vis.arr[j + 1] = vis.arr[j + 1], vis.arr[j]
                swaps += 1
                if not vis.render("Bubble Sort", comps, swaps, swapping=[j, j + 1], sorted_set=sorted_set):
                    return
        sorted_set.add(n - 1 - i)
    sorted_set.add(0)
    vis.render("Bubble Sort (DONE)", comps, swaps, sorted_set=set(range(n)))


def insertion_sort(vis):
    n = len(vis.arr)
    sorted_set = {0}
    comps = swaps = 0

    for i in range(1, n):
        j = i
        while j > 0:
            comps += 1
            if not vis.render("Insertion Sort", comps, swaps, comparing=[j - 1, j], sorted_set=sorted_set):
                return
            if vis.arr[j - 1] > vis.arr[j]:
                vis.arr[j - 1], vis.arr[j] = vis.arr[j], vis.arr[j - 1]
                swaps += 1
                if not vis.render("Insertion Sort", comps, swaps, swapping=[j - 1, j], sorted_set=sorted_set):
                    return
                j -= 1
            else:
                break
        sorted_set.add(i)
    vis.render("Insertion Sort (DONE)", comps, swaps, sorted_set=set(range(n)))


def merge_sort(vis):
    comps = swaps = 0
    sorted_set = set()

    def ms_divide(start, end):
        nonlocal comps, swaps
        if end - start <= 1:
            return True

        mid = (start + end) // 2
        if not ms_divide(start, mid): return False
        if not ms_divide(mid, end): return False

        left = vis.arr[start:mid]
        right = vis.arr[mid:end]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            comps += 1
            if not vis.render("Merge Sort", comps, swaps, comparing=[start + i, mid + j], sorted_set=sorted_set):
                return False

            if left[i] <= right[j]:
                vis.arr[k] = left[i]
                i += 1
            else:
                vis.arr[k] = right[j]
                j += 1
                swaps += 1
            k += 1
            if not vis.render("Merge Sort", comps, swaps, swapping=[k - 1], sorted_set=sorted_set):
                return False

        while i < len(left):
            vis.arr[k] = left[i]
            i += 1
            k += 1
            if not vis.render("Merge Sort", comps, swaps, swapping=[k - 1], sorted_set=sorted_set):
                return False

        while j < len(right):
            vis.arr[k] = right[j]
            j += 1
            k += 1
            if not vis.render("Merge Sort", comps, swaps, swapping=[k - 1], sorted_set=sorted_set):
                return False

        return True

    if ms_divide(0, len(vis.arr)):
        vis.render("Merge Sort (DONE)", comps, swaps, sorted_set=set(range(len(vis.arr))))


def quick_sort(vis):
    comps = swaps = 0
    sorted_set = set()

    def qs_logic(low, high):
        nonlocal comps, swaps
        if low >= high:
            if low == high:
                sorted_set.add(low)
            return True

        pivot = vis.arr[high]
        i = low - 1

        for j in range(low, high):
            comps += 1
            if not vis.render("Quick Sort", comps, swaps, comparing=[j, high], sorted_set=sorted_set):
                return False
            if vis.arr[j] < pivot:
                i += 1
                vis.arr[i], vis.arr[j] = vis.arr[j], vis.arr[i]
                swaps += 1
                if not vis.render("Quick Sort", comps, swaps, swapping=[i, j], sorted_set=sorted_set):
                    return False

        vis.arr[i + 1], vis.arr[high] = vis.arr[high], vis.arr[i + 1]
        swaps += 1
        pivot_idx = i + 1
        sorted_set.add(pivot_idx)

        if not vis.render("Quick Sort", comps, swaps, swapping=[pivot_idx, high], sorted_set=sorted_set):
            return False

        if not qs_logic(low, pivot_idx - 1): return False
        if not qs_logic(pivot_idx + 1, high): return False
        return True

    if qs_logic(0, len(vis.arr) - 1):
        vis.render("Quick Sort (DONE)", comps, swaps, sorted_set=set(range(len(vis.arr))))
