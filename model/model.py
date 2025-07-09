import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMap = {}

    def getStores(self):
        return DAO.getAllStores()

    def buildGraph(self, store, k):

        self._graph.clear()
        self._orders = DAO.getAllOrdersByStores(store)
        for order in self._orders:
            self._idMap[order.order_id] = order

        self._graph.add_nodes_from(self._orders)

        allEdges = DAO.getAllEdges(store, k, self._idMap)
        for edge in allEdges:
            self._graph.add_edge(edge[0], edge[1], weight=edge[2])

    def getAllNodes(self):
        nodes = list(self._graph.nodes())
        return nodes

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getCammino(self, sourceStr):
        source = self._idMap[int(sourceStr)]
        lp = []

        #for source in self._graph.nodes:
        tree = nx.dfs_tree(self._graph, source)
        nodi = list(tree.nodes())

        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp