import json
import math
import networkx as nx

INPUT_FILE = "church_data_clean.json"
OUTPUT_FILE = "church_network.gexf"

# Load JSON data
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

# Create graph
G = nx.Graph()

# Store membership by church ID
members = {}

# Add churches (nodes)
for church in data["churches"]:
    members[church["id"]] = church["members"]

    G.add_node(
        church["id"],
        label=church["name"],
        tradition=church["tradition"],
        members=church["members"]
    )

# Add relationships (edges)
for relationship in data["relationships"]:
    source = relationship["source"]
    target = relationship["target"]
    strength = relationship["strength"]

    # Combined membership, with logarithmic scaling
    combined_members = members[source] + members[target]
    weight = (strength * math.log10(combined_members + 1))/1000 #*log(members) to account for split nodes

    G.add_edge(
        source,
        target,
        strength=strength,
        weight=weight
    )

# Export to GEXF
nx.write_gexf(G, OUTPUT_FILE)

print(f"Created {OUTPUT_FILE}")