import queue
import time
import networkx as nx
import matplotlib.pyplot as plot


#BFS search logic

def order_bfs(graph, start_node):
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    order = []

    while not q.empty():
        vertex = q.get()
        if vertex not in visited:
            order.append(vertex)
            visited.add(vertex)
            for node in graph[vertex]:
                if node not in visited:
                    q.put(node)
    return order


def search_visualizer(order, title, G, pos):
    plot.figure()
    plot.title(title)
    for i, node in enumerate(order, start=1):
        plot.clf()
        plot.title(title)
        nx.draw(G, pos, with_labels=True, node_color=['b' if n == node else ('r' if G.degree(n) == 0 else 'g') for n in G.nodes()])
        plot.draw()
        plot.pause(2)
    plot.show()
    time.sleep(2)

G = nx.grid_2d_graph(5,5)
pos = pos = dict((n, n) for n in G.nodes())
donotvisit = []
for each in G.edges((2,2)):
    donotvisit.append(each)
for each in G.edges((0,2)):
    donotvisit.append(each)
#donotvisit = G.edges(2,2)
#donotvisit.extend(G.edges(2,1))
G.remove_edges_from(donotvisit)
    
search_visualizer(order_bfs(G, (1,1)), 'BFS', G, pos)