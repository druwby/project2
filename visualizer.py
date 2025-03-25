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

        if vertex not in visited:
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


def search_visualizer(result, title, G, pos):
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
        nx.draw(G, pos, with_labels=True, 
                node_color=['b' if n == node else 
                           ('y' if n in result['path'] else 
                           ('r' if G.degree(n) == 0 else 'g')) 
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
    
    # Add ALL nodes, including Titan-infested areas
    for r in range(rows):
        for c in range(cols):
            G.add_node((r, c), value=grid[r][c])
    
    # Add edges between adjacent nodes (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            #if grid[r][c] == -1:  # Skip connecting Titan-infested areas
             #   continue
                
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Check if neighbor is valid and not a Titan area
                if (0 <= nr < rows and 0 <= nc < cols):
                    G.add_edge((r, c), (nr, nc))
    
    # Create position mapping for visualization
    pos = {(r, c): (c, -r) for r in range(rows) for c in range(cols)}

    return G, pos


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
    result = order_bfs(grid1, -1, 0)
    graph1, pos = grid_to_graph(grid1)
    print(pos)
    #search_visualizer(result, "test", graph1, pos)