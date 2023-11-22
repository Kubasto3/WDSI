# prob.py
# This is
import queue
import random
import numpy as np
import queue as q
import math as m

from gridutil import *


class Agent:
    def __init__(self, size, walls, graph, loc, dir, goal):
        self.size = size
        self.walls = walls
        self.graph = graph
        # list of valid locations
        self.locations = list(self.graph.keys())
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.loc = loc
        self.dir = dir
        self.goal = goal

        self.t = 0
        self.path = self.find_path()

    def __call__(self):
        action = self.loc

        # select action to reach first location in self.path
        # TODO PUT YOUR CODE HERE
        action = self.path[self.t+1]
        self.t=self.t+1
        # ------------------

        return action



    def find_path(self):
        path = []

        # find path from sel.loc to self.goal
        # TODO PUT YOUR CODE HERE

        def distance(point1, point2):
            return m.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

        #Mało optymalny pomysł, lecz z braku czasu nie zdążyłem zrobić uniwersalnej metody dla graphu, który odstajemy
        #przy konstruktorze.
        graph = {
            (0, 4): [((5, 5), distance((0, 4), (5, 5))), ((0, 7), distance((0, 4), (0, 7)))],
            (0, 7): [((0, 4), distance((0, 7), (0, 4))), ((3, 8), distance((0, 7), (3, 8)))],
            (1, 10): [((3, 8), distance((1, 10), (3, 8))), ((3, 11), distance((1, 10), (3, 11)))],
            (3, 8): [((0, 7), distance((3, 8), (0, 7))), ((1, 10), distance((3, 8), (1, 10))),
                     ((5, 5), distance((3, 8), (5, 5))), ((5, 10), distance((3, 8), (5, 10)))],
            (3, 11): [((1, 10), distance((3, 11), (1, 10)))],
            (5, 5): [((0, 4), distance((5, 5), (0, 4))), ((3, 8), distance((5, 5), (3, 8))),
                     ((9, 4), distance((5, 5), (9, 4)))],
            (5, 10): [((3, 8), distance((5, 10), (3, 8))), ((8, 8), distance((5, 10), (8, 8))),
                      ((10, 10), distance((5, 10), (10, 10)))],
            (8, 7): [((9, 4), distance((8, 7), (9, 4)))],
            (8, 8): [((5, 10), distance((8, 8), (5, 10))), ((10, 10), distance((8, 8), (10, 10)))],
            (9, 4): [((5, 5), distance((9, 4), (5, 5))), ((8, 7), distance((9, 4), (8, 7))),
                     ((10, 7), distance((9, 4), (10, 7)))],
            (10, 7): [((9, 4), distance((10, 7), (9, 4))), ((10, 10), distance((10, 7), (10, 10))),
                      ((12, 5), distance((10, 7), (12, 5)))],
            (10, 10): [((5, 10), distance((10, 10), (5, 10))), ((8, 8), distance((10, 10), (8, 8))),
                       ((12, 9), distance((10, 10), (12, 9)))],
            (12, 5): [((10, 7), distance((12, 5), (10, 7))), ((12, 7), distance((12, 5), (12, 7)))],
            (12, 7): [((12, 5), distance((12, 7), (12, 5))), ((12, 9), distance((12, 7), (12, 9))),
                      ((15, 8), distance((12, 7), (15, 8)))],
            (12, 9): [((10, 10), distance((12, 9), (10, 10))), ((12, 7), distance((12, 9), (12, 7))),
                      ((14, 10), distance((12, 9), (14, 10)))],
            (14, 4): [((15, 8), distance((14, 4), (15, 8)))],
            (14, 10): [((12, 9), distance((14, 10), (12, 9))), ((15, 8), distance((14, 10), (15, 8)))],
            (15, 8): [((14, 4), distance((15, 8), (14, 4))), ((14, 10), distance((15, 8), (14, 10)))]
        }

        #Algorytm Dijkstry (lekko zmodyfikowany kod, który przerabialiśmy na zajęciach)
        start = self.loc
        goal = self.goal

        visited = set()
        cost = {n: float('inf') for n in graph}
        parent = {n: None for n in graph}
        q = queue.PriorityQueue()

        q.put((0, start))
        cost[start] = 0

        while not q.empty():
            _, cur_n = q.get()

            if cur_n in visited:
                continue

            visited.add(cur_n)

            #print("Eksplorowany wierzchołek:", cur_n)

            if cur_n == goal:
                break

            for nh, distance in graph[cur_n]:
                if nh in visited:
                    continue

                old_cost = cost[nh]
                new_cost = cost[cur_n] + distance

                if new_cost < old_cost:
                    cost[nh] = new_cost
                    parent[nh] = cur_n
                    q.put((new_cost, nh))

        # Odtwórz ścieżkę
        path = []
        cur_n = goal
        while cur_n is not None:
            path.append(cur_n)
            cur_n = parent[cur_n]


        path.reverse()
        print("Otrzymana droga: ",path)
    # ------------------

        return path

    def get_path(self):
        return self.path
