import networkx as nx

churches = [
    ("catholic", "Roman Catholic Church", "Catholic", 1300000000, "200,50,50"),
    ("orthodox", "Eastern Orthodox Church", "Orthodox", 220000000, "50,100,200"),

    ("anglican", "Anglican Communion", "Anglican", 85000000, "120,80,200"),
    ("episcopal", "Episcopal Church", "Anglican", 1500000, "120,80,200"),

    ("pcusa", "Presbyterian Church (USA)", "Reformed", 1100000, "50,180,100"),
    ("pca", "Presbyterian Church in America", "Reformed", 400000, "50,180,100"),
    ("crcna", "Christian Reformed Church", "Reformed", 200000, "50,180,100"),

    ("elca", "Evangelical Lutheran Church in America", "Lutheran", 3000000, "230,170,50"),
    ("lcms", "Lutheran Church Missouri Synod", "Lutheran", 1800000, "230,170,50"),
    ("wels", "Wisconsin Evangelical Lutheran Synod", "Lutheran", 350000, "230,170,50"),

    ("umc", "United Methodist Church", "Methodist", 6000000, "240,140,40"),
    ("wesleyan", "Wesleyan Church", "Methodist", 150000, "240,140,40"),
    ("nazarene", "Church of the Nazarene", "Methodist", 700000, "240,140,40"),

    ("sbc", "Southern Baptist Convention", "Baptist", 13000000, "220,80,80"),
    ("abcusa", "American Baptist Churches USA", "Baptist", 1200000, "220,80,80"),
    ("converge", "Converge Worldwide", "Baptist", 350000, "220,80,80"),

    ("disciples", "Christian Church (Disciples of Christ)", "Restorationist", 300000, "40,180,170"),
    ("churchchrist", "Churches of Christ", "Restorationist", 500000, "40,180,170"),

    ("cma", "Christian and Missionary Alliance", "Evangelical", 600000, "120,120,120"),
    ("nondenom", "Non-Denominational Evangelical", "Evangelical", 40000000, "120,120,120"),
]

edges = [
    ("catholic", "orthodox", "Historical split"),
    ("catholic", "anglican", "Dialogue"),

    ("anglican", "episcopal", "Member relationship"),
    ("episcopal", "elca", "Full communion"),
    ("episcopal", "pcusa", "Full communion"),

    ("pcusa", "pca", "Reformed family"),
    ("pcusa", "crcna", "Reformed family"),

    ("elca", "lcms", "Lutheran family"),
    ("lcms", "wels", "Lutheran family"),

    ("umc", "wesleyan", "Wesleyan heritage"),
    ("umc", "nazarene", "Wesleyan heritage"),

    ("sbc", "abcusa", "Baptist family"),
    ("sbc", "converge", "Baptist family"),

    ("disciples", "churchchrist", "Restorationist heritage"),

    ("sbc", "nondenom", "Evangelical relationship"),
    ("cma", "nondenom", "Evangelical relationship"),

    ("umc", "elca", "Ecumenical relationship"),
    ("pcusa", "elca", "Ecumenical relationship"),
]


G = nx.Graph()

for cid, name, tradition, members, color in churches:
    size = max(5, members / 500000)

    G.add_node(
        cid,
        label=name,
        tradition=tradition,
        members=members,
        color=color,
        size=size
    )


for source, target, relationship in edges:
    G.add_edge(
        source,
        target,
        relationship=relationship
    )


nx.write_gexf(G, "church_network.gexf")

print("Created church_network.gexf")