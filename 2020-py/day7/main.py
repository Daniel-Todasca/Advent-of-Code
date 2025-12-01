from src.helper import IO
import re
import sys


class Graph:
    def __init__(self):
        self.p_edges = {}
        self.n_edges = {}
        self.weights = {}

    def add_nodes(self, *args):
        for x in args:
            if x not in self.p_edges:
                self.p_edges[x] = []
            if x not in self.n_edges:
                self.n_edges[x] = []

    def add(self, src, to, weight):
        self.weights[(src, to)] = weight

        self.add_nodes(src, to)

        self.p_edges[src].append(to)
        self.n_edges[to].append(src)

    def get_callees(self, node):
        ans = {node}

        for to in self.n_edges[node]:
            ans.update(self.get_callees(to))
        return ans

    def get_weight(self, node):
        ans = 1
        for to in self.p_edges[node]:
            ans += self.weights[(node, to)] * self.get_weight(to)
        return ans


def format_bag_string(bag):
    return bag.replace("bags", "").replace("bag", "").strip()


sys.setrecursionlimit(4000)


def build_graph():
    ans = Graph()
    for line in IO.read_all():
        match = re.match(r"(.+) contain (.+)", line)
        parent_group = match.group(1)

        child_group = match.group(2)
        if "no other bag" in child_group:
            continue
        bag_matches = re.findall(r"((\d+) ([\w\s]+))[,.]", child_group)
        for bag in bag_matches:
            weight = int(bag[1])
            ans.add(format_bag_string(parent_group), format_bag_string(bag[2]), weight)
    return ans


graph = build_graph()
IO.write(len(graph.get_callees("shiny gold"))-1)
IO.write(graph.get_weight("shiny gold")-1)
