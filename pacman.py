import Heuristic as He
import Pacman_node as Pa
import heapq
import copy

maze = []
vertex = []
graph = He.Graph()
with open('tinySearch.txt', 'r') as file:
    ini_maze = file.readlines()
    n = len(ini_maze)
    i = 0
    while i < n - 1:
        line = list(ini_maze[i][:len(ini_maze[i])-1])
        l = len(line)
        j = 0
        while j < l:
            if line[j] == 'P':
                start = (i, j)
            elif line[j] == '.':
                v = He.Vertex(i, j)
                vertex.append(v)
            j += 1
        i += 1
        maze.append(line)
    maze.append(list(ini_maze[len(ini_maze)-1]))
num = len(vertex)
if num == 1:
    graph.add_vertex(vertex[0])
    aim = vertex[0].index
else:
    i = 0
    while i < num:
        j = i + 1
        while j < num:
            e = He.Edge(vertex[i], vertex[j])
            graph.add_edge(e)
            j += 1
        i += 1
    graph.sort_edge()
    graph.sort_vertex_y()
    graph.find_boundary()
rem = []
for i in range(num):
    rem.append(1)
frontier = []
expanded = set()
fron_set = set()
expanded_num = 0
cost = 0
eat_order = []
path_node = None
maze_copy = copy.deepcopy(maze)
start_node = Pa.Node(start, copy.deepcopy(rem), [], copy.deepcopy(graph), copy.deepcopy(num))
# greedy search heuristic function
# start_node.update_greedy_heu(start)
# A* search heuristic function for a single aim
# start_node.update_a_star_single_aim(start)
# A* search.heuristic function for multiple aims
start_node.update_start_heu()
start_node.update_a_star_heu()
fron_set.add((start_node.position,tuple(start_node.rem)))
frontier.append(start_node)
# greedy search or A* Search
heapq.heapify(frontier)
if num == 1:
    while frontier:
        if num == 0:
            break
        # 4 search method to select: bfs, dfs, greedy search, A* search
        current_node = Pa.dfs(frontier)
        state = (current_node.position,tuple(current_node.rem))
        if state not in expanded:
            expanded_num += 1
            child = current_node.act(maze_copy, aim)
            expanded.add((copy.deepcopy(current_node.position),copy.deepcopy(tuple(current_node.rem))))
        else:
            child = []
        for c in child:
            if c.rem_num == 0:
                cost = c.cost
                path_node = c
                num = 0
                break
            state = (c.position,tuple(c.rem))
            if state not in expanded:
                # for greedy search and A* Search
                # heapq.heappush(frontier,c)
                # for bfs and dfs
                frontier.append(c)
else:
    while frontier:
        if num == 0:
            break
        current_node = Pa.a_star(frontier)
        state = (current_node.position,tuple(current_node.rem))
        if state not in expanded:
            expanded_num += 1
            child = current_node.eat(maze_copy, vertex)
            expanded.add((current_node.position, tuple(current_node.rem)))
        else:
            child = []
        for c in child:
            if c.rem_num == 0:
                cost = c.cost
                eat_order = c.eat_order
                num = 0
                break
            state = (c.position,tuple(c.rem))
            if state not in expanded:
                heapq.heappush(frontier, c)

# for part1.1 output solution
# while path_node.parent:
#     path = path_node.position
#     maze_copy[path[0]][path[1]] = '.'
#     path_node = path_node.parent
# with open('mediumMaze_dfs.txt', 'x') as file:
#     print("number of expanded nodes:",expanded_num,"path cost:",cost,file=file)
#     for i in maze_copy:
#         print(''.join(i), file=file)

# print part1.2
print("number of expanded nodes:",expanded_num,"path cost:",cost)
i = 1
j = 97
for x, y in eat_order:
    if i < 10:
        maze_copy[x][y] = '{}'.format(i)
        i += 1
    else:
        maze_copy[x][y] = chr(j)
        j += 1
with open('tinySearch1_result.txt', 'x') as file:
    print("number of expanded nodes:",expanded_num,"path cost:",cost,file=file)
    for l in maze_copy:
        print(''.join(l), file=file)
