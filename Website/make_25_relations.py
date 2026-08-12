import json
from itertools import combinations

INPUT_FILE = "church_data_25.json"
OUTPUT_FILE = "church_data_25.json"

# --------------------------------------------------
# Protestant traditions to include
# --------------------------------------------------

PROTESTANT_TRADITIONS = {
    "Lutheran",
    "Anglican",
    "Methodist",
    "Reformed",
    "Dutch Reformed",
    "Presbyterian",
    "Baptist",
    "Pentecostal",
    "Congregationalist",
    "Anabaptist",
    "Moravian",
    "Adventist",
    "Restorationist",
}

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# --------------------------------------------------
# Find Protestant churches
# --------------------------------------------------

protestant_churches = [
    church
    for church in data["churches"]
    if church.get("tradition") in PROTESTANT_TRADITIONS
]

print(f"Found {len(protestant_churches)} Protestant churches.")

# --------------------------------------------------
# Existing relationships
# --------------------------------------------------

relationships = data.get("relationships", [])

# Store existing edges so we don't create duplicates
existing_edges = {
    frozenset([relationship["source"], relationship["target"]])
    for relationship in relationships
}

# --------------------------------------------------
# Generate 25-strength relationships
# --------------------------------------------------

added = 0

for church_a, church_b in combinations(protestant_churches, 2):

    source = church_a["id"]
    target = church_b["id"]

    edge = frozenset([source, target])

    # Don't overwrite an existing relationship
    if edge in existing_edges:
        continue

    relationships.append({
        "source": source,
        "target": target,
        "strength": 25
    })

    existing_edges.add(edge)
    added += 1

data["relationships"] = relationships

# --------------------------------------------------
# Save
# --------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Added {added} Protestant relationships at strength 25.")
print(f"Saved to {OUTPUT_FILE}")