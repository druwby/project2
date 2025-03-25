from visualizer import *
import random

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\0 প্রেস[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
RESET = '\033[0m'

print(RED + "This is red text" + RESET)
print(GREEN + "This is green text" + RESET)
print(YELLOW + "This is yellow text" + RESET)
print(BLUE + "This is blue text" + RESET)
print(MAGENTA + "This is magenta text" + RESET)
print(CYAN + "This is cyan text" + RESET)
print(WHITE + "This is white text" + RESET)


# Complete example:

INF = float('inf')
opt = [0, -1, INF]
randgrid = []
m = 20
n = 10
for i in range(m):
    row = []  # Create a new row
    for j in range(n):
        row.append(random.choice(opt))
    randgrid.append(row)  # Add the complete row to the grid
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
solved_grid1 = solve_walls_of_maria(grid1)
visualize_solution(grid1, solved_grid1)
solved_grid2 = solve_walls_of_maria(grid2)
visualize_solution(grid2, solved_grid2)
solved_grid3 = solve_walls_of_maria(randgrid)
visualize_solution(randgrid, solved_grid3)

visualize_titan_grid(grid1, solved_grid1)
solved_grid2 = solve_walls_of_maria(grid2)
visualize_titan_grid(grid2, solved_grid2)
solved_grid3 = solve_walls_of_maria(randgrid)
visualize_solution(randgrid, solved_grid3)