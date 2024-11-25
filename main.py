import itertools as it
from copy import deepcopy as copy

def get_neighbours(grid, x, y):
    n = 0
    for x2 in range(-1, 2):
        for y2 in range(-1, 2):
            if (x2 or y2) and 0 <= x + x2 < len(grid[0]) and 0 <= y + y2 < len(grid):
                n += int(grid[y + y2][x + x2])

    return n

def step_forward(grid):
    new = copy(grid)
    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char == "1":
                if get_neighbours(grid, x, y) in [2, 3]:
                    new[y][x] = "1"
                else:
                    new[y][x] = "0"
            else:
                if get_neighbours(grid, x, y) == 3:
                    new[y][x] = "1"
                else:
                    new[y][x] = "0"


    return new

def shape_in_grid(grid_lines, shape_lines):
    # Split the input strings into 2D lists (list of rows)

    # Dimensions of the grid and shape
    grid_rows, grid_cols = len(grid_lines), len(grid_lines[0])
    shape_rows, shape_cols = len(shape_lines), len(shape_lines[0])

    # Early exit if the shape is larger than the grid
    if shape_rows > grid_rows or shape_cols > grid_cols:
        return False

    # Sliding window check
    for i in range(grid_rows - shape_rows + 1):  # Rows of the grid to start the shape
        for j in range(grid_cols - shape_cols + 1):  # Columns of the grid to start the shape
            # Check if the shape matches the grid section
            match = True
            for si in range(shape_rows):
                if grid_lines[i + si][j:j + shape_cols] != shape_lines[si]:
                    match = False
                    break
            if match:
                return True  # Shape found

    return False  # Shape not found

# def shape_in_grid(grid_lines, shape_lines):
#     # Split the input strings into 2D lists (list of rows)

#     # Dimensions of the grid and shape
#     grid_rows, grid_cols = len(grid_lines), len(grid_lines[0])
#     shape_rows, shape_cols = len(shape_lines), len(shape_lines[0])

#     # Early exit if the shape is larger than the grid
#     if shape_rows > grid_rows or shape_cols > grid_cols:
#         return False

#     # Sliding window check
#     for i in range(grid_rows - shape_rows + 1):  # Rows of the grid to start the shape
#         for j in range(grid_cols - shape_cols + 1):  # Columns of the grid to start the shape
#             match = True

#             # Check the shape region
#             for si in range(shape_rows):
#                 if grid_lines[i + si][j:j + shape_cols] != shape_lines[si]:
#                     match = False
#                     break
            
#             if match:
#                 # Check everything outside the window
#                 for row in range(grid_rows):
#                     for col in range(grid_cols):
#                         # Skip the window region
#                         if i <= row < i + shape_rows and j <= col < j + shape_cols:
#                             continue
#                         if grid_lines[row][col] != "0":
#                             match = False
#                             break
#                     if not match:
#                         break
            
#             if match:
#                 return True  # Shape found with valid outside region

#     return False

def gen_combos(n_alive):
    all_possible = list(map(lambda e: "".join(e), it.product("10", repeat=8)))
    return [soln[:4] + "0" + soln[4:] for soln in all_possible if soln.count("1") == n_alive]

combos = {k: gen_combos(k) for k in range(9)}

def fill_around(x, y, grid, perm):
    for i, char in enumerate(perm):
        x2 = i % 3 - 1
        y2 = i // 3 - 1
        if (x2 or y2) and 0 <= y + y2 < len(grid) and 0 <= x + x2 < len(grid[0]): 
            grid[y + y2][x + x2] = char

# inp = "00100 01010 10001 01010 00100".split(" ")
inp = "10001 10000 11101 10101 10101".split(" ")
# inp = "010 001 111".split(" ")
w, h = len(inp[0]), len(inp)
original = list(map(list, inp))

inp = "".join(inp)


possibilities = []

for char in inp:
    if char == 1:
        possibilities += [
            {
                0: combos[3],
                1: combos[2] + combos[3]
            }
        ]
    else:
        possibilities += [
            {
                0: combos[0] + combos[1] + combos[2] + combos[4] + combos[5] + combos[6] + combos[7] + combos[8],
                1: combos[0] + combos[1] + combos[4] + combos[5] + combos[6] + combos[7] + combos[8]
            }
        ]

n = 0
# out_a = [list("0" * (w + 2)) for _ in range(h + 2)]
out_a = [list("0" * (w + 2)) for _ in range(h + 2)]
_01s = it.product([0, 1], repeat = w * h)

for dec in _01s:
    state = []
    for i, poss in enumerate(possibilities):
        state += [poss[dec[i]]]

    for cstate in it.product(*state):
        n += 1
        out = copy(out_a)   
        for i, change in enumerate(cstate):
            x = i % w
            y = i // w
            c = dec[i]

            out[y][x] = str(c)

            fill_around(x, y, out, change)
        
        if shape_in_grid(step_forward(out), original):
            print("FOUND!!")
            print(out)
            exit()

        if n % 1000 == 0:
            print(f"Checked {n}")
            # print(step_forward(out), out)
