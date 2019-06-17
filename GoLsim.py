import random
import numpy as np
import time

def dead_state(width, height):
    # 0 represents dead cell or False Boolean Value or a 0 bit and 1 represents an alive cell or True Boolean Value or a 1 bit
    dead_grid = [[0] * width] * height
    return dead_grid

#width = 10
#height = 10
#print(dead_state(width, height))

def random_state(width, height):
    dead_grid = dead_state(width, height)
    # height is len(dead_grid) which is number of rows because matrices are R (rows) x C (columns) and width is len(dead_grid[0]) which is number of columns
    random_grid = []
    # now we have to randomize each element in state to either a 0 or 1 for an initial random state of the grid
    for i in range(0, len(dead_grid)):
        current_row = []
        for j in range(0, len(dead_grid[0])):
            # for some reason, the below code for random doesn't really work as each row is the same as before which makes no sense
            '''
            rand_num = rand.random()
            if rand_num >= 0.5:
                cell_state = 0
            else:
                cell_state = 1
            dead_grid[i][j] = cell_state
            '''
            # for some reason, the below code for random doesn't really work as each "randomly generated row" is the same as the very first randomly generated row which makes no sense
            #dead_grid[i][j] = np.random.randint(0,2)

            rand_num = random.random()
            if rand_num >= 0.5:
                cell_state = 0
            else:
                cell_state = 1
            current_row.append(cell_state)
        random_grid.append(current_row)
    #random_grid = dead_grid

    #random_grid = []
    #[random_grid.append(list(np.random.randint(len(dead_grid[0]), size = (2)))) for i in range(0, len(dead_grid))]
    return random_grid

#print(random_state(10,10))

def render(initial_random_board):
    '''
    for i in range(0, len(initial_random_board)):
        print(initial_random_board[i])
    '''
    rendered_initial_board = []
    #[print("_", end=" ") for i in range(0, len(initial_random_board))]
    beg = ["_" for i in range(0, len(initial_random_board[0])+2)]
    print("".join(beg))
    for i in range(0, len(initial_random_board)):
        current_row = []
        print("\n|", end="")
        for j in range(0, len(initial_random_board[0])):
            if initial_random_board[i][j] == 0:
                current_row.append(".")
            else:
                current_row.append("#")
        #[print(k, end = " ") for k in current_row]
        print("".join(current_row) + "|")
        rendered_initial_board.append(current_row)
    end = ["_" for i in range(0, len(initial_random_board[0])+2)]
    print("".join(end))

#a_dead_state = dead_state(30, 30)
#render(a_dead_state)

#a_random_state = random_state(10, 10)
#render(a_random_state)
'''
def cell_assignment(new_board, surrounding_cells, x, y):
    sum = 0
    for i in surrounding_cells:
        sum += i
    if new_board[x][y] == 1:
        if sum <= 1:
            new_board[x][y] = 0
        elif sum <= 3:
            new_board[x][y] = 1
        else:
            new_board[x][y] = 0
    else:
        if sum == 3:
            new_board[x][y] = 1
        else:
            new_board[x][y] = 0
'''
def cell_assignment_Moore(new_board, x, y):
    # We wanna iterate around each cell and check the different conditions. Make note of the surrounding cells' states and add them up for further evaluation
    sum = 0
    for x1 in range(x-1, (x+1)+1):
        if x1 < 0 or x1 >= len(new_board):
            continue
        for y1 in range(y-1, (y+1)+1):
            if y1 < 0 or y1 >= len(new_board[0]):
                continue
            if x1 == x and y1 == y:
                continue
            sum += new_board[x1][y1]

    if new_board[x][y] == 1:
        if sum <= 1:
            new_board[x][y] = 0
        elif sum <= 3:
            new_board[x][y] = 1
        else:
            new_board[x][y] = 0
    else:
        if sum == 3:
            new_board[x][y] = 1
        else:
            new_board[x][y] = 0

def cell_assignment_vonNeumann(new_board, x, y, r):
    # We wanna iterate around each cell and check the different conditions. Make note of the surrounding cells' states and add them up for further evaluation
    # I'm not sure how to code the ones for a r > 1 because I don't fully understand Manhattan Distance and extended von Neumann neighborhoods yet or can't find a good explanation of it online
    if r == 1:
        sum = 0
        for x1 in range(x-1, (x+1)+1):
            if x1 < 0 or x1 >= len(new_board):
                continue
            if x1 == x:
                continue
            sum += new_board[x1][y]
        for y1 in range(y-1, (y+1)+1):
            if y1 < 0 or y1 >= len(new_board[0]):
                continue
            if y1 == y:
                continue
            sum += new_board[x][y1]

        if new_board[x][y] == 1:
            if sum <= 1:
                new_board[x][y] = 0
            elif sum <= 3:
                new_board[x][y] = 1
            else:
                new_board[x][y] = 0
        else:
            if sum == 3:
                new_board[x][y] = 1
            else:
                new_board[x][y] = 0

def next_board_state(initial_board_state):
    '''
    Rules for this CA:
    1. Any live cell with 0 or 1 live neighbors becomes dead, because of underpopulation
    2. Any live cell with 2 or 3 live neighbors stays alive, because its neighborhood is just right
    3. Any live cell with more than 3 live neighbors becomes dead, because of overpopulation
    4. Any dead cell with exactly 3 live neighbors becomes alive, by reproduction

    How do we tackle this? Well, I see two options: 1. either we do a bunch of if-elif cases for edge and corner cells and separate
    the first row, middle rows, and last row 2. wrap the board around so each cell has 8 neighboring cells as usual and this can be done by
    creating a copy of the board and attaching it to the top, bottom, L, R sides of the original board and only looking at the neighboring
    rows or columns and using them as a reference point (think of attaching them like this).

    '''
    new_board = initial_board_state
    for x in range(0, len(new_board)):
        for y in range(0, len(new_board[0])):
            '''
            # check if cell is a corner
            if x == 0 and y == 0:
                surrounding_cells = [new_board[x][y-1], new_board[x+1][y], new_board[x+1][y-1]]
            elif x == len(new_board)-1 and y == 0:
                surrounding_cells = [new_board[x][y+1], new_board[x-1][y], new_board[x-1][y+1]]
            elif x == 0 and y == len(new_board[0])-1:
                surrounding_cells = [new_board[x-1][y], new_board[x-1][y-1], new_board[x][y-1]]
            elif x == len(new_board)-1 and y == len(new_board[0])-1:
                surrounding_cells = [new_board[x-1][y], new_board[x-1][y+1], new_board[x][y+1]]
            # check if cell is an edge/border
            elif y == 0:
                surrounding_cells = [new_board[x][y+1], new_board[x][y-1], new_board[x+1][y+1], new_board[x+1][y], new_board[x+1][y-1]]
            elif y == len(new_board[0])-1:
                surrounding_cells = [new_board[x][y+1], new_board[x][y-1], new_board[x-1][y+1], new_board[x-1][y], new_board[x-1][y-1]]
            elif x == 0:
                surrounding_cells = [new_board[x][y-1], new_board[x+1][y], new_board[x-1][y-1], new_board[x-1][y], new_board[x-1][y-1]]
            elif x == len(new_board)-1:
                surrounding_cells = [new_board[x][y+1], new_board[x+1][y], new_board[x-1][y+1], new_board[x-1][y], new_board[x-1][y+1]]
            # regular cell
            else:
                surrounding_cells = [new_board[x][y-1], new_board[x][y+1], new_board[x-1][y], new_board[x+1][y], new_board[x+1][y+1], new_board[x-1][y-1], new_board[x+1][y-1], new_board[x-1][y+1]]
            cell_assignment(new_board, surrounding_cells, x, y)
            '''
            cell_assignment_Moore(new_board, x, y)

    '''
    '''
    '''
    THIS PART BELOW DIDN'T ACTUALLY WORK FOR SOME REASON, SO I DECIDED TO GO WITH THE FIRST STRATEGY BECAUSE SIMPLICITY IS KEY IN DEVELOPING PROJECTS AND PRODUCTS (K.I.S.S.)
    Let's go with the second option because it is more
    flexible and less "hard-codey"
    So, in the second option, add the last column to the first column, first column to the last column, the last row to the first row, and the first row to the
    last row, and this is one new board to work with and then when you get to the top left corner, it is a neighbor of the bottom right corner and vice versa and
    and the bottom left corner is a neighbor of the top right corner and vice versa, so every single cell in this new board has 8 surrounding cells

    # SECOND ATTEMPT: create new board to work off of
    first_row = initial_board_state[0]
    last_row = initial_board_state[len(initial_board_state)-1]
    '''
    '''
    first_column = []
    last_column = []
    for i in range(0, len(initial_board_state)):
        first_column.append(initial_board_state[i][0])
        last_column.append(initial_board_state[i][len(initial_board_state[0])-1])
    '''
    '''
    initial_board_state.insert(len(initial_board_state), first_row)
    initial_board_state.insert(0, last_row)

    for i in range(0, len(initial_board_state)):
        print(initial_board_state[i])


    for i in range(1, len(initial_board_state)-1):
        initial_board_state[i].insert(0, initial_board_state[i][len(initial_board_state[0])-1])
        initial_board_state[i].insert(len(initial_board_state[1]), initial_board_state[i][1])
        #print(initial_board_state[i])
    new_board = initial_board_state
    for i in range(0, len(new_board)):
        print(new_board[i])
    '''
    '''
    # FIRST ATTEMPT: create new board to work off of
    beg_rows_height = len(initial_board_state)
    beg_columns_width = len(initial_board_state[0])
    old_first_row = initial_board_state[0]
    old_last_row = initial_board_state[len(initial_board_state)-1]
    for i in range(0, beg_rows_height):
        initial_board_state[i].insert(0, initial_board_state[i][beg_columns_width-1])
    beg_columns_width = len(initial_board_state[1])
    for i in range(0, beg_rows_height):
        # technically, we don't have to do beg_columns_width-1 because we're adding to the end and extending the length of the row/number of columns
        initial_board_state[i].insert(beg_columns_width, initial_board_state[i][1])
    #print(len(initial_board_state[0]))
    initial_board_state.insert(0, old_last_row)
    initial_board_state.insert(len(initial_board_state), old_first_row)
    '''
    '''
    new_board = initial_board_state
    render(new_board)
    #print(new_board)
    for x in range(1, len(new_board)-1):
        for y in range(1, len(new_board[0])-1):
            if x == 1 and y == 1:
                surrounding_cells = [new_board[x][y-1], new_board[x][y+1], new_board[x-1][y], new_board[x+1][y], new_board[x+1][y+1], new_board[x-1][y-1], new_board[x+1][y-1], new_board[len(new_board)-2][len(new_board[0])-2]]
                print(surrounding_cells)
                cell_assignment(new_board, surrounding_cells, x, y)
            elif x == len(new_board)-2 and y == 1:
                surrounding_cells = [new_board[x][y-1], new_board[x][y+1], new_board[x-1][y], new_board[x+1][y], new_board[x+1][y+1], new_board[x+1][y-1], new_board[x-1][y+1], new_board[1][len(new_board[0])-2]]
                cell_assignment(new_board, surrounding_cells, x, y)
            elif x == len(new_board)-2 and y == len(new_board[0])-2:
                surrounding_cells = [new_board[x][y-1], new_board[x][y+1], new_board[x-1][y], new_board[x+1][y], new_board[x+1][y+1], new_board[x-1][y-1], new_board[x-1][y+1], new_board[1][1]]
                cell_assignment(new_board, surrounding_cells, x, y)
            elif x == 1 and y == len(new_board[0])-2:
                surrounding_cells = [new_board[x][y-1], new_board[x][y+1], new_board[x-1][y], new_board[x+1][y], new_board[x-1][y-1], new_board[x+1][y-1], new_board[x-1][y+1], new_board[len(new_board[0])-2][1]]
                cell_assignment(new_board, surrounding_cells, x, y)
            else:
                surrounding_cells = [new_board[x][y-1], new_board[x][y+1], new_board[x-1][y], new_board[x+1][y], new_board[x+1][y+1], new_board[x-1][y-1], new_board[x+1][y-1], new_board[x-1][y+1]]
                cell_assignment(new_board, surrounding_cells, x, y)
    del new_board[len(new_board)-1]
    del new_board[0]
    for i in range(0, len(new_board)):
        del new_board[i][len(new_board[i])-1]
        del new_board[i][0]
    return new_board
    '''
    return new_board

def run_forever(starting_state):
    next_state = starting_state
    while(True):
        render(next_state)
        '''
        g = []
        print("_________________________")
        for i in next_state:
            current_row = []
            for j in range(0, len(next_state[0])):
                current_row.append(int(i[j]))
            print(current_row)
            g.append(current_row)
        '''
        next_state = next_board_state(next_state)
        time.sleep(0.05)

#run_forever(random_state(10,10))

def run_file(input_file):
    '''
    starting_conditions = []
    with open(input_file, 'r') as f:
        while f.readline() != "":
            starting_conditions.append(f.readline().strip())
            print(starting_conditions)
    '''
    with open(input_file, 'r') as f:
        contents = f.readlines()
    starting_conditions = contents

    for i in range(0, len(starting_conditions)):
        starting_conditions[i] = starting_conditions[i][:len(starting_conditions[i])-1]
    official_starting_conditions = []
    for i in starting_conditions:
        current_row = []
        for j in range(0, len(starting_conditions[0])):
            current_row.append(int(i[j]))
        print(current_row)
        official_starting_conditions.append(current_row)
    run_forever(official_starting_conditions)

run_file("E:\\Python\\Projects\\Game of Life Simulation\\toad.txt")
