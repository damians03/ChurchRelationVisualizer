import json
from itertools import combinations

INPUT_FILE = "lwf_churches.json"
OUTPUT_FILE = "lwf_relations.json"


def main():
    # Load church data
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        churches = json.load(f)

    relations = []

    # Create every unique pair
    for church_a, church_b in combinations(churches, 2):
        relations.append({
            "source": church_a["id"],
            "target": church_b["id"],
            "strength": 100
        })

    # Save relations
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=2, ensure_ascii=False)

    print(f"Created {len(relations)} full communion relations.")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()