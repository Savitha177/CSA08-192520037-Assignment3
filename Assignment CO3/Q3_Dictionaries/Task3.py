
import random
import re
import time
from collections import Counter


# TASK 3: FARMER HELPLINE COMPLAINT ANALYSIS

STOP = {"not", "high"}

# Original examples supplied in the assessment
calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]


# 1. Normalise text: lowercase and remove punctuation
def tokenize(text):
    text = text.lower()
    return re.findall(r"\b\w+\b", text)


# 2. TODO 1: Count words using dict.get()
def frequencies(texts, stop):
    counts = {}

    for text in texts:
        for word in tokenize(text):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1

    return counts


# Alternative counting method using setdefault()
def frequencies_setdefault(texts, stop):
    counts = {}

    for text in texts:
        for word in tokenize(text):
            if word not in stop:
                counts.setdefault(word, 0)
                counts[word] += 1

    return counts


# 3. TODO 2: Return the k most frequent words
def top(counts, k):
    return sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )[:k]


# 4. Group complaints by district
def group_by_district(records):
    grouped = {}

    for district, complaint in records:
        grouped.setdefault(district, []).append(complaint)

    return grouped


# 5. Generate a larger synthetic complaint dataset
def generate_complaints(number):
    templates = [
        "Seeds not received, seeds delayed!",
        "Fertiliser price high.",
        "Seeds price high; subsidy not received.",
        "Water supply problem in field.",
        "Pesticide delivery delayed.",
        "Crop loan application pending.",
        "Seeds quality is poor.",
        "Fertiliser subsidy delayed.",
    ]

    return [
        templates[i % len(templates)]
        for i in range(number)
    ]


# 6. Dictionary counting for benchmarking
def count_dictionary(words):
    counts = {}

    for word in words:
        counts[word] = counts.get(word, 0) + 1

    return counts


# 7. list.count() counting for benchmarking
def count_with_list_count(words):
    counts = {}

    for word in set(words):
        counts[word] = words.count(word)

    return counts


# 8. Counter counting for benchmarking
def count_with_counter(words):
    return dict(Counter(words))


# Measure the three counting approaches
def benchmark(number):
    complaints = generate_complaints(number)

    # Tokenise once so every method gets identical input
    words = [
        word
        for complaint in complaints
        for word in tokenize(complaint)
        if word not in STOP
    ]

    start = time.perf_counter()
    dictionary_result = count_dictionary(words)
    dictionary_time = time.perf_counter() - start

    start = time.perf_counter()
    list_count_result = count_with_list_count(words)
    list_count_time = time.perf_counter() - start

    start = time.perf_counter()
    counter_result = count_with_counter(words)
    counter_time = time.perf_counter() - start

    assert dictionary_result == list_count_result
    assert dictionary_result == counter_result

    print(
        f"{number:>7} | {len(words):>8} | "
        f"{dictionary_time:.6f} | "
        f"{list_count_time:.6f} | "
        f"{counter_time:.6f} | PASS"
    )


# 9. Edge-case tests
def run_tests():
    print("\nEDGE CASE TESTS")

    # Empty text
    assert frequencies([""], STOP) == {}
    print("Empty text: PASS")

    # Case normalisation and punctuation
    result = frequencies(["SEEDS, seeds! Price."], STOP)
    assert result == {"seeds": 2, "price": 1}
    print("Upper/lower case and punctuation: PASS")

    # Stop words are excluded
    assert frequencies(["not high seeds"], STOP) == {"seeds": 1}
    print("Stop-word removal: PASS")

    # Empty input list
    assert frequencies([], STOP) == {}
    print("Empty complaint list: PASS")

    # District grouping
    records = [
        ("Chennai", "Seeds delayed"),
        ("Madurai", "Water problem"),
        ("Chennai", "Subsidy pending"),
    ]
    grouped = group_by_district(records)
    assert len(grouped["Chennai"]) == 2
    assert len(grouped["Madurai"]) == 1
    print("District grouping: PASS")

    # Tie-breaking alphabetically
    assert top({"received": 2, "price": 2, "seeds": 3}, 3) == [
        ("seeds", 3), ("price", 2), ("received", 2)
    ]
    print("Top-k tie-breaking: PASS")


def main():
    print("FARMER HELPLINE COMPLAINT ANALYSIS")
    print("=" * 50)

    counts = frequencies(calls, STOP)

    print("\nOriginal supplied TODO result:")
    print(top(counts, 3))

    # Confirm get() and setdefault() produce identical counts
    assert counts == frequencies_setdefault(calls, STOP)
    print("get() and setdefault() results match: PASS")

    # Display all word frequencies
    print("\nAll word frequencies:")
    for word, count in sorted(counts.items()):
        print(f"{word}: {count}")

    # District grouping demonstration
    records = [
        ("Chennai", "Seeds not received"),
        ("Madurai", "Water supply problem"),
        ("Chennai", "Fertiliser delayed"),
        ("Salem", "Crop loan pending"),
        ("Madurai", "Seeds price high"),
    ]

    grouped = group_by_district(records)

    print("\nCOMPLAINTS PER DISTRICT")
    for district in sorted(grouped):
        print(f"{district}: {len(grouped[district])} complaints")

    print("\nCOMPLAINTS GROUPED BY DISTRICT")
    for district in sorted(grouped):
        print(district, "->", grouped[district])

    # Performance experiments
    print("\nPERFORMANCE COMPARISON")
    print(
        "Complaints | Words | Dictionary(s) | "
        "list.count(s) | Counter(s) | Check"
    )
    print("-" * 83)

    for size in (1000, 10000, 100000):
        benchmark(size)

    run_tests()

    print("\nAll Task 3 correctness tests passed.")


if __name__ == "__main__":
    main()
