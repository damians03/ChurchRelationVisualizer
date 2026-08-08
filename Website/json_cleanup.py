import json

INPUT_FILE = "church_data.json"
OUTPUT_FILE = "church_data_clean.json"

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

seen = set()
clean_relationships = []
duplicates = 0

for relationship in data["relationships"]:
    source = relationship["source"]
    target = relationship["target"]

    # Treat A → B and B → A as the same relationship
    edge = frozenset([source, target])

    if edge in seen:
        duplicates += 1
        continue

    seen.add(edge)
    clean_relationships.append(relationship)

data["relationships"] = clean_relationships

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)

print(f"Removed {duplicates} duplicate relationships.")
print(f"Saved cleaned data to {OUTPUT_FILE}")