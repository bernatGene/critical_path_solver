import numpy as np
import string

from collections import defaultdict
 
class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices  
 
    def addEdge(self, u, v):
        self.graph[u].append(v)
 
    def topologicalSortUtil(self, v, visited, stack):

        visited[v] = True
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
 
        stack.append(v)

    def topologicalSort(self):
        visited = [False]*self.V
        stack = []
 
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i, visited, stack)
 
        print(stack[::-1])
        return stack[::-1]


def record_input_basics():
    print("Num of tasks?")
    nt = int(input())
    print("Alpha or numeric (1/0)?")
    alpha = bool(int(input()))
    name_dic = ['s']
    if alpha:
        name_dic = ['s'] + list(string.ascii_lowercase[0:nt-2]) + ['z']
    else:
        name_dic = ['s'] + [str(x) for x in range(1,nt-1)] + ['z']
    revr_dic = {s : i for i,s in enumerate(name_dic)}
    return nt, name_dic, revr_dic

def record_input_structure(nt, name_dic, revr_dic):
    task_dur = np.zeros(nt)
    tma = np.zeros((nt, nt))
    for n in range(nt):
        if n != 0 and n != nt -1 :
            print(f"Task {name_dic[n]} duration?")
            task_dur[n] = int(input())
        if n != nt -1 :
            print(f"Task {name_dic[n]} connections?")
            conns = (input())
            for c in conns:
                ic = revr_dic[c]
                tma[n][ic] = 1
        print('-'*50)
    return task_dur, tma

def solve(task_dur, tma, nt, name_dic):
    g = Graph(nt)
    for i, l in enumerate(tma):
        for j, c in enumerate(l):
            if c:
                g.addEdge(i, j)
    tl = g.topologicalSort()
    items = {i : [d,0,0,0,0,0] for i, d in enumerate(task_dur)}
    # forward
    for n in tl[1:]:
        es_list = [items[p][2] for p, c in enumerate(tma[:, n]) if c]
        es = max(es_list)
        items[n][1] = es
        items[n][2] = items[n][1] + items[n][0] 
    # backward
    items[len(items)-1][3] = items[len(items)-1][1]
    items[len(items)-1][4] = items[len(items)-1][1]
    for n in tl[-2::-1]:
        lf_list = [items[p][3] for p, c in enumerate(tma[n]) if c]
        lf = min(lf_list)
        items[n][4] = lf
        items[n][3] = items[n][4] - items[n][0]
    # float
    for i,v in items.items():
        v[-1] = v[4]-v[2]
    # print
    print("SOLUTION")
    print("-"*50)
    for k, v in items.items():
        print(f"{name_dic[k]}:\tes:{v[1]}\tef:{v[2]}\tls:{v[3]}\tlf:{v[4]}\t float:{v[5]}")
    print("-"*50)
    print("\nCritical Path:", [name_dic[n] for n in tl if items[n][-1] == 0])

def interact():
    print('='*100)
    print('='*100)
    print("HELP: Critical Path solver")
    print("Follow prompts:")
    print("- Enter Number of Tasks")
    print("- Enter if they are either indexed by letters or by numbers")
    print("- For each task, enter duration (e.g. 10)") 
    print("- For each task, enter the children (e.g. adf if task connected to a, d and f)")
    print('='*100)
    print('='*100)
    nt, name_dic, revr_dic = record_input_basics()
    print("Task names:", name_dic)
    task_dur, tma = record_input_structure(nt, name_dic, revr_dic)
    solve(task_dur, tma, nt, name_dic)
    print('='*100)
    print('='*100)


if __name__ == "__main__":
    interact()
