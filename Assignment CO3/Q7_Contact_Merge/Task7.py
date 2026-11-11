# ============================================================
# TASK 7: CONTACT MERGING AND DUPLICATE DETECTION
# ============================================================

import time


contacts = [
    {"name": "  ARUN Kumar ", "phone": "+91 98765 43210",
     "email": "ARUN@example.com"},
    {"name": "Arun Kumar", "phone": "+91-98765-43210",
     "email": "arun.work@example.com"},
    {"name": "Priya Sharma", "phone": "98765-11111",
     "email": "priya@example.com"},
    {"name": "Arun Kumar", "phone": "9000000001",
     "email": "arun.other@example.com"},
    {"name": "Arun Kumar", "phone": "9000000002",
     "email": "arun.second@example.com"},
    {"name": "Unknown Contact", "phone": "",
     "email": "unknown1@example.com"},
    {"name": "Unknown Contact", "phone": None,
     "email": "unknown2@example.com"},
    {"name": "Priya Sharma", "phone": "9876511111",
     "email": "priya.personal@example.com"},
]


def normalize_phone(phone):
    if phone is None:
        return ""

    digits = "".join(
        character for character in str(phone)
        if character.isdigit()
    )

    # Normalize Indian country code when it precedes
    # a ten-digit local phone number.
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    return digits


def normalize_name(name):
    if name is None:
        return ""

    return " ".join(str(name).split()).title()


def normalize_email(email):
    if email is None:
        return ""

    return str(email).strip().lower()


def create_group(phone_key, contact):
    group = {
        "normalized_phone": phone_key,
        "names": set(),
        "phones": set(),
        "emails": set()
    }

    add_contact_to_group(group, contact)
    return group


def add_contact_to_group(group, contact):
    name = normalize_name(contact.get("name"))
    phone = contact.get("phone")
    email = normalize_email(contact.get("email"))

    if name:
        group["names"].add(name)

    if phone is not None and str(phone).strip():
        group["phones"].add(str(phone).strip())

    if email:
        group["emails"].add(email)


def finalize_groups(groups):
    results = []

    for group in groups:
        results.append({
            "normalized_phone": group["normalized_phone"],
            "names": sorted(group["names"]),
            "phones": sorted(group["phones"]),
            "emails": sorted(group["emails"])
        })

    return sorted(
        results,
        key=lambda item: (
            item["normalized_phone"] or "",
            item["names"],
            item["emails"]
        )
    )


def merge_contacts_dictionary(contact_list):
    groups_by_phone = {}
    contacts_without_phone = []

    for contact in contact_list:
        phone_key = normalize_phone(contact.get("phone"))

        if not phone_key:
            contacts_without_phone.append(
                create_group(None, contact)
            )
            continue

        if phone_key not in groups_by_phone:
            groups_by_phone[phone_key] = create_group(
                phone_key, contact
            )
        else:
            add_contact_to_group(
                groups_by_phone[phone_key], contact
            )

    all_groups = list(groups_by_phone.values())
    all_groups.extend(contacts_without_phone)

    return finalize_groups(all_groups)


def merge_contacts_pairwise(contact_list):
    groups = []

    for contact in contact_list:
        phone_key = normalize_phone(contact.get("phone"))

        if not phone_key:
            groups.append(create_group(None, contact))
            continue

        matched_group = None

        for group in groups:
            if group["normalized_phone"] == phone_key:
                matched_group = group
                break

        if matched_group is None:
            groups.append(create_group(phone_key, contact))
        else:
            add_contact_to_group(matched_group, contact)

    return finalize_groups(groups)


def display_contacts(merged_contacts):
    for number, contact in enumerate(merged_contacts, start=1):
        print(f"\nContact {number}")
        print("Normalized phone:",
              contact["normalized_phone"] or "Missing")
        print("Names:", contact["names"] or ["Not provided"])
        print("Phone formats:", contact["phones"] or ["Not provided"])
        print("Emails:", contact["emails"] or ["Not provided"])


def generate_contacts(number_of_contacts):
    generated = []

    for i in range(number_of_contacts):
        phone_group = i // 2
        local_number = f"90000{phone_group:05d}"

        if i % 2 == 0:
            phone = "+91 " + local_number
        else:
            phone = local_number

        generated.append({
            "name": f"Contact {i + 1}",
            "phone": phone,
            "email": f"person{i + 1}@example.com"
        })

    return generated


def performance_experiment():
    print("\nPERFORMANCE COMPARISON")
    print("=" * 75)
    print(f"{'Contacts':>12} {'Dictionary (s)':>18} "
          f"{'Pairwise (s)':>18} {'Results match':>18}")
    print("-" * 75)

    for size in [1000, 100000]:
        data = generate_contacts(size)

        start = time.perf_counter()
        dictionary_result = merge_contacts_dictionary(data)
        dictionary_time = time.perf_counter() - start

        if size == 1000:
            start = time.perf_counter()
            pairwise_result = merge_contacts_pairwise(data)
            pairwise_time = time.perf_counter() - start

            matches = dictionary_result == pairwise_result

            print(f"{size:>12,} {dictionary_time:>18.6f} "
                  f"{pairwise_time:>18.6f} {str(matches):>18}")

            assert matches
        else:
            print(f"{size:>12,} {dictionary_time:>18.6f} "
                  f"{'Skipped (O(n^2))':>18} {'N/A':>18}")

        assert len(dictionary_result) == (size + 1) // 2

    print("\nDictionary merging passed both scalability checks.")


def run_tests():
    print("\nCORRECTNESS AND EDGE-CASE TESTS")
    print("-" * 55)

    assert merge_contacts_dictionary([]) == []
    print("Empty contact list: PASS")

    formatted = [
        {"name": "Alex", "phone": "+91 98400 12345",
         "email": "ALEX@example.com"},
        {"name": "Alex", "phone": "9840012345",
         "email": "alex@example.com"}
    ]

    merged = merge_contacts_dictionary(formatted)

    assert len(merged) == 1
    assert merged[0]["normalized_phone"] == "9840012345"
    assert len(merged[0]["emails"]) == 1
    print("Country code and phone-format normalization: PASS")

    assert normalize_name("  aLEX   kUMAR ") == "Alex Kumar"
    assert normalize_email(" ALEX@Example.COM ") == "alex@example.com"
    print("Name and email normalization: PASS")

    duplicates = [
        {"name": "Ravi", "phone": "12345",
         "email": "ravi@example.com"},
        {"name": "RAVI", "phone": "12345",
         "email": "RAVI@example.com"}
    ]

    merged = merge_contacts_dictionary(duplicates)

    assert len(merged) == 1
    assert merged[0]["names"] == ["Ravi"]
    assert merged[0]["emails"] == ["ravi@example.com"]
    print("Duplicate merging and set-based deduplication: PASS")

    same_name = [
        {"name": "Sam", "phone": "11111",
         "email": "sam1@example.com"},
        {"name": "Sam", "phone": "22222",
         "email": "sam2@example.com"}
    ]

    assert len(merge_contacts_dictionary(same_name)) == 2
    print("Same name with different phone numbers: PASS")

    missing = [
        {"name": "Taylor", "phone": None,
         "email": "t1@example.com"},
        {"name": "Taylor", "phone": "",
         "email": "t2@example.com"}
    ]

    assert len(merge_contacts_dictionary(missing)) == 2
    print("Missing phone numbers remain separate: PASS")

    incomplete = [
        {"name": None, "phone": "33333", "email": None},
        {"name": "Morgan", "phone": "33333", "email": ""}
    ]

    merged = merge_contacts_dictionary(incomplete)

    assert len(merged) == 1
    assert merged[0]["names"] == ["Morgan"]
    assert merged[0]["emails"] == []
    print("Missing name and email fields: PASS")

    small_data = generate_contacts(100)

    assert (
        merge_contacts_dictionary(small_data)
        == merge_contacts_pairwise(small_data)
    )
    print("Dictionary vs pairwise results: PASS")

    print("\nAll Task 7 correctness tests passed!")


def main():
    print("CONTACT MERGING AND DUPLICATE DETECTION")
    print("=" * 65)

    print("\nORIGINAL CONTACTS")
    for contact in contacts:
        print(contact)

    merged = merge_contacts_dictionary(contacts)

    print("\nMERGED CONTACTS")
    display_contacts(merged)

    print("\nSUMMARY")
    print("Original contact records:", len(contacts))
    print("Merged contact groups:", len(merged))
    print("Duplicate records combined:", len(contacts) - len(merged))

    run_tests()
    performance_experiment()


if __name__ == "__main__":
    main()