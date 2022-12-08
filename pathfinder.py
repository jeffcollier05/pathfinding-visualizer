# LIBRARIES
import pygame
from queue import LifoQueue, PriorityQueue
import time
import tkinter.filedialog as tkf
import pickle
import random
import preloadedmazes as mazes


###############################################################################################
# INITIAL SETUP
###############################################################################################

#PROGRAM INFORMATION
version = "V5.0"
lastUpdate = "12/6/2022"

#WINDOW DISPLAY
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Visual Application of Pathfinding Algorithms")

#COLOR SET
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#DEFINES EACH GRID AND DEFINES STATUS
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == PURPLE

    def is_opennode(self):
        return self.color == WHITE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE
    
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win): 
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    #DETERMINES BARRIERS ON A GLOBAL LEVEL BEFORE ALGORITHM STARTS
    def update_neighbors(self, grid): 
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

#FUNCTION TO FIND TAXI-CAB DISTANCE
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

#SHOWS SHORTEST PATH
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


###############################################################################################
# ALGORITHMS FOR SEACHING
###############################################################################################

#A* ALGORITHM
def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() #SET THAT RETURNS THE NODE WITH SMALLEST VALUE WHEN CALLED
    open_set.put((0, count, start))
    came_from = {} #RECORDS PATH FROM PREVIOUS NODE
    g_score = {node: float("inf") for row in grid for node in row} #DISTANCE FROM THE START
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row} #DISTANCE FROM THE END
    f_score[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start} #SEARCHABLE QUEUE SINCE PRIORITYQUEUE DOESN'T ALLOW US TO

    while not open_set.empty(): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        #SHOWS SHORTEST PATH
        if current == end: 
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 #ONE SPACE AWAY FROM CURRENT NODE
            #REROUTES PATH AND UPDATES VALUE IF CLOSER PATH FOUND
            if temp_g_score < g_score[neighbor]: 
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                #OPENS PATH OPTION IN NODE IF IT WAS UNEXPLORED
                if neighbor not in open_set_hash: 
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

#DIJKSTRA'S ALGORITHM
def dijkstra(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue() #SET THAT RETURNS THE NODE WITH SMALELST VALUE WHEN CALLED
    open_set.put((0, count, start))
    came_from = {} #RECORDS PATH FROM PREVIOUS NODE
    g_score = {node: float("inf") for row in grid for node in row} #DISTANCE FROM THE START
    g_score[start] = 0
    open_set_hash = {start} #SEARCHABLE QUEUE SINCE PRIORITYQUEUE DOESN'T ALLOW US TO

    while not open_set.empty(): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        #SHOWS SHORTEST PATH
        if current == end: 
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 #ONE SPACE AWAY FROM CURRENT NODE
            #REROUTES PATH AND UPDATES VALUE IF CLOSER PATH FOUND
            if temp_g_score < g_score[neighbor]: 
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                #OPENS PATH OPTION IN NODE IF IT WAS UNEXPLORED
                if neighbor not in open_set_hash: 
                    count += 1
                    open_set.put((g_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()

#DEPTH FIRST SEARCH ALGORITHM
def dfs(draw, grid, start, end):
    count = 0
    open_set = LifoQueue() #LAST IN FIRST OUT QUEUE TO AGGRESIVELY SEARCH
    open_set.put((count, start))
    came_from = {} #KEEPS TRACK OF WHERE EACH EXPLORED NODE CAME FROM
    open_set_hash = {start} #LIST OF EXPLORED NODES

    while not open_set.empty(): 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[1]
    
        #SHOWS FOUND PATH
        if current == end: 
            reconstruct_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        #PUTS EACH AVAILABLE NEIGHBOR OF CURRENT NODE INTO LIFO QUEUE
        for neighbor in current.neighbors: 
            if not neighbor in open_set_hash:
                came_from[neighbor] = current 
            if neighbor not in open_set_hash: 
                    count += 1
                    open_set.put((count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()


###############################################################################################
# FUNCTIONS TO USE
###############################################################################################

#MAKES AREA FOR GRID SPACES
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

#DRAWS LINES TO VISUALLY DEFINE GRIDS
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
    for j in range(rows):
        pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

#FILLS GRID WITH COLOR WHEN CLICKED AND UPDATES ENTIRE SCREEN
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

#TAKES PIXEL LOCATION AND DETERMINES GRID LOCATION
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

#COUNT PATH LENGTH   
def path_length(grid):
    path_count = 0
    for row in grid:
        for node in row:
            if node.is_path():
                path_count += 1
    return path_count

#DETERMINES IF A PATH WAS FOUND   
def path_stats(grid, start_time):
    for row in grid:
        for node in row:
            if node.is_path():
                print("--- %.2f seconds and %i path blocks ---" % ((time.time() - start_time), path_length(grid)))
                return
    print("No Path Was Found...")

#SAVES THE MAZE FILE
def save_mazefile(row, grid, node):
    try:
        #PROCESS TO STORE BARRIER LAYOUT IN THE FILE
        mazeLayout = [] 
        for row in grid:
            for node in row:
                if node.is_barrier():
                    mazeLayout.append("1")
                else:
                    mazeLayout.append("4")
        
        #Export data to pickle file with user choice of save location
        files = [('Pickle File', '*.pickle')]
        filename = tkf.asksaveasfilename(filetypes = files, defaultextension = files)
        with open(filename, 'wb') as f:
            pickle.dump(mazeLayout, f)
        print("Successfully saved the file.")

    except FileNotFoundError:
        print("Saving file failed. Reason: Aborted save process.")
    except:
        print("Saving file failed.")

#LOADS MAZE ONTO BOARD
def loading_maze(grid, mazeLayout):
    i = 0 
    for row in grid:
        for node in row:
            if mazeLayout[i] == '1':
                node.make_barrier()
            else:
                node.reset()
            i+=1

#LOADS A MAZE FROM SELECTED FILE
def load_mazefile(grid):
    try:
        #USING TKINTER TO OPEN INTERFACE TO SELECT FILE
        files = [('Pickle File', '*.pickle')]
        filename = tkf.askopenfilename(filetypes = files, defaultextension = files)
        with open(filename, 'rb') as f:
            mazeLayout = pickle.load(f)
        
        #PROCESS TO BUILD MAZE BY READING FILE
        loading_maze(grid, mazeLayout)
        print("Successfully opened the maze layout file.")
    except FileNotFoundError:
        print("Opening file failed. Reason: Aborted opening process.")
    except:
        print("Opening file failed.")

# Instructions on use
def say_usermanual():
    print("")
    print("Welcome to the pathfinding algorithm visualizer by Jeffrey Collier!")
    print("---------------------------------------------------------------------")
    print("Current version: %s" % version)
    print("Last updated: %s" % lastUpdate)
    print("---------------------------------------------------------------------")
    print("• Your first left mouse click will place the start node, second click will place the end node, and then any remaining clicks will place walls.")
    print("• Your right mouse click will remove selected node.")
    print("• Keyboard press \"1\" runs the A* search algorithm.")
    print("• Keyboard press \"2\" runs the Dijkstra's algorithm.")
    print("• Keyboard press \"3\" runs the Depth-first search algorithm.")
    print("• Keyboard press \"R\" loads a random preloaded maze.")
    print("• Keyboard press \"C\" clears the board.")
    print("• Keyboard press \"S\" saves your current board layout.")
    print("• Keyboard press \"L\" loads a saved board layout.")
    print("• Keyboard press \"H\" prints this menu again for help.")

#LOADING A RANDOM PRELOADED MAZE
numberMemmory = [0]
def load_randomMaze(grid):
    try:
        lastNumber = numberMemmory.pop()
        
        currentNumber = random.randint(0,2)
        while currentNumber == lastNumber:
            currentNumber = random.randint(0,2)
        numberMemmory.append(currentNumber)
        
        listofmazes = [mazes.maze1, mazes.maze2, mazes.maze3]
        mazeLayout = listofmazes[currentNumber]
        loading_maze(grid, mazeLayout)
        print("Successfully loaded a random preloaded maze.")
    except Exception as e:
        print("Error: failed loading a random preloaded maze.")
        print(e)


###############################################################################################
# MAIN GAME LOOP
###############################################################################################

def main(win, width):
    say_usermanual()
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None #start node
    end = None #end node
    locked = False #board lock

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get(): 
            #QUITS PROGRAM IF REQUESTED
            if event.type == pygame.QUIT:
                run = False

            #CLEARS BOARD IF NEW ALGORITHM IS STARTED OR MOUSE BUTTON IS CLICKED
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2] or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_1) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_2) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_3):
                    if locked:
                        locked = False
                        for row in grid:
                            for node in row:
                                if node.is_open() or node.is_closed() or node.is_path():
                                    node.reset()
                    
            #CREATES START, END, AND BARRIER NODES            
            if pygame.mouse.get_pressed()[0]: #LEFT MOUSE CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            #RESETS NODES WITH MOUSE CLICK
            elif pygame.mouse.get_pressed()[2]: #RIGHT MOUSE CLICK
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            #KEYBOARD COMMANDS
            if event.type == pygame.KEYDOWN:
                #A* STAR ALGORITHM
                if event.key == pygame.K_1 and start and end: #RUNS PROGRAM
                    start_time = time.time()
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    locked = True
                    path_stats(grid, start_time)  
                
                #DIJKSTRA'S ALGORITHM
                if event.key == pygame.K_2 and start and end: #RUNS PROGRAM
                    start_time = time.time()
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    locked = True
                    path_stats(grid, start_time)
                
                #DEPTH FIRST SEARCH ALGORITHM
                if event.key == pygame.K_3 and start and end: #RUNS PROGRAM
                    start_time = time.time()
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    dfs(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    locked = True
                    path_stats(grid, start_time)
                
                #LOADING A SAVED MAZE FILE ONTO BOARD
                if event.key == pygame.K_l: 
                    grid = make_grid(ROWS, width)
                    start = None
                    end = None
                    load_mazefile(grid)
                
                #SAVING A MAZE BOARD INTO A FILE
                if event.key == pygame.K_s: 
                    save_mazefile(row, grid, node)

                #CLEARS THE GRID BOARD
                if event.key == pygame.K_c: 
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                #PRINTS THE HELP MENU
                if event.key == pygame.K_h: 
                    say_usermanual()

                #LOADS A RANDOM MAZE
                if event.key == pygame.K_r:
                    grid = make_grid(ROWS, width)
                    start = None
                    end = None
                    load_randomMaze(grid)

    pygame.quit()
main(WIN, WIDTH)