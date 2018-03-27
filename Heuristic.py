import math


class Vertex:
    def __init__(self, x, y, parent=None):
        self.index = (x, y)
        self.parent = parent

    def __eq__(self,other):
        return self.index == other.index

    def __ne__(self,other):
        return self.index != other.index


class Edge:
    def __init__(self, head: Vertex, tail: Vertex):
        self.head = head
        self.tail = tail
        self.value = int(math.fabs(tail.index[0]-head.index[0]) + math.fabs(tail.index[1]-head.index[1]))


class Graph:
    def __init__(self, v=0, e=0):
        self.vertex_num = v
        self.edge_num = e
        self.vertex = []
        self.edge = []
        self.total_edge = []
        self.fat = []
        self.vertex_y = []
        self.bound = []

    def find_vertex(self, x, y):
        for v in self.vertex:
            if v.index == (x, y):
                return v

    def add_vertex(self, v: Vertex):
        i = 0
        while i < self.vertex_num:
            if v == self.vertex[i]:
                return i
            i += 1
        self.vertex.append(v)
        self.vertex_num += 1
        self.edge.append([])
        return len(self.edge)-1

    def add_edge(self, e: Edge):
        i = self.add_vertex(e.head)
        self.add_vertex(e.tail)
        if e not in self.edge[i]:
            self.edge[i].append(e)
            self.total_edge.append(e)
            self.edge_num += 1

    def remove_vertex(self, v: Vertex):
        n = self.vertex_num
        if v:
            j = 0
            while j < n:
                if v == self.vertex_y[j]:
                    self.vertex_y.remove(self.vertex_y[j])
                    break
                j += 1
            i = 0
            while i < n:
                if v == self.vertex[i]:
                    self.vertex.remove(self.vertex[i])
                    self.vertex_num -= 1
                    return i
                i += 1

    def remove_edge(self, v: Vertex):
        index = self.remove_vertex(v)
        n = len(self.edge[index])
        if not n:
            n = 0
        self.edge.remove(self.edge[index])
        for i in self.edge:
            for j in i:
                if j.tail == v:
                    i.remove(j)
                    n += 1
        i = 0
        e = self.edge_num
        while i < e:
            if v == self.total_edge[i].head:
                self.total_edge.remove(self.total_edge[i])
                e -= 1
            elif v == self.total_edge[i].tail:
                self.total_edge.remove(self.total_edge[i])
                e -= 1
            else:
                i += 1
        self.edge_num -= n

    def sort_edge(self):
        self.total_edge.sort(key=lambda e : e.value)

    def sort_vertex_y(self):
        self.vertex_y = sorted(self.vertex, key=lambda v: v.index[1])

    def find_boundary(self):
            bound = set()
        # ho_bo_len = self.vertex_y[self.vertex_num-1].index[1] - self.vertex_y[0].index[1]
        # ver_bo_len = self.vertex[self.vertex_num-1].index[0] - self.vertex[0].index[0]
            lo = 256
            hi = 0
        # if ho_bo_len > ver_bo_len:
            for v in self.vertex_y:
                if v.index[1] <= lo:
                    lo = v.index[1]
                    bound.add(v.index)
                else:
                    break
            n = self.vertex_num - 1
            while n>=0:
                if self.vertex_y[n].index[1] >= hi:
                    hi = self.vertex_y[n].index[1]
                    bound.add(self.vertex_y[n].index)
                else:
                    break
                n -= 1
        # else:
            lo = 256
            hi = 0
            for v in self.vertex:
                if v.index[0] <= lo:
                    lo = v.index[0]
                    bound.add(v.index)
                else:
                    break
            n = self.vertex_num - 1
            while n >= 0:
                if self.vertex[n].index[0] >= hi:
                    hi = self.vertex[n].index[0]
                    bound.add(self.vertex[n].index)
                else:
                    break
                n -= 1
            self.bound = list(bound)
            return self.bound

    def nearest_vertex(self, v: Vertex):
        for e in self.total_edge:
            if e.head == v:
                return e.tail
            elif e.tail == v:
                return e.head

    def find_set(self, v: Vertex):
        index = self.vertex.index(v)
        if index == self.fat[index]:
            return self.fat[index]
        else:
            return self.find_set(self.vertex[self.fat[index]])

    def same_set(self, v1: Vertex, v2: Vertex):
        if self.find_set(v1) == self.find_set(v2):
            return True
        else:
            return False

    def combine_set(self, v1: Vertex, v2: Vertex):
        x = self.find_set(v1)
        y = self.find_set(v2)
        if x == y:
            return
        else:
            self.fat[y] = x

    def mst(self, v=None):
        if v:
            self.remove_edge(v)
        self.fat = []
        lon = 0
        i = 0
        while i < self.vertex_num:
            self.fat.append(i)
            i += 1
        for e in self.total_edge:
            if not self.same_set(e.head, e.tail):
                lon += e.value
                self.combine_set(e.head, e.tail)
        return lon






