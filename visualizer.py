import queue
import time
import networkx as nx
import matplotlib.pyplot as plt
import random

INF = float('inf')

# create a random 2d grid list
def rand_grid(m, n):
    opt = [0, -1, INF]
    randgrid = []

    for i in range(m):
        row = []  # create a new row
        for j in range(n):
            row.append(random.choice(opt))
        randgrid.append(row)  # add the complete row to the grid
    return randgrid

#BFS search logic

def order_bfs(graph, start_node, end_node):
    visited = set()
    q = queue.Queue()
    q.put(start_node)
    distances = {start_node: 0}
    parents = {start_node: None}
    
    order = []
    found = False

    while not q.empty():
        vertex = q.get()
        print(vertex)
        if vertex not in visited and graph.nodes[vertex]['value'] != -1:
            order.append(vertex)
            visited.add(vertex)

            if vertex == end_node:
                found = True
                break

            for neighbor in graph[vertex]:

                if neighbor not in visited:
                    q.put(neighbor)

                    if neighbor not in parents:
                        parents[neighbor] = vertex
                        distances[neighbor] = distances[vertex] + 1
    path = []
    if found:
        current = end_node
        while current is not None:
            path.append(current)
            current = parents[current]
        path.reverse()

    return {'order':order, 'found':found, 'distance':distances.get(end_node, -1), 'path':path}


def search_visualizer(result, title, G, pos, node_labels):
    plt.figure()
    plt.title(f"{title}: Distance = {result['distance']}")
    
    # Create an edge list for the path
    path_edges = []
    if len(result['path']) > 1:
        for i in range(len(result['path'])-1):
            path_edges.append((result['path'][i], result['path'][i+1]))
    
    # Visualize each step
    for i, node in enumerate(result['order'], start=1):
        plt.clf()
        plt.title(f"{title}: Step {i}, Distance = {result['distance']}")
        
        # Draw the graph
        nx.draw(G, pos, with_labels=True, node_shape = 's', labels = node_labels,
                node_color=['b' if n == node else 
                           ('y' if n in result['path'] else 
                           ('r' if node_labels[n] == -1 else 'g')) 
                           for n in G.nodes()])
        
        # Highlight the path edges
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, 
                              width=2, edge_color='r')
        
        plt.draw()
        plt.pause(2)
    
    plt.show()
    time.sleep(2)

def grid_to_graph(grid):
    """Convert a 2D grid to a NetworkX graph"""
    G = nx.Graph()
    rows, cols = len(grid), len(grid[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # add nodes and edges to graph object
    for r in range(rows):
        for c in range(cols):
            G.add_node((r, c), value=grid[r][c], label=grid[r][c])
            for drow, dcol in directions:
                newrow, newcol = r+drow, c+dcol
                if (0<=newrow<rows and 0<= newcol < cols):
                    G.add_edge((r,c), (newrow,newcol))
    
    # Create position mapping for visualization
    pos = {(r, c): (c, -r) for r in range(rows) for c in range(cols)}

    node_labels = {}
    for node, data in G.nodes(data=True):  # Iterate with attribute data
        node_labels[node] = data.get('value', 'default')  # Use .get() to avoid KeyError

    return G, pos, node_labels


# Complete example:
if __name__ == "__main__":

    
    grid1 = [
        [INF, -1, 0, INF],
        [INF, INF, INF, -1],
        [INF, -1, INF, -1],
        [0, -1, INF, INF]
    ]

    grid2 = [
        [0, INF, INF],
        [INF, -1, INF],
        [INF, INF, 0]
    ]

    #solved_grid1 = solve_walls_of_maria(grid1)
    #visualize_solution(grid1, solved_grid1)
    #solved_grid2 = solve_walls_of_maria(grid2)
    #visualize_solution(grid2, solved_grid2)
    #solved_grid3 = solve_walls_of_maria(randgrid)
    #visualize_solution(randgrid, solved_grid3)
    #visualize_titan_grid(grid1)
    #visualize_titan_grid(solved_grid1)
    #result = order_bfs(grid1, -1, 0)
    graph1, pos1, node_labels1 = grid_to_graph(grid1)
    result1 = order_bfs(graph1, (0,0), (0,2))
    search_visualizer(result1, "Graph 1", graph1, pos1, node_labels1)

    graph2, pos2, node_labels2 = grid_to_graph(grid2)
    result2 = order_bfs(graph2, (0,0), (0,2))
    search_visualizer(result1, "Graph 2", graph2, pos2, node_labels2)

    grid3 = rand_grid(10, 10)
    graph3, pos3, node_labels3 = grid_to_graph(grid3)
    result3 = order_bfs(graph3, (0,0), (0,2))
    search_visualizer(result3, "Random Graph", graph3, pos3, node_labels3)
