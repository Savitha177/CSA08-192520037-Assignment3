
import random
import time


# TASK 4: ELECTIVE REGISTRATION CLASH DETECTION

# Supplied assessment data
ai_elective = {
    "192311001", "192311004", "192311007", "192311009"
}

iot_elective = {
    "192311002", "192311004", "192311009", "192311010"
}

all_students = {
    f"1923110{i:02d}" for i in range(1, 11)
}


# 1. Find students registered for both electives
def find_both(ai, iot):
    return ai & iot


# 2. Find students registered for exactly one elective
def find_exactly_one(ai, iot):
    return ai ^ iot


# 3. Find students registered for neither elective
def find_neither(all_ids, ai, iot):
    return all_ids - (ai | iot)


# 4. Print sorted reports
def display_report(ai, iot, all_ids):
    both = find_both(ai, iot)
    exactly_one = find_exactly_one(ai, iot)
    neither = find_neither(all_ids, ai, iot)

    print("ELECTIVE REGISTRATION CLASH DETECTION")
    print("=" * 55)

    print("AI elective students       :", sorted(ai))
    print("IoT elective students      :", sorted(iot))
    print("All students               :", sorted(all_ids))

    print("\nRESULTS")
    print("clash      :", sorted(both))
    print("exactly one:", sorted(exactly_one))
    print("neither    :", sorted(neither))

    print("\nSUMMARY")
    print("Registered in both:", len(both))
    print("Registered in exactly one:", len(exactly_one))
    print("Registered in neither:", len(neither))


# 5. Compare set membership with list membership
def membership_experiment(size, queries):
    student_ids = [f"STU{i:07d}" for i in range(size)]

    # Convert the list into a set for comparison
    student_set = set(student_ids)

    # Use a fixed random seed for repeatable queries
    rng = random.Random(42)

    # Half of the queries are existing IDs and half are absent IDs
    test_queries = []
    for i in range(queries):
        if i % 2 == 0:
            test_queries.append(student_ids[rng.randrange(size)])
        else:
            test_queries.append(f"MISSING{i:07d}")

    # Time list membership
    start = time.perf_counter()
    list_results = [item in student_ids for item in test_queries]
    list_time = time.perf_counter() - start

    # Time set membership
    start = time.perf_counter()
    set_results = [item in student_set for item in test_queries]
    set_time = time.perf_counter() - start

    assert list_results == set_results

    print(
        f"{size:>10} | {queries:>7} | "
        f"{list_time:.6f} | {set_time:.6f} | PASS"
    )


# 6. Compare nested-loop intersection with set intersection
def intersection_nested_loop(ai, iot):
    result = set()

    for student in ai:
        for other_student in iot:
            if student == other_student:
                result.add(student)

    return result


def intersection_using_sets(ai, iot):
    return ai & iot


# 7. Correctness and edge-case tests
def run_tests():
    print("\nCORRECTNESS AND EDGE-CASE TESTS")

    # Expected results from the assessment
    assert find_both(ai_elective, iot_elective) == {
        "192311004", "192311009"
    }
    print("Students registered in both: PASS")

    assert find_exactly_one(ai_elective, iot_elective) == {
        "192311001", "192311007",
        "192311002", "192311010"
    }
    print("Exactly-one registration: PASS")

    assert find_neither(
        all_students, ai_elective, iot_elective
    ) == {
        "192311003", "192311005", "192311006", "192311008"
    }
    print("Neither-elective registration: PASS")

    # Empty set tests
    assert find_both(set(), iot_elective) == set()
    assert find_exactly_one(set(), iot_elective) == iot_elective
    print("Empty-set tests: PASS")

    # Identical sets
    assert find_exactly_one(ai_elective, ai_elective) == set()
    assert find_both(ai_elective, ai_elective) == ai_elective
    print("Identical-set tests: PASS")

    # No overlap
    no_overlap = {"A", "B"}
    other = {"C", "D"}
    assert find_both(no_overlap, other) == set()
    print("No-overlap test: PASS")

    # Duplicates disappear in a set
    duplicate_ids = {"STU01", "STU01", "STU02"}
    assert len(duplicate_ids) == 2
    print("Duplicate removal: PASS")

    # Compare two intersection approaches
    assert intersection_nested_loop(
        ai_elective, iot_elective
    ) == intersection_using_sets(ai_elective, iot_elective)
    print("Nested-loop and set intersection match: PASS")


def main():
    display_report(ai_elective, iot_elective, all_students)

    print("\nPERFORMANCE: LIST VS SET MEMBERSHIP")
    print("Students    | Queries | List time(s) | Set time(s) | Check")
    print("-" * 68)

    for size in (10_000, 100_000, 1_000_000):
        membership_experiment(size, queries=100)

    print("\nPERFORMANCE: INTERSECTION")
    start = time.perf_counter()
    nested_result = intersection_nested_loop(
        ai_elective, iot_elective
    )
    nested_time = time.perf_counter() - start

    start = time.perf_counter()
    set_result = intersection_using_sets(
        ai_elective, iot_elective
    )
    set_time = time.perf_counter() - start

    assert nested_result == set_result

    print(f"Nested-loop intersection: {nested_time:.8f} seconds")
    print(f"Set intersection        : {set_time:.8f} seconds")
    print("Intersection results match: PASS")

    run_tests()

    print("\nAll Task 4 correctness tests passed.")


if __name__ == "__main__":
    main()
