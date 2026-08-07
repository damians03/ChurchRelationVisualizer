import json
import networkx as nx


INPUT_FILE = "church_data.json"
OUTPUT_FILE = "church_network.gexf"


# Load JSON data
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)


# Create graph
G = nx.Graph()


# Add churches (nodes)
for church in data["churches"]:
    G.add_node(
        church["id"],
        label=church["name"],
        tradition=church["tradition"],
        members=church["members"]
    )


# Add relationships (edges)
for relationship in data["relationships"]:
    G.add_edge(
        relationship["source"],
        relationship["target"],
        weight=relationship["strength"],
        relationship=relationship["relationship"]
    )


# Export to GEXF
nx.write_gexf(G, OUTPUT_FILE)

print(f"Created {OUTPUT_FILE}")