
import copy
import sys
import time


# TASK 2: TUPLES, MUTABILITY AND COPYING

def demonstrate_grid():
    print("\n1. GRID ALIASING BUG AND CORRECTION")
    rows, cols = 3, 4

    # Incorrect: every row refers to the same list
    bad = [[0] * cols] * rows
    bad[0][1] = 7

    # TODO 1: Correct grid using list comprehension
    good = [[0] * cols for _ in range(rows)]
    good[0][1] = 7

    print("bad :", bad)
    print("good:", good)
    print("bad[0] is bad[1]:", bad[0] is bad[1])
    print("good[0] is good[1]:", good[0] is good[1])

    print("IDs of bad rows:", [id(row) for row in bad])
    print("IDs of good rows:", [id(row) for row in good])


def demonstrate_tuples_and_dictionary():
    print("\n2. TUPLES AS DICTIONARY KEYS")

    stops = {
        (13.0827, 80.2707): "Chennai Central",
        (13.0418, 80.2341): "T. Nagar",
        (13.0569, 80.2425): "Nandanam"
    }

    for (latitude, longitude), stop_name in stops.items():
        print(
            f"{stop_name}: latitude={latitude}, "
            f"longitude={longitude}"
        )

    print("Lookup:", stops[(13.0418, 80.2341)])

    try:
        stops[[13.0418, 80.2341]] = "Invalid key"
    except TypeError as error:
        print("List key error:", error)


def demonstrate_unpacking():
    print("\n3. TUPLE UNPACKING")

    stops = [
        ("Chennai Central", 13.0827, 80.2707),
        ("T. Nagar", 13.0418, 80.2341),
        ("Nandanam", 13.0569, 80.2425)
    ]

    for name, latitude, longitude in stops:
        print(f"{name}: ({latitude}, {longitude})")


def demonstrate_copying():
    print("\n4. ALIASING, SHALLOW COPY AND DEEP COPY")

    original = [[1, 2], [3, 4]]
    alias = original
    shallow_slice = original[:]
    shallow_copy = copy.copy(original)
    deep = copy.deepcopy(original)

    print("original is alias:", original is alias)
    print("original is shallow_slice:", original is shallow_slice)
    print("original is shallow_copy:", original is shallow_copy)
    print("original is deep:", original is deep)

    print("Inner list shared by slice:", original[0] is shallow_slice[0])
    print("Inner list shared by copy.copy:", original[0] is shallow_copy[0])
    print("Inner list shared by deepcopy:", original[0] is deep[0])

    original[0][0] = 99
    print("After changing original[0][0]:")
    print("original:", original)
    print("alias:", alias)
    print("shallow slice:", shallow_slice)
    print("shallow copy:", shallow_copy)
    print("deep copy:", deep)

    original[0] = [7, 8]
    print("After replacing original[0]:")
    print("alias:", alias)
    print("shallow copy:", shallow_copy)
    print("deep copy:", deep)


def demonstrate_mutable_inside_tuple():
    print("\n5. MUTABLE LIST INSIDE AN IMMUTABLE TUPLE")

    data = ("Bus Stop A", [10, 20, 30])
    print("Before:", data)

    data[1].append(40)
    print("After appending to the inner list:", data)

    try:
        data[0] = "Bus Stop B"
    except TypeError as error:
        print("Tuple assignment error:", error)


def memory_comparison():
    print("\n6. MEMORY COMPARISON")

    values = list(range(1_000_000))
    tuple_values = tuple(values)

    list_bytes = sys.getsizeof(values)
    tuple_bytes = sys.getsizeof(tuple_values)

    print("Number of values:", len(values))
    print("List container size:", list_bytes, "bytes")
    print("Tuple container size:", tuple_bytes, "bytes")
    print("Note: sizes exclude the referenced integer objects.")


def timing_comparison():
    print("\n7. CREATION AND INDEXING TIME")

    n = 1_000_000
    repetitions = 20

    start = time.perf_counter()
    list_values = list(range(n))
    list_creation = time.perf_counter() - start

    start = time.perf_counter()
    tuple_values = tuple(range(n))
    tuple_creation = time.perf_counter() - start

    # Repeat indexing to make the timing easier to measure
    start = time.perf_counter()
    list_total = 0
    for _ in range(repetitions):
        list_total += list_values[n // 2]
    list_indexing = time.perf_counter() - start

    start = time.perf_counter()
    tuple_total = 0
    for _ in range(repetitions):
        tuple_total += tuple_values[n // 2]
    tuple_indexing = time.perf_counter() - start

    print(f"List creation:  {list_creation:.6f} seconds")
    print(f"Tuple creation: {tuple_creation:.6f} seconds")
    print(f"List indexing ({repetitions} reads):  "
          f"{list_indexing:.6f} seconds")
    print(f"Tuple indexing ({repetitions} reads): "
          f"{tuple_indexing:.6f} seconds")
    print("Indexing results match:", list_total == tuple_total)


def test_grid():
    print("\n8. CORRECTNESS TESTS")

    good = [[0] * 4 for _ in range(3)]
    good[0][1] = 7

    assert good == [
        [0, 7, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    assert good[0] is not good[1]
    assert good[1] is not good[2]

    print("Grid test: PASS")

    # Demonstrate that a tuple can contain a mutable list
    data = ("Stop A", [1, 2])
    data[1].append(3)
    assert data == ("Stop A", [1, 2, 3])
    print("Mutable object inside tuple test: PASS")

    # Tuple keys work; list keys fail
    stops = {(13.0418, 80.2341): "T. Nagar"}
    assert stops[(13.0418, 80.2341)] == "T. Nagar"

    try:
        stops[[13.0418, 80.2341]]
    except TypeError:
        print("Unhashable list key test: PASS")


def main():
    demonstrate_grid()
    demonstrate_tuples_and_dictionary()
    demonstrate_unpacking()
    demonstrate_copying()
    demonstrate_mutable_inside_tuple()
    memory_comparison()
    timing_comparison()
    test_grid()

    print("\nAll Task 2 correctness tests passed.")


if __name__ == "__main__":
    main()
