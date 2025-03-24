import queue
import time
import networkx as nx
import matplotlib.pyplot as plt


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

def parse_grid_input(input_text):
    """Parse the input format from algo1.txt to a 2D grid"""
    # Remove the 'Input:' and brackets, split by lines
    grid_text = input_text.replace('Input:', '').replace('[', '').replace(']', '').strip()
    lines = [line.strip() for line in grid_text.split('\n') if line.strip()]
    
    grid = []
    for line in lines:
        row = []
        # Split by commas and process each cell
        cells = [cell.strip() for cell in line.split(',')]
        for cell in cells:
            if not cell:  # Skip empty cells
                continue
            if cell == 'INF':
                row.append(float('inf'))  # Use infinity for INF
            else:
                row.append(int(cell))  # Convert -1 and 0 to integers
        if row:
            grid.append(row)
    
    return grid

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
            if grid[r][c] == -1:  # Skip connecting Titan-infested areas
                continue
                
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                # Check if neighbor is valid and not a Titan area
                if (0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != -1):
                    G.add_edge((r, c), (nr, nc))
    
    # Create position mapping for visualization
    pos = {(r, c): (c, -r) for r in range(rows) for c in range(cols)}
    
    return G, pos

def visualize_titan_grid(grid, title="Walls of Maria"):
    """Create a graph from grid and visualize with strongholds and titans"""
    G, pos = grid_to_graph(grid)
    
    # Color mapping:
    # - Green (0): Strongholds
    # - Red (-1): Titan areas
    # - Blue (INF or other): City areas with distances
    node_colors = []
    labels = {}
    
    for node in G.nodes():
        r, c = node
        value = grid[r][c]
        
        if value == 0:
            node_colors.append('green')
        elif value == -1:
            node_colors.append('red')
        elif value == float('inf'):
            node_colors.append('blue')
        else:
            node_colors.append('yellow')  # Distance values
            
        # Create labels showing the distance values
        if value == float('inf'):
            labels[node] = 'INF'
        elif value == -1:
            labels[node] = 'X'
        else:
            labels[node] = str(value)
    
    # Visualization
    plt.figure(figsize=(10, 8))
    plt.title(title)
    
    # Draw the graph
    nx.draw(G, pos=pos, node_color=node_colors, with_labels=False)
    nx.draw_networkx_labels(G, pos, labels=labels)
    
    plt.show()

def solve_walls_of_maria(grid):
    """Solve the problem using multi-source BFS"""
    rows, cols = len(grid), len(grid[0])
    result_grid = [row[:] for row in grid]  # Make a copy of the grid
    
    # Find all strongholds to use as starting points
    strongholds = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                strongholds.append((r, c))
    
    # Create graph from grid
    G, pos = grid_to_graph(grid)
    
    # Run modified BFS from all strongholds
    visited = set()
    q = queue.Queue()
    
    # Initialize with all strongholds
    for r, c in strongholds:
        q.put((r, c))
        visited.add((r, c))
    
    # BFS
    while not q.empty():
        r, c = q.get()
        
        # Get current distance
        current_dist = result_grid[r][c]
        
        # Check all four directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            
            # Check if valid and not visited
            if (0 <= nr < rows and 0 <= nc < cols and
                (nr, nc) not in visited and result_grid[nr][nc] != -1):
                
                # Update distance
                if result_grid[nr][nc] == float('inf'):
                    result_grid[nr][nc] = current_dist + 1
                
                q.put((nr, nc))
                visited.add((nr, nc))
    
    return result_grid

def visualize_solution(original_grid, solved_grid, title="Walls of Maria - Solved"):
    """Visualize before and after grids"""
    # Create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Convert grids to NetworkX graphs
    G1, pos1 = grid_to_graph(original_grid)
    G2, pos2 = grid_to_graph(solved_grid)
    
    # Labels for the original grid
    labels1 = {}
    for node in G1.nodes():
        r, c = node
        val = original_grid[r][c]
        if val == -1:
            labels1[node] = "X"
        elif val == 0:
            labels1[node] = "0"
        elif val == float('inf'):
            labels1[node] = "INF"
        else:
            labels1[node] = str(val)
    
    # Labels for the solved grid
    labels2 = {}
    for node in G2.nodes():
        r, c = node
        val = solved_grid[r][c]
        if val == -1:
            labels2[node] = "X"
        elif val == 0:
            labels2[node] = "0" 
        elif val == float('inf'):
            labels2[node] = "INF"
        else:
            labels2[node] = str(val)
    
    # Color nodes
    node_colors1 = []
    for node in G1.nodes():
        r, c = node
        val = original_grid[r][c]
        if val == -1:
            node_colors1.append('red')
        elif val == 0:
            node_colors1.append('green')
        else:
            node_colors1.append('blue')
    
    node_colors2 = []
    for node in G2.nodes():
        r, c = node
        val = solved_grid[r][c]
        if val == -1:
            node_colors2.append('red')
        elif val == 0:
            node_colors2.append('green')
        else:
            node_colors2.append('yellow')
    
    # Draw original grid
    ax1.set_title("Original Grid")
    nx.draw(G1, pos=pos1, ax=ax1, with_labels=False, node_color=node_colors1)
    nx.draw_networkx_labels(G1, pos1, labels=labels1, ax=ax1)
    
    # Draw solved grid
    ax2.set_title("Solved Grid")
    nx.draw(G2, pos=pos2, ax=ax2, with_labels=False, node_color=node_colors2)
    nx.draw_networkx_labels(G2, pos2, labels=labels2, ax=ax2)
    
    plt.tight_layout()
    plt.show()