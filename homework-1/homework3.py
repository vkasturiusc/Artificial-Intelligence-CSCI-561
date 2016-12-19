from collections import deque
import graph

start = graph.get_start().rstrip('\n')
goal = graph.get_goal().rstrip('\n')
path = []
adj_list = graph.graph_create()
heu_list = graph.sunny_graph()
output = list()
def bfs(graph):

    open = deque([[[start,0]]])
    closed = deque([[]])

    while len(open) > 0:
        state = open.popleft()
        closed.append(state[0][0])

        if state[0][0] == goal:
            path = state
            path.reverse()
            return path

        try:
         for frontier_state in adj_list[state[0][0]]:
            if frontier_state[0] in closed:
                continue
            flag=0
            for lists in open:
                    if frontier_state[0]==lists[0][0]:
                        flag=1
                        break
            if flag ==1:
                continue
            temp_state = [[frontier_state[0],1+state[0][1]]] + state
            open.append(temp_state)
        except KeyError:
            pass

    return None

def dfs(graph):
    open = deque([[[start, 0]]])
    closed = deque([[]])

    while len(open) > 0:
        state = open.popleft()
        closed.append(state[0][0])

        if state[0][0] == goal:
            path = state
            path.reverse()
            return path

        try:
          for frontier_state in reversed(adj_list[state[0][0]]):
            if frontier_state[0] in closed:
                continue
            flag = 0
            for lists in open:
                if frontier_state[0] == lists[0][0]:
                    flag = 1
                    break
            if flag==1:
                continue
            temp_state = [[frontier_state[0], 1 + state[0][1]]] + state
            open.appendleft(temp_state)
        except KeyError:
            pass

    return None

def ucs(graph):

    open = deque([[0, [[start, 0]]]])
    closed = deque([])

    while len(open) > 0:
        state = open.popleft()[1]
        closed.append(state[0][0])

        if state[0][0] == goal:
            path = state
            path.reverse()
            return path

        try:
         for frontier_state in adj_list[state[0][0]]:
            if frontier_state[0] in closed:
                continue

            temp_state = [frontier_state[1]+state[0][1],[[frontier_state[0],frontier_state[1]+state[0][1]]] + state]

            count = 0
            flag=0

            for lists in open:
                if (frontier_state[0]==lists[1][0]) and (frontier_state[1]<lists[1][1]):
                    flag=count
                else:
                    '''do nothing'''
                count+=1
            if flag==0:
                open.append(temp_state)
            else:
                open[flag] = temp_state
            temp_open = list(open)
            temp_open.sort(key=lambda x:x[0])
            open=deque(temp_open)
        except KeyError:
            pass

    return None

def astar(graph):

    open = deque([[0, [[start, 0]]]])
    closed = deque([])

    while len(open) > 0:
        state = open.popleft()[1]
        closed.append(state[0][0])

        if state[0][0] == goal:
            path = state
            path.reverse()
            return path

        try:
         for frontier_state in adj_list[state[0][0]]:

            temp_state = [frontier_state[1]+state[0][1]+heu_list[frontier_state[0]],[[frontier_state[0],frontier_state[1]+state[0][1]]] + state]
            count = 0
            flag=0
            for lists in open:
                if (frontier_state[0]==lists[1][0][0]) and (frontier_state[1]<lists[1][0][1]):
                    flag=count
                else:
                    '''do nothing'''
                count+=1
            if flag==0:
                open.append(temp_state)
            else:
                open[flag] = temp_state

            temp_open = list(open)
            temp_open.sort(key=lambda x:x[0])
            open=deque(temp_open)
        except KeyError:
            pass
    return None

fw = open("output.txt","w+")
i=0
if "B" in graph.get_search_type():

    output = bfs(graph)
    print("BFS: ",output,"\n")

elif "D" in graph.get_search_type():

    output = dfs(graph)
    print("DFS: ",output, "\n")

elif "U" in graph.get_search_type():

    output = ucs(graph)
    print("UCS: ", ucs(graph), "\n")

elif "A" in graph.get_search_type():

    output = astar(graph)
    print("Astar: ",astar(graph),"\n")

while i < len(output):
    line = output[i][0] + " " + str(output[i][1]) + "\n"
    fw.writelines(line)
    i += 1