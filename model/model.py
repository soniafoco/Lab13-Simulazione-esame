import copy
import networkx as nx
from geopy import distance
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._states = DAO.getAllStates()
        self._idMap = {}
        for state in self._states:
            self._idMap[state.id] = state

    def getShapes(self, anno):
        return DAO.getShapes(anno)

    def buildGraph(self, anno, forma):
        self._graph.clear()
        self._graph.add_nodes_from(self._states)

        neighbors = DAO.getNeighbors()
        for neighbor in neighbors:
            state1 = self._idMap[neighbor[0]]
            state2 = self._idMap[neighbor[1]]
            peso = DAO.getPeso(neighbor[0], anno, forma)+DAO.getPeso(neighbor[1], anno, forma)
            self._graph.add_edge(state1, state2, weight=peso)

    def getDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getVicini(self):
        result = []
        for node in self._graph.nodes:
            vicini = nx.neighbors(self._graph, node)
            sum = 0
            for vicino in vicini:
                sum += self._graph[node][vicino]["weight"]
            result.append((node, sum))

        return result


    def getPercorso(self):

        self._solBest = []
        self._bestScore = 0

        parziale = []

        for node in self._graph.nodes:
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestScore, self._solution(self._solBest)


    def _ricorsione(self, parziale):

        score = self._score(parziale)
        if score > self._bestScore:
            self._bestScore = score
            self._solBest = copy.deepcopy(parziale)

        for node in nx.neighbors(self._graph, parziale[-1]):
            if node not in parziale:
                if (len(parziale)>1 and self._graph[node][parziale[-1]]["weight"] > self._graph[parziale[-2]][parziale[-1]]["weight"]) or len(parziale)<=1:
                    parziale.append(node)
                    self._ricorsione(parziale)
                    parziale.pop()

    def _score(self, list):
        dist = 0
        for i in range(len(list)-1):
            coord1 = (list[i].Lat, list[i].Lng)
            coord2 = (list[i+1].Lat, list[i+1].Lng)
            dist += distance.distance(coord1, coord2).km
        return dist

    def _solution(self, list):
        result = []
        for i in range(len(list)-1):
            coord1 = (list[i].Lat, list[i].Lng)
            coord2 = (list[i+1].Lat, list[i+1].Lng)
            dist = distance.distance(coord1, coord2).km
            peso = self._graph[list[i]][list[i+1]]["weight"]
            result.append((list[i].id, list[i+1].id, peso, dist))

        return result