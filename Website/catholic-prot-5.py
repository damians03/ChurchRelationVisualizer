import json

INPUT_FILE = "church_data_25.json"
OUTPUT_FILE = "church_data_25.json"

# --------------------------------------------------
# Catholic and Orthodox traditions
# --------------------------------------------------

SOURCE_TRADITIONS = {
    "Catholic",
    "Eastern Orthodox",
    "Oriental Orthodox",
    "Church of the East"
}

# --------------------------------------------------
# Protestant traditions to connect to
# --------------------------------------------------

TARGET_TRADITIONS = {
    "Lutheran",
    "Anglican",
    "Methodist",
    "Reformed",
    "Dutch Reformed",
    "Presbyterian",
    "Baptist",
}

# --------------------------------------------------
# Load data
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

churches = data["churches"]
relationships = data.get("relationships", [])

# --------------------------------------------------
# Find Catholic and Orthodox churches
# --------------------------------------------------

source_churches = [
    church
    for church in churches
    if church.get("tradition") in SOURCE_TRADITIONS
]

print(f"Found {len(source_churches)} Catholic/Orthodox churches.")

# --------------------------------------------------
# Find Protestant churches
# --------------------------------------------------

target_churches = [
    church
    for church in churches
    if church.get("tradition") in TARGET_TRADITIONS
]

print(f"Found {len(target_churches)} Protestant churches.")

# --------------------------------------------------
# Existing relationships
# --------------------------------------------------

existing_edges = {
    frozenset([relationship["source"], relationship["target"]])
    for relationship in relationships
}

# --------------------------------------------------
# Add strength-5 relationships
# --------------------------------------------------

added = 0

for source_church in source_churches:
    for target_church in target_churches:

        source = source_church["id"]
        target = target_church["id"]

        edge = frozenset([source, target])

        # Don't create a duplicate if any relationship already exists
        if edge in existing_edges:
            continue

        relationships.append({
            "source": source,
            "target": target,
            "strength": 5
        })

        existing_edges.add(edge)
        added += 1

# --------------------------------------------------
# Save
# --------------------------------------------------

data["relationships"] = relationships

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Added {added} Catholic/Orthodox-Protestant relationships at strength 5.")
print(f"Saved to {OUTPUT_FILE}")