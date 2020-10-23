from shapely.geometry import LineString
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
from matplotlib import cm
from itertools import combinations
import matplotlib.pyplot as plt
import numpy as np
from geopy import distance
from scipy.sparse.csgraph import dijkstra


class Edge:
    def __init__(self, start, end, figure=None):
        self.start, self.end = start, end
        self.line = LineString([start, end])
        self.figure = figure

    def intersects_with(self, other_line: tuple):
        if self.figure and all(p in self.figure for p in other_line) and self.figure.crosses(other_line):
            return True
        return self.line.crosses(LineString(other_line))


class Polygon:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color
        self.edges = [Edge(*e, figure=self) for e in zip(vertices, list(vertices[1:]) + [vertices[0]])]
        self.inner_edges = [Edge(*e, figure=self) for e in combinations(vertices, 2)]
        self.mpl_poly = MplPolygon(
            vertices,
            True,
            color=[1, 0, 0]
        )

    def __contains__(self, item):
        return item in self.vertices

    def crosses(self, item):
        item = LineString(item)
        return any(item.crosses(e.line) for e in self.inner_edges)

    def __hash__(self):
        return hash(self.vertices)


class Plot:
    def __init__(self, img, obstacles, targets, box):
        self.img, self.obstacles, self.targets, self.box = img, obstacles, targets, box
        self.plot = plt.imread('data/map.png')

        self.fig, self.ax = plt.subplots()

        patches = [polygon.mpl_poly for polygon in self.obstacles]

        p = PatchCollection(patches, cmap=cm.jet, alpha=0.4, match_original=True)

        self.ax.add_collection(p)

        plt.scatter([t[0] for t in targets], [t[1] for t in targets], marker="o")

        plt.imshow(self.plot, zorder=0, extent=box, aspect='auto')

    def show(self):
        plt.show()


class Data:
    def __init__(self, targets: [tuple], obstacles: [Polygon], plot: Plot):
        self.targets = targets
        self.obstacles = obstacles
        self.plot = plot

        self.vis_edges = []

        self.edges_set = []
        points = [*targets]

        self.T = len(targets)

        for pol in self.obstacles:
            self.edges_set.extend(pol.edges)
            points.extend(pol.vertices)

        D = np.full((len(points), len(points)), np.inf)

        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points):
                if i == j:
                    continue
                if not any(e.intersects_with((p1, p2)) for e in self.edges_set):
                    self.vis_edges.append(Edge(p1, p2))
                    plot.ax.plot([p1[0], p2[0]], [p1[1], p2[1]], linestyle=':', linewidth=1, color='green')
                    D[i][j] = distance.distance(p1, p2).m

        cur_point = 0

        dist_matrix, predecessors = dijkstra(csgraph=D, directed=False, indices=list(range(self.T)), return_predecessors=True)

        for t1, t2 in combinations(range(self.T), 2):
            back_track_id = t2
            path = [targets[t2]]
            while True:
                back_track_id = predecessors[t1][back_track_id]
                path.append(points[back_track_id])
                if back_track_id == t1:
                    break

            plot.ax.plot([p[0] for p in path], [p[1] for p in path], linewidth=2, color='orange')
