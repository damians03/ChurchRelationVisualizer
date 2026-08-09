import json

INPUT_FILE = "church_data_filtered.json"
OUTPUT_FILE = "church_data_clean.json"


def clean_id(value):
    if isinstance(value, str) and value.startswith("the_"):
        return value[4:]
    return value


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)


# Clean church IDs
for church in data.get("churches", []):
    if "id" in church:
        church["id"] = clean_id(church["id"])


# Clean relationship source/target IDs
for relationship in data.get("relationships", []):
    if "source" in relationship:
        relationship["source"] = clean_id(relationship["source"])

    if "target" in relationship:
        relationship["target"] = clean_id(relationship["target"])


with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)


print(f"Saved cleaned data to {OUTPUT_FILE}")