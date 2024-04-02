# -*- coding: utf-8 -*-

"""The expander use the DAG to generate curve by topological order."""

import inspect

__nodes = {}


def reg_node(func):
    name = func.__name__
    assert name not in __nodes, f"Node {name} already exists."

    sig = inspect.signature(func)
    __nodes[name] = {
        "deps": list(sig.parameters.keys()),
        "processor": func,
        "curve": None,
    }

    return func


def all_nodes():
    return __nodes


def get_processor(name):
    return __nodes[name]["processor"]


def get_curve(name):
    return __nodes[name]["curve"]


def get_deps(name):
    return __nodes[name]["deps"]


def get_node(name):
    return __nodes[name]


class DAG:
    """Directed Acyclic Graph."""

    def __init__(self):
        self._vertices = []
        self._edges = []

        self._depend = {}
        self._depended = {}

    def _valid_vertex(self, *vertices):
        for vtx in vertices:
            if vtx not in self._vertices:
                raise ValueError(f"vertex {vtx} does not belong to DAG.")

    def add_vertex(self, vertex):
        self._vertices.append(vertex)

    def vertices(self):
        return self._vertices

    def add_edge(self, v_from, *v_tos):
        self._valid_vertex(v_from, *v_tos)
        for v_to in v_tos:
            self._edges.append((v_from, v_to))
            self._depend[v_from] = self._depend.setdefault(v_from, []) + [v_to]
            self._depended[v_to] = self._depended.setdefault(v_to, []) + [v_from]

    def get_depended(self, vertex):
        return self._depended.get(vertex, [])

    def get_predecessors(self, vertex):
        return self._depend.get(vertex, [])

    def indegree(self, vertex):
        return len(self.get_predecessors(vertex))

    def all_starts(self):
        res = []
        for vtx in self._vertices:
            if self.indegree(vtx) == 0:
                res.append(vtx)
        return res


class Expander:
    def __init__(self, dag: DAG):
        self.dag = dag

    def execute(self):
        """Execute in topological order.

        TODO: async and parallel
        """

        indegree_dict = {}
        for vtx in self.dag.vertices():
            indegree_dict[vtx] = self.dag.indegree(vtx)

        zero_indgrees = self.dag.all_starts()

        while zero_indgrees:
            vtx = zero_indgrees.pop(0)
            # use predecessors as arguments
            deps = get_deps(vtx)
            pres = self.dag.get_predecessors(vtx)
            assert len(deps) == len(
                pres
            ), f"deps: {deps} and pres: {pres} should be the same."
            cs = [None] * len(pres)
            for pre in pres:
                cs[deps.index(pre)] = get_curve(pre)
            get_node(vtx)["curve"] = get_processor(vtx)(*cs)

            for vtx in self.dag.get_depended(vtx):
                indegree_dict[vtx] -= 1
                if indegree_dict[vtx] == 0:
                    zero_indgrees.append(vtx)
