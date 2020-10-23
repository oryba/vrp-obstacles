from entities import Plot, Polygon, Data

polygons = [
    Polygon(
        vertices=(
            (34.05, 48.825), (33.94, 48.920), (34.11, 48.877), (34.15, 48.815)
        ),
        color=[1, 0, 0]
    ),
    Polygon(
        vertices=(
            (34.10, 48.92), (34.16, 48.94), (34.21, 48.88)
        ),
        color=[1, 0, 0]
    ),
    Polygon(
        vertices=(
            (34.14, 48.87), (34.16, 48.877), (34.24, 48.82)
        ),
        color=[1, 0, 0]
    )
]

targets = [(33.95, 48.8), (34.20, 48.925), (34.05, 48.940), (34.17, 48.774)]

box = ((33.8993, 34.2701,
        48.7587, 48.9545))

plot = Plot(
    obstacles=polygons,
    targets=targets,
    img='data/map.png',
    box=box
)

data = Data(
    targets=targets, obstacles=polygons, plot=plot
)