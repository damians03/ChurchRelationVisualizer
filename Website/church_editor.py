import json
import os


DATA_FILE = "church_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"churches": [], "relationships": []}

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("\nSaved successfully.\n")


def find_church(data, church_id):
    for church in data["churches"]:
        if church["id"] == church_id:
            return church
    return None


def list_churches(data):
    print("\nChurches:")
    print("-" * 50)

    for church in data["churches"]:
        print(
            f'{church["id"]}: {church["name"]} '
            f'({church["tradition"]}, {church["members"]:,} members)'
        )

    print()


def add_church(data):
    print("\nAdd Church")

    church_id = input("ID: ").lower().strip()

    if find_church(data, church_id):
        print("That ID already exists.")
        return

    traditions = [
        "Catholic",
        "Eastern Orthodox",
        "Oriental Orthodox",
        "Church of the East",
        "Anglican",
        "Lutheran",
        "Methodist",
        "Baptist",
        "Dutch Reformed",
        "Presbyterian",
        "Congregationalist",
        "Anabaptist",
        "Pentecostal",
        "Restorationist",
        "Non-Denominational",
        "Adventist"
    ]

    print("\nTraditions:")
    for i, tradition in enumerate(traditions, 1):
        print(f"{i}. {tradition}")

    while True:
        try:
            choice = int(input("Select tradition: "))
            if 1 <= choice <= len(traditions):
                tradition = traditions[choice - 1]
                break
            else:
                print("Invalid selection.")
        except ValueError:
            print("Enter a number.")

    church = {
        "id": church_id,
        "name": input("Name: "),
        "tradition": tradition,
        "members": int(input("Members: "))
    }

    data["churches"].append(church)
    save_data(data)

    print(f"Added {church['name']} ({tradition})")


def remove_church(data):
    church_id = input("Church ID to remove: ").lower()

    church = find_church(data, church_id)

    if not church:
        print("Church not found.")
        return

    data["churches"].remove(church)

    # remove relationships involving church
    data["relationships"] = [
        r for r in data["relationships"]
        if r["source"] != church_id and r["target"] != church_id
    ]

    save_data(data)


def list_relationships(data):
    print("\nRelationships:")
    print("-" * 60)

    for r in data["relationships"]:
        print(
            f'{r["source"]} -> {r["target"]}: '
            f'{r["relationship"]} ({r["strength"]})'
        )

    print()


def add_relationship(data):
    print("\nAdd Relationship")

    source = input("Source church ID: ").lower()
    target = input("Target church ID: ").lower()

    if not find_church(data, source):
        print("Source church does not exist.")
        return

    if not find_church(data, target):
        print("Target church does not exist.")
        return

    print("""
    Relationship types:
    10 - Full Communion
    5  - Recognition
    3  - Cooperation
    1  - Separation
    0  - Condemnation
    """)

    relationship_types = {
        10: "Full Communion",
        5: "Recognition",
        3: "Cooperation",
        1: "Separation",
        0: "Condemnation"
    }

    strength = int(input("Strength: "))

    if strength in relationship_types:
        relationship = relationship_types[strength]
    else:
        print("Invalid strength. Please use one of the listed values.")
        return

    data["relationships"].append({
        "source": source,
        "target": target,
        "relationship": relationship,
        "strength": strength
    })

    save_data(data)


def remove_relationship(data):
    list_relationships(data)

    source = input("Source ID: ")
    target = input("Target ID: ")

    before = len(data["relationships"])

    data["relationships"] = [
        r for r in data["relationships"]
        if not (
            r["source"] == source and
            r["target"] == target
        )
    ]

    if len(data["relationships"]) < before:
        save_data(data)
    else:
        print("Relationship not found.")


def menu():
    data = load_data()

    while True:
        print("""
==============================
 Church Relationship Editor
==============================

1. List churches
2. Add church
3. Remove church

4. List relationships
5. Add relationship
6. Remove relationship

7. Exit
""")

        choice = input("> ")

        if choice == "1":
            list_churches(data)

        elif choice == "2":
            add_church(data)

        elif choice == "3":
            remove_church(data)

        elif choice == "4":
            list_relationships(data)

        elif choice == "5":
            add_relationship(data)

        elif choice == "6":
            remove_relationship(data)

        elif choice == "7":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    menu()