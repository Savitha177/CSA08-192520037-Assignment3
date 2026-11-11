
# ============================================================
# TASK 6: NESTED DATA STRUCTURES - RAILWAY TIMETABLE ANALYSIS
# ============================================================

import time
import sys


# ------------------------------------------------------------
# 1. SAMPLE RAILWAY TIMETABLE
# Train number -> name, station tuples, running days
# ------------------------------------------------------------

trains = {
    "12601": {
        "name": "Chennai Express",
        "stations": [
            ("Chennai", "06:00", "06:10"),
            ("Katpadi", "08:00", "08:05"),
            ("Bengaluru", "10:30", "10:40"),
        ],
        "running_days": {"Monday", "Wednesday", "Friday"},
    },
    "12602": {
        "name": "Southern Express",
        "stations": [
            ("Bengaluru", "07:00", "07:10"),
            ("Katpadi", "09:30", "09:35"),
            ("Chennai", "12:00", "12:10"),
        ],
        "running_days": {"Tuesday", "Thursday", "Saturday"},
    },
    "12603": {
        "name": "Coastal Express",
        "stations": [
            ("Chennai", "08:00", "08:15"),
            ("Vellore", "10:00", "10:05"),
            ("Katpadi", "10:30", "10:35"),
            ("Bengaluru", "13:00", "13:10"),
        ],
        "running_days": {
            "Monday", "Tuesday", "Wednesday", "Thursday",
            "Friday", "Saturday", "Sunday"
        },
    },
    "12604": {
        "name": "City Link",
        "stations": [
            ("Bengaluru", "14:00", "14:10"),
            ("Vellore", "17:00", "17:05"),
            ("Chennai", "19:30", "19:40"),
        ],
        "running_days": {"Monday", "Tuesday", "Friday", "Sunday"},
    },
    "12605": {
        "name": "Hill Express",
        "stations": [
            ("Chennai", "15:00", "15:10"),
            ("Katpadi", "17:00", "17:05"),
            ("Bengaluru", "19:00", "19:10"),
        ],
        "running_days": {"Wednesday", "Thursday", "Saturday"},
    },
}


DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday", "Saturday", "Sunday"
]

STATIONS = [
    "Chennai", "Katpadi", "Vellore", "Bengaluru",
    "Salem", "Erode", "Coimbatore", "Madurai",
    "Trichy", "Villupuram"
]


# ------------------------------------------------------------
# 2. DISPLAY TIMETABLE
# ------------------------------------------------------------

def display_timetable(data):
    for train_number, details in sorted(data.items()):
        print(f"\nTrain: {train_number} - {details['name']}")
        print("Running days:", ", ".join(sorted(details["running_days"])))

        print(f"{'Station':<15} {'Arrival':<10} {'Departure':<10}")

        for station, arrival, departure in details["stations"]:
            print(f"{station:<15} {arrival:<10} {departure:<10}")


# ------------------------------------------------------------
# 3. BUILD STATION INDEX
# Each station maps to the train numbers stopping there.
# ------------------------------------------------------------

def build_station_index(data):
    index = {}

    for train_number, details in data.items():
        for station, arrival, departure in details["stations"]:
            index.setdefault(station, set()).add(train_number)

    return index


# ------------------------------------------------------------
# 4. SEARCH BY SCANNING ALL TRAINS
# ------------------------------------------------------------

def search_station_scan(data, station, day):
    results = []

    for train_number, details in data.items():
        if day not in details["running_days"]:
            continue

        for stop, arrival, departure in details["stations"]:
            if stop == station:
                results.append(
                    (departure, train_number, details["name"], arrival)
                )
                break

    return sorted(results)


# ------------------------------------------------------------
# 5. SEARCH USING THE STATION INDEX
# ------------------------------------------------------------

def search_station_indexed(data, index, station, day):
    results = []

    for train_number in index.get(station, set()):
        details = data[train_number]

        if day not in details["running_days"]:
            continue

        for stop, arrival, departure in details["stations"]:
            if stop == station:
                results.append(
                    (departure, train_number, details["name"], arrival)
                )
                break

    return sorted(results)


# ------------------------------------------------------------
# 6. QUERY A STATION ON A PARTICULAR DAY
# ------------------------------------------------------------

def query_station(data, index, station, day):
    print(f"\nTRAINS AT {station.upper()} ON {day.upper()}")
    print("-" * 65)

    results = search_station_indexed(data, index, station, day)

    if not results:
        print("No trains found for this station and day.")
        return

    print(
        f"{'Departure':<12} {'Train No.':<12} "
        f"{'Train Name':<25} {'Arrival'}"
    )

    for departure, train_number, name, arrival in results:
        print(
            f"{departure:<12} {train_number:<12} "
            f"{name:<25} {arrival}"
        )


# ------------------------------------------------------------
# 7. GENERATE SYNTHETIC TIMETABLE DATA
# ------------------------------------------------------------

def generate_trains(number_of_trains):
    data = {}

    for i in range(number_of_trains):
        train_number = str(20000 + i)

        # Create three consecutive stations for each train.
        start = i % len(STATIONS)
        route = [
            STATIONS[(start + j) % len(STATIONS)]
            for j in range(3)
        ]

        station_records = []

        for j, station in enumerate(route):
            hour = (6 + (i % 12) + j * 2) % 24
            arrival = f"{hour:02d}:00"
            departure = f"{hour:02d}:10"

            station_records.append(
                (station, arrival, departure)
            )

        # Generate a repeatable set of running days.
        running_days = {
            day for day_number, day in enumerate(DAYS)
            if (i + day_number) % 2 == 0
        }

        data[train_number] = {
            "name": f"Express {i + 1}",
            "stations": station_records,
            "running_days": running_days,
        }

    return data


# ------------------------------------------------------------
# 8. PERFORMANCE EXPERIMENT
# Compare scanning with indexed searching.
# ------------------------------------------------------------

def performance_experiment():
    print("\nPERFORMANCE: STATION SEARCH")
    print("=" * 78)

    print(
        f"{'Trains':>10} {'Scan time (s)':>16} "
        f"{'Index build (s)':>17} {'Indexed query (s)':>19}"
    )
    print("-" * 78)

    for size in [100, 1_000, 10_000]:
        data = generate_trains(size)

        # Measure station index construction.
        start = time.perf_counter()
        index = build_station_index(data)
        build_time = time.perf_counter() - start

        station = "Chennai"
        day = "Monday"

        # Verify both approaches before timing.
        scan_result = search_station_scan(data, station, day)
        indexed_result = search_station_indexed(
            data, index, station, day
        )

        assert scan_result == indexed_result

        repetitions = 20

        start = time.perf_counter()
        for _ in range(repetitions):
            scan_result = search_station_scan(data, station, day)
        scan_time = (time.perf_counter() - start) / repetitions

        start = time.perf_counter()
        for _ in range(repetitions):
            indexed_result = search_station_indexed(
                data, index, station, day
            )
        indexed_time = (time.perf_counter() - start) / repetitions

        print(
            f"{size:>10,} {scan_time:>16.6f} "
            f"{build_time:>17.6f} {indexed_time:>19.6f}"
        )

    print("\nScan and indexed search results match: PASS")


# ------------------------------------------------------------
# 9. APPROXIMATE MEMORY MEASUREMENT
# These are shallow sizes, not total memory usage.
# ------------------------------------------------------------

def memory_experiment(data, index):
    print("\nSTATION INDEX MEMORY")
    print("-" * 45)

    print(
        f"Outer timetable dictionary: "
        f"{sys.getsizeof(data):,} bytes"
    )
    print(
        f"Outer station index:         "
        f"{sys.getsizeof(index):,} bytes"
    )

    print("Note: Measurements exclude nested objects and their contents.")


# ------------------------------------------------------------
# 10. CORRECTNESS AND EDGE-CASE TESTS
# ------------------------------------------------------------

def run_tests(data, index):
    print("\nCORRECTNESS AND EDGE-CASE TESTS")
    print("-" * 50)

    # Known station and running day.
    result = search_station_indexed(
        data, index, "Chennai", "Monday"
    )
    assert len(result) == 3
    print("Known station and running day: PASS")

    # Unknown station.
    result = search_station_indexed(
        data, index, "Unknown Station", "Monday"
    )
    assert result == []
    print("Unknown station: PASS")

    # Coastal Express stops at Katpadi on Sunday.
    result = search_station_indexed(
        data, index, "Katpadi", "Sunday"
    )
    assert result == [
        ("10:35", "12603", "Coastal Express", "10:30")
    ]
    print("Katpadi with a matching Sunday train: PASS")

    # Unknown day produces no matches.
    result = search_station_indexed(
        data, index, "Chennai", "Funday"
    )
    assert result == []
    print("Unknown day: PASS")

    # Empty timetable and empty index.
    assert search_station_scan({}, "Chennai", "Monday") == []
    assert search_station_indexed(
        {}, {}, "Chennai", "Monday"
    ) == []
    print("Empty timetable: PASS")

    # Compare scanning and indexing for all stations and days.
    for station in STATIONS:
        for day in DAYS:
            scan = search_station_scan(data, station, day)
            indexed = search_station_indexed(
                data, index, station, day
            )
            assert scan == indexed

    print("Scan vs index across all stations and days: PASS")

    # Verify that every index entry points to a real train and stop.
    for station, train_numbers in index.items():
        for train_number in train_numbers:
            assert train_number in data

            assert any(
                stop == station
                for stop, arrival, departure
                in data[train_number]["stations"]
            )

    print("Station index integrity: PASS")
    print("\nAll Task 6 correctness tests passed!")


# ------------------------------------------------------------
# 11. MAIN PROGRAM
# ------------------------------------------------------------

def main():
    print("RAILWAY TIMETABLE ANALYSIS")
    print("=" * 65)

    print("\nSAMPLE TIMETABLE")
    display_timetable(trains)

    station_index = build_station_index(trains)

    query_station(trains, station_index, "Chennai", "Monday")
    query_station(trains, station_index, "Katpadi", "Sunday")
    query_station(
        trains, station_index, "Unknown Station", "Monday"
    )

    run_tests(trains, station_index)
    memory_experiment(trains, station_index)
    performance_experiment()


if __name__ == "__main__":
    main()
