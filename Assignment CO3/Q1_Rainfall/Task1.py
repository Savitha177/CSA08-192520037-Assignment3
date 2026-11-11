# ============================================================
# TASK 1: DAILY RAINFALL ANALYSIS
# ============================================================

import random
import time


def weekly_totals(readings):
    return [
        sum(readings[i:i + 7])
        for i in range(0, len(readings) - 6, 7)
    ]


def moving_average_naive(readings, window=7):
    if window <= 0:
        raise ValueError("Window must be positive")

    return [
        sum(readings[i:i + window]) / window
        for i in range(len(readings) - window + 1)
    ]


def moving_average_running(readings, window=7):
    if window <= 0:
        raise ValueError("Window must be positive")

    if len(readings) < window:
        return []

    current_sum = sum(readings[:window])
    averages = [current_sum / window]

    for i in range(window, len(readings)):
        current_sum += readings[i] - readings[i - window]
        averages.append(current_sum / window)

    return averages


def find_extremes(readings):
    if not readings:
        return None

    maximum = max(readings)
    minimum = min(readings)

    return {
        "maximum": maximum,
        "maximum_day": readings.index(maximum) + 1,
        "minimum": minimum,
        "minimum_day": readings.index(minimum) + 1
    }


def performance_experiment():
    print("\nPERFORMANCE EXPERIMENT")
    print("-" * 75)
    print(f"{'Readings':>12} {'Naive (s)':>15} "
          f"{'Running sum (s)':>18} {'Results match':>18}")

    for size in [365, 36500, 365000]:
        readings = [random.randint(0, 100) for _ in range(size)]

        start = time.perf_counter()
        naive = moving_average_naive(readings)
        naive_time = time.perf_counter() - start

        start = time.perf_counter()
        running = moving_average_running(readings)
        running_time = time.perf_counter() - start

        matches = (
            len(naive) == len(running)
            and all(abs(a - b) < 1e-9 for a, b in zip(naive, running))
        )

        print(f"{size:>12,} {naive_time:>15.6f} "
              f"{running_time:>18.6f} {str(matches):>18}")

        assert matches


def run_tests():
    print("\nCORRECTNESS AND EDGE-CASE TESTS")

    assert moving_average_naive([]) == []
    assert moving_average_running([]) == []
    print("Empty list: PASS")

    assert moving_average_naive([1, 2, 3]) == []
    assert moving_average_running([1, 2, 3]) == []
    print("Fewer than 7 readings: PASS")

    readings = [1, 2, 3, 4, 5, 6, 7, 8]
    assert moving_average_naive(readings) == moving_average_running(readings)
    print("Naive and running-sum results match: PASS")

    assert weekly_totals([1, 2, 3, 4, 5, 6, 7]) == [28]
    print("Weekly total: PASS")

    assert moving_average_running([1, 2, 3, 4, 5, 6, 7])[0] == 4.0
    print("Moving average: PASS")

    assert [i + 1 for i, value in enumerate([0, 1, 0]) if value == 0] == [1, 3]
    print("Dry-day detection: PASS")

    print("All Task 1 correctness tests passed!")


def main():
    random.seed(42)

    readings = [random.randint(0, 100) for _ in range(365)]

    print("DAILY RAINFALL ANALYSIS")
    print("=" * 60)

    print("\nFirst 10 rainfall readings:")
    print(readings[:10])

    print("\nWeekly rainfall totals:")
    weeks = weekly_totals(readings)
    print(weeks)

    if weeks:
        wettest_week = max(range(len(weeks)), key=lambda i: weeks[i])
        driest_week = min(range(len(weeks)), key=lambda i: weeks[i])

        print("Wettest week:", wettest_week + 1,
              "Total rainfall:", weeks[wettest_week])
        print("Driest week:", driest_week + 1,
              "Total rainfall:", weeks[driest_week])

    extremes = find_extremes(readings)

    print("\nDAILY EXTREMES")
    print("Maximum rainfall:", extremes["maximum"],
          "on day", extremes["maximum_day"])
    print("Minimum rainfall:", extremes["minimum"],
          "on day", extremes["minimum_day"])

    print("\n7-DAY MOVING AVERAGE")
    averages = moving_average_running(readings)
    print("Number of averages:", len(averages))
    print("First 10 averages:", averages[:10])

    dry_days = [
        day for day, value in enumerate(readings, start=1)
        if value == 0
    ]

    print("\nDRY DAYS")
    print("Number of dry days:", len(dry_days))
    print("Dry-day numbers:", dry_days)

    print("\nSLICING EXAMPLES")
    print("readings[7:14]:", readings[7:14])
    print("readings[-7:]:", readings[-7:])
    print("readings[::7]:", readings[::7])

    print("\nMOVING-AVERAGE ADDITION COUNTS")
    n = len(readings)
    window = 7

    naive_additions = (n - window + 1) * (window - 1)
    running_additions = (window - 1) + 2 * (n - window)

    print("Naive method additions:", naive_additions)
    print("Running-sum additions:", running_additions)
    print("Naive complexity: O(n * window)")
    print("Running-sum complexity: O(n) for fixed window")

    run_tests()
    performance_experiment()


if __name__ == "__main__":
    main()