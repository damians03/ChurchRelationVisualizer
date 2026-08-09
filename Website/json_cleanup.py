import json

INPUT_FILE = "church_data.json"
OUTPUT_FILE = "church_data_clean.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# --------------------------------------------------
# Remove duplicate churches
# --------------------------------------------------

seen_churches = set()
clean_churches = []
duplicate_churches = 0

for church in data["churches"]:
    church_id = church["id"]

    if church_id in seen_churches:
        duplicate_churches += 1
        continue

    seen_churches.add(church_id)
    clean_churches.append(church)

data["churches"] = clean_churches

# --------------------------------------------------
# Remove duplicate relationships
# --------------------------------------------------

seen_relationships = set()
clean_relationships = []
duplicate_relationships = 0

for relationship in data["relationships"]:
    source = relationship["source"]
    target = relationship["target"]

    # Treat A → B and B → A as the same relationship
    edge = frozenset([source, target])

    if edge in seen_relationships:
        duplicate_relationships += 1
        continue

    seen_relationships.add(edge)
    clean_relationships.append(relationship)

data["relationships"] = clean_relationships

# --------------------------------------------------
# Save cleaned data
# --------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Removed {duplicate_churches} duplicate churches.")
print(f"Removed {duplicate_relationships} duplicate relationships.")
print(f"Saved cleaned data to {OUTPUT_FILE}")