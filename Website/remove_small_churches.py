import json

INPUT_FILE = "church_data.json"
OUTPUT_FILE = "church_data_filtered.json"

# Change this to whatever minimum membership you want.
MIN_MEMBERS = 100000

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# Find churches below the membership threshold
removed_ids = {
    church["id"]
    for church in data["churches"]
    if church.get("members", 0) < MIN_MEMBERS
}

# Remove those churches
original_church_count = len(data["churches"])

data["churches"] = [
    church
    for church in data["churches"]
    if church["id"] not in removed_ids
]

# Remove relationships connected to removed churches
original_relationship_count = len(data["relationships"])

data["relationships"] = [
    relationship
    for relationship in data["relationships"]
    if relationship["source"] not in removed_ids
    and relationship["target"] not in removed_ids
]

removed_churches = original_church_count - len(data["churches"])
removed_relationships = original_relationship_count - len(data["relationships"])

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Minimum membership: {MIN_MEMBERS:,}")
print(f"Removed {removed_churches} churches.")
print(f"Removed {removed_relationships} relationships.")
print(f"Saved filtered data to {OUTPUT_FILE}")