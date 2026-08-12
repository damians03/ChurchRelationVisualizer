import json
from itertools import combinations

INPUT_FILE = "church_data_25.json"
OUTPUT_FILE = "church_data_25.json"

# --------------------------------------------------
# Traditions to connect
# --------------------------------------------------

TRUE_CHURCH_TRADITIONS = {
    "Catholic",
    "Oriental Orthodox",
    "Eastern Orthodox",
}

TRUE_CHURCH_STRENGTH = 25

# --------------------------------------------------
# Load data
# --------------------------------------------------

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

churches = data["churches"]
relationships = data.get("relationships", [])

# --------------------------------------------------
# Find Catholic / Orthodox churches
# --------------------------------------------------

true_churches = [
    church
    for church in churches
    if church.get("tradition") in TRUE_CHURCH_TRADITIONS
]

print(f"Found {len(true_churches)} churches.")

# --------------------------------------------------
# Existing relationships
# --------------------------------------------------

existing_edges = {
    frozenset([relationship["source"], relationship["target"]])
    for relationship in relationships
}

# --------------------------------------------------
# Create True Church relationships
# --------------------------------------------------

added = 0

for church_a, church_b in combinations(true_churches, 2):

    source = church_a["id"]
    target = church_b["id"]

    edge = frozenset([source, target])

    # Don't duplicate an existing relationship
    if edge in existing_edges:
        continue

    relationships.append({
        "source": source,
        "target": target,
        "strength": TRUE_CHURCH_STRENGTH,
        "type": "True Church"
    })

    existing_edges.add(edge)
    added += 1

# --------------------------------------------------
# Save
# --------------------------------------------------

data["relationships"] = relationships

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Added {added} True Church relationships at strength 25.")
print(f"Saved to {OUTPUT_FILE}")