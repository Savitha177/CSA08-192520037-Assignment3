# ============================================================
# TASK 5: CLEANING SENSOR READINGS
# ============================================================

import random
import sys
import time


SAMPLE_READINGS = [
    (1, 5.0),
    (2, 10.0),
    (3, -3.0),
    (4, 55.0),
    (5, 2.0),
    (6, 8.0),
    (7, 50.0),
    (8, -50.0),
    (9, 60.0),
    (10, 1.0)
]


def clean_loop(readings):
    cleaned = []

    for minute, temperature in readings:
        if -50 <= temperature <= 50:
            cleaned.append((minute, temperature))

    return cleaned


def clean_comprehension(readings):
    return [
        (minute, temperature)
        for minute, temperature in readings
        if -50 <= temperature <= 50
    ]


def clean_filter(readings):
    return list(
        filter(
            lambda record: -50 <= record[1] <= 50,
            readings
        )
    )


def convert_to_fahrenheit(readings):
    return [
        (minute, temperature * 9 / 5 + 32)
        for minute, temperature in readings
    ]


def convert_with_map(readings):
    return list(
        map(
            lambda record: (
                record[0],
                record[1] * 9 / 5 + 32
            ),
            readings
        )
    )


def find_alarm_minutes(readings):
    return [
        minute
        for minute, temperature in readings
        if temperature < 2 or temperature > 8
    ]


def benchmark():
    print("\nPERFORMANCE COMPARISON")
    print("-" * 70)
    print(f"{'Readings':>12} {'Loop (s)':>14} "
          f"{'Comprehension (s)':>20} {'Filter (s)':>14}")

    for size in [10000, 100000, 1000000]:
        readings = [
            (i, random.uniform(-60, 60))
            for i in range(size)
        ]

        results = []
        timings = []

        for method in [clean_loop, clean_comprehension, clean_filter]:
            start = time.perf_counter()
            result = method(readings)
            elapsed = time.perf_counter() - start

            results.append(result)
            timings.append(elapsed)

        assert results[0] == results[1] == results[2]

        print(f"{size:>12,} {timings[0]:>14.6f} "
              f"{timings[1]:>20.6f} {timings[2]:>14.6f}")


def run_tests():
    print("\nCORRECTNESS AND EDGE-CASE TESTS")

    assert clean_comprehension([]) == []
    print("Empty readings: PASS")

    valid = [(1, 0.0), (2, 50.0), (3, -50.0)]
    assert clean_comprehension(valid) == valid
    print("All-valid readings: PASS")

    invalid = [(1, 55.0), (2, -55.0)]
    assert clean_comprehension(invalid) == []
    print("All-invalid readings: PASS")

    sample = [(1, 5.0), (2, 55.0), (3, -50.0)]
    assert clean_loop(sample) == clean_comprehension(sample)
    assert clean_filter(sample) == clean_comprehension(sample)
    print("All cleaning methods match: PASS")

    assert convert_to_fahrenheit([(1, 0.0)]) == [(1, 32.0)]
    assert convert_with_map([(1, 0.0)]) == [(1, 32.0)]
    print("Fahrenheit conversion using comprehension and map: PASS")

    assert find_alarm_minutes([
        (1, 2.0),
        (2, 8.0),
        (3, 1.9),
        (4, 8.1)
    ]) == [3, 4]
    print("Alarm boundary tests: PASS")

    print("All Task 5 correctness tests passed!")


def main():
    print("SENSOR READING ANALYSIS")
    print("=" * 60)

    print("\nORIGINAL READINGS")
    print(SAMPLE_READINGS)

    loop_result = clean_loop(SAMPLE_READINGS)
    comprehension_result = clean_comprehension(SAMPLE_READINGS)
    filter_result = clean_filter(SAMPLE_READINGS)

    print("\nCLEANED READINGS")
    print(comprehension_result)

    print("\nInvalid readings removed:")
    print([
        record for record in SAMPLE_READINGS
        if record not in comprehension_result
    ])

    fahrenheit = convert_to_fahrenheit(comprehension_result)
    fahrenheit_map = convert_with_map(comprehension_result)

    print("\nFAHRENHEIT USING COMPREHENSION")
    print(fahrenheit)

    print("\nFAHRENHEIT USING MAP AND LAMBDA")
    print(fahrenheit_map)

    print("\nALARM MINUTES")
    print(find_alarm_minutes(comprehension_result))

    print("\nSUMMARY")
    print("Original readings:", len(SAMPLE_READINGS))
    print("Valid readings:", len(comprehension_result))
    print("Invalid readings:", len(SAMPLE_READINGS) - len(comprehension_result))
    print("Alarm count:", len(find_alarm_minutes(comprehension_result)))

    print("\nMETHODS GIVE IDENTICAL RESULTS:",
          loop_result == comprehension_result == filter_result)

    print("\nMEMORY COMPARISON")
    generator = (
        (minute, temperature)
        for minute, temperature in SAMPLE_READINGS
        if -50 <= temperature <= 50
    )

    print("List shallow size:", sys.getsizeof(comprehension_result), "bytes")
    print("Generator object size:", sys.getsizeof(generator), "bytes")
    print("Note: these sizes exclude referenced contents.")

    print("\nCOMPLEXITY")
    print("Loop cleaning: O(n) time, O(n) output space")
    print("List comprehension: O(n) time, O(n) output space")
    print("Generator filtering: O(n) time, O(1) auxiliary space")

    run_tests()
    benchmark()


if __name__ == "__main__":
    random.seed(42)
    main()