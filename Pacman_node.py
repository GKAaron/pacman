import Heuristic as He
import heapq
import math
import copy


class Node:
    def __init__(self, position: tuple,rem: list, eat_order:list, graph: He.Graph, rem_num=0, cost=0, heu=0, parent=None):
        self.position = position
        self.rem = rem
        self.parent = parent
        self.rem_num = rem_num
        self.cost = cost
        self.heu = heu
        self.est = self.cost + self.heu
        self.eat_order = eat_order
        self.graph = graph

    # for Greedy Search
    # def __lt__(self,other):
    #     return self.heu < other.heu
    #
    # def __le__(self,other):
    #     return self.heu <= other.heu
    #
    # def __gt__(self,other):
    #     return self.heu > other.heu
    #
    # def __ge__(self,other):
    #     return self.heu >= other.heu

    # for A* Search
    def __lt__(self,other):
        return self.est < other.est

    def __le__(self,other):
        return self.est <= other.est

    def __gt__(self,other):
        return self.est > other.est

    def __ge__(self,other):
        return self.est >= other.est

    def left(self):
        x = self.position[0]
        y = self.position[1] - 1
        return x, y

    def right(self):
        x = self.position[0]
        y = self.position[1] + 1
        return x, y

    def up(self):
        x = self.position[0] - 1
        y = self.position[1]
        return x, y

    def down(self):
        x = self.position[0] + 1
        y = self.position[1]
        return x, y

    def act(self, maze: list, aim:tuple)->list:
        child = []
        av_pos = [self.left(), self.right(), self.up(), self.down()]
        for x, y in av_pos:
            if (x, y) == aim:
                cur_rem = copy.deepcopy(self.rem)
                eat_order = []
                cur_rem[0] = 0
                eat_order.append((x, y))
                c = Node((x, y), cur_rem, eat_order, self.graph, 0, copy.deepcopy(self.cost+1),parent=self)
                # for greedy search
                # c.update_greedy_heu(aim)
                # for A* Search
                # c.update_a_star(aim)
                child.append(c)
                return child
            if maze[x][y] == ' ':
                c = Node((x, y), copy.deepcopy(self.rem), copy.deepcopy(self.eat_order),self.graph,
                         copy.deepcopy(self.rem_num), copy.deepcopy(self.cost+1), parent=self)
                # for greedy search
                # c.update_greedy_heu(aim)
                # for A*Search
                # c.update_a_star(aim)
                child.append(c)
        return child

    def eat(self, maze: list, vertex: list)->list:
        child = []
        av_pos = [self.left(), self.right(), self.up(), self.down()]
        for x, y in av_pos:
            if maze[x][y] == ' ':
                c = Node((x, y), copy.deepcopy(self.rem), copy.deepcopy(self.eat_order), self.graph,
                         copy.deepcopy(self.rem_num), copy.deepcopy(self.cost+1),heu=self.heu,parent=self)
                c.update_a_star_heu()
                child.append(c)
            if maze[x][y] == '.':
                for v in vertex:
                    if v.index == (x, y):
                        index = vertex.index(v)
                if self.rem[index] == 1:
                    cur_rem = copy.deepcopy(self.rem)
                    cur_rem[index] = 0
                    num = copy.deepcopy(self.rem_num-1)
                    eat_order = copy.deepcopy(self.eat_order)
                    eat_order.append((x,y))
                    graph = copy.deepcopy(self.graph)
                    new_heu = graph.mst(vertex[index])
                    c = Node((x, y), cur_rem, eat_order, graph, num, copy.deepcopy(self.cost+1),parent=self)
                    if c.rem_num == 0:
                        child = []
                        child.append(c)
                        return child
                    c.update_a_star_heu(new_heu)
                else:
                    c = Node((x, y), copy.deepcopy(self.rem), copy.deepcopy(self.eat_order), self.graph,
                             copy.deepcopy(self.rem_num), copy.deepcopy(self.cost + 1),heu=self.heu,parent=self)
                    c.update_a_star_heu()
                child.append(c)
        return child

    def update_greedy_heu(self, aim: tuple):
        self.heu = int(math.fabs(self.position[0]-aim[0]) + math.fabs(self.position[1]-aim[1]))

    def update_a_star_single_aim(self,aim: tuple):
        self.update_greedy_heu(aim)
        self.est = self.cost + self.heu

    def cal_distance(self, x, y):
        return int(math.fabs(self.position[0]- x) + math.fabs(self.position[1]-y))

    def update_start_heu(self):
        self.heu = self.graph.mst()
        return

    def update_a_star_heu(self, new_heu=None):
        shortest = 256
        if new_heu is not None :
            self.heu = new_heu
            self.graph.find_boundary()
        for x,y in self.graph.bound:
            distance = self.cal_distance(x,y)
            if distance < shortest:
                shortest = distance
        self.est = self.heu + self.cost + shortest
        return


def bfs(frontier:list)->Node:
    return frontier.pop(0)


def dfs(frontier:list)->Node:
    return frontier.pop()


def greedy(frontier:list)->Node:
    return heapq.heappop(frontier)


def a_star(frontier:list)->Node:
    return heapq.heappop(frontier)


