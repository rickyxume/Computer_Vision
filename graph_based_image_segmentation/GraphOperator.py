import math


class OptimizedUnionFind:
    def __init__(self, num_node):
        self.parent = [i for i in range(num_node)]
        self.rank = [0 for i in range(num_node)]
        self.size = [1 for i in range(num_node)]
        self.num_set = num_node

    def size_of(self, u):
        return self.size[u]

    def find(self, u):
        if self.parent[u] == u:
            return u

        self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def merge(self, u, v):
        u = self.find(u)
        v = self.find(v)

        if u != v:
            if self.rank[u] > self.rank[v]:
                u, v = v, u

            self.parent[u] = v
            self.size[v] += self.size[u]
            if self.rank[u] == self.rank[v]:
                self.rank[v] += 1

            self.num_set -= 1


def get_diff(img, x1, y1, x2, y2):
    r = (img[0][y1, x1] - img[0][y2, x2]) ** 2
    g = (img[1][y1, x1] - img[1][y2, x2]) ** 2
    b = (img[2][y1, x1] - img[2][y2, x2]) ** 2
    return math.sqrt(r + g + b)


def get_threshold(k, size):
    return (k / size)


def create_edge(img, width, x1, y1, x2, y2):
    def vertex_id(x, y): return y * width + x

    w = get_diff(img, x1, y1, x2, y2)
    return (vertex_id(x1, y1), vertex_id(x2, y2), w)


def build_graph(img, width, height):
    graph = []

    for y in range(height):
        for x in range(width):
            if x < width - 1:
                graph.append(create_edge(img, width, x, y, x + 1, y))
            if y < height - 1:
                graph.append(create_edge(img, width, x, y, x, y + 1))
            if x < width - 1 and y < height - 1:
                graph.append(create_edge(img, width, x, y, x + 1, y + 1))
            if x < width - 1 and y > 0:
                graph.append(create_edge(img, width, x, y, x + 1, y - 1))

    return graph


def remove_small_component(ufset, sorted_graph, min_size):
    for edge in sorted_graph:
        u = ufset.find(edge[0])
        v = ufset.find(edge[1])

        if u != v:
            if ufset.size_of(u) < min_size or ufset.size_of(v) < min_size:
                ufset.merge(u, v)

    return ufset


def segment_graph(sorted_graph, num_node, k):
    ufset = OptimizedUnionFind(num_node)
    threshold = [get_threshold(k, 1)] * num_node

    for edge in sorted_graph:
        u = ufset.find(edge[0])
        v = ufset.find(edge[1])
        w = edge[2]

        if u != v:
            if w <= threshold[u] and w <= threshold[v]:
                ufset.merge(u, v)
                parent = ufset.find(u)
                threshold[parent] = w + get_threshold(k, ufset.size_of(parent))

    return ufset
