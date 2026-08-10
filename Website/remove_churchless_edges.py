import json

INPUT_FILE = "church_data_25.json"
OUTPUT_FILE = "church_data_v2_clean.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# --------------------------------------------------
# Get valid church IDs
# --------------------------------------------------

valid_church_ids = {
    church["id"]
    for church in data["churches"]
}

# --------------------------------------------------
# Remove relationships with missing churches
# --------------------------------------------------

clean_relationships = []
removed_relationships = 0

for relationship in data["relationships"]:
    source = relationship["source"]
    target = relationship["target"]

    if source not in valid_church_ids or target not in valid_church_ids:
        removed_relationships += 1
        continue

    clean_relationships.append(relationship)

data["relationships"] = clean_relationships

# --------------------------------------------------
# Save cleaned data
# --------------------------------------------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Removed {removed_relationships} relationships with missing churches.")
print(f"Remaining relationships: {len(clean_relationships)}")
print(f"Saved cleaned data to {OUTPUT_FILE}")