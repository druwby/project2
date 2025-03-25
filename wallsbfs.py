import queue
import random

# used for printing colors in terminal (may not work for everyone)
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[0m'

# used to refrain from typing float('inf) every time we input INF in the grid
INF = float('inf')

def solve_bfs(grid):
    if not grid or not grid[0]:
        return grid
        
    rows, cols = len(grid), len(grid[0])
    # creates a copy of the grid to modify
    result = [row[:] for row in grid]
    
    # initialize queue with all of the strongholds
    q = queue.Queue()
    visited = set()
    
    # add all of the strongholds to the queue as starting points
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:  # 0 represents a stronghold
                q.put((r, c))
                visited.add((r, c))
    
    # movement directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # BFS from all strongholds in the queue
    while not q.empty():
        r, c = q.get()
        # each pair from directions represents (change in row, change in column) so
        for dr, dc in directions:
            #new row, new column is formed
            nr, nc = r + dr, c + dc
            
            # check if new position is a valid cell and has not been visited
            if (0 <= nr < rows and 0 <= nc < cols and 
                grid[nr][nc] != -1 and (nr, nc) not in visited):
                
                # update distance traveled (current distance + 1)
                result[nr][nc] = result[r][c] + 1
                
                q.put((nr, nc))
                visited.add((nr, nc))
    
    return result

# randomly generate grids for more rigorous testing
def rand_grid(m, n):
    opt = [0, -1, INF]
    randgrid = []

    for i in range(m):
        row = []  # create a new row
        for j in range(n):
            row.append(random.choice(opt))
        randgrid.append(row)  # add the complete row to the grid
    return randgrid

# print the grid with colors for better readability
# i was working on displaying the grids with networkx and matplotlib but ran out of time finishing the implementation
def print_grid(grid):
    for row in grid:
        for val in row:
            if val == -1:
                print(f"{RED}{val:>5}{RESET}", end='')
            elif val == 0:
                print(f"{BLUE}{val:>5}{RESET}", end='')
            elif val == INF:
                print(f"{MAGENTA}{val:>5}{RESET}", end='')
            else:
                print(f"{GREEN}{val:>5}{RESET}", end='')
        print()  # new line after each row is finished


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

    randomgrid = rand_grid(10,10)

    print("Original Grid 1:")
    print_grid(grid1)
    print("\nSolved Grid 1:")
    print_grid(solve_bfs(grid1))

    print("Original Grid 2:")
    print_grid(grid2)
    print("\nSolved Grid: 2")
    print_grid(solve_bfs(grid2))

    print("Original Random Grid:")
    print_grid(randomgrid)
    print("\nSolved Random Grid:")
    print_grid(solve_bfs(randomgrid))