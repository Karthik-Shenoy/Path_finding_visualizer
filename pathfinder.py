import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, Radiobutton
import os


screen = pygame.display.set_mode((700, 700))

class spot:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.previous = None
        self.obs = False
        self.closed = False
        self.visited = False
        self.value = 1

    def show(self, color, no_fill):
        if self.closed == False :
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), no_fill)
            pygame.display.update()

    def path(self, color, no_fill):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), no_fill)
        pygame.display.update()

    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < cols-1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row-1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])


cols = 50
grid = [0 for i in range(cols)]
row = 50
openSet = []
closedSet = []
box_color = (233,234,236)
yellow = ((252,228,4))
orange = ((244,91,24))
blue = (81,172,122)
grey = (64, 62, 60)
path = (81,172,122)
w = 700 / cols
h = 700 / row
cameFrom = []



# create 2d array
for i in range(cols):
    grid[i] = [0 for i in range(row)]

# Create Spots
for i in range(cols):
    for j in range(row):
        grid[i][j] = spot(i, j)


# Set start and end node
start = grid[12][5]
end = grid[3][6]
# SHOW RECT
for i in range(cols):
    for j in range(row):
        grid[i][j].show(box_color, 0)

for i in range(0,row):
    grid[0][i].show(grey, 0)
    grid[0][i].obs = True
    grid[cols-1][i].obs = True
    grid[cols-1][i].show(grey, 0)
    grid[i][row-1].show(grey, 0)
    grid[i][0].show(grey, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True

def onsubmit():
    global start
    global end
    start_coordinates = startBox.get().split(',')
    end_coordinates = endBox.get().split(',')
    start = grid[int(start_coordinates[0])][int(start_coordinates[1])]
    end = grid[int(end_coordinates[0])][int(end_coordinates[1])]
    window.quit()
    window.destroy()

window = Tk()
label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

algorithm = IntVar()


label2 = Label(text = "default algorithm : A*-algorithm")
Dijkstras = Radiobutton(window, text='dijkstras :', variable=algorithm, value = 1)
A_star = Radiobutton(window, text='A* Algorithm :', variable=algorithm, value =2)
BFS = Radiobutton(window, text='Breadth first search :', variable=algorithm, value = 3)

submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=2)
label2.grid(columnspan=2, row=3)
Dijkstras.grid(columnspan=2, row=4)
A_star.grid(columnspan=2, row=5)
BFS.grid(columnspan=2, row=6)
submit.grid(columnspan=2, row=7)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)

window.update()
mainloop()

pygame.init()
openSet.append(start)

def mousePress(x):
    pos_x = x[0]
    pos_y = x[1]
    g1 = pos_x // (700 // cols)
    g2 = pos_y // (700 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show((0, 0, 0), 0)

end.show((255, 0, 0), 0)
start.show((255, 0, 0), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(cols):
    for j in range(row):
        grid[i][j].addNeighbors(grid)

def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    #d = abs(n.i - e.i) + abs(n.j - e.j)
    return d


def A_star():
    end.show((255, 0, 0), 0)
    start.show((255, 0, 0), 0)
    initiate=1
    if len(openSet) > 0:
        lowestIndex = 0
        for i in range(len(openSet)):
            if openSet[i].f < openSet[lowestIndex].f:
                lowestIndex = i
        initiate = 0
        current = openSet[lowestIndex]


        ########################## Back Track ###########################################################
        if current == end:
            print('done', current.f)
            start.show((255,0,0),0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show(path, 0)
                current = current.previous
            end.show((255, 0, 0), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', ("A_star algorithm computed the shortest distance \n to Be " + str(temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable,sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        openSet.pop(lowestIndex)
        closedSet.append(current)
        ########################## Back Track ###########################################################

        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tempG = current.g + current.value
                if neighbor in openSet:
                    if neighbor.g > tempG:
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    openSet.append(neighbor)

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous == None:
                neighbor.previous = current
    if var.get():
        for i in range(len(openSet)):
            openSet[i].show(orange, 0)

        for i in range(len(closedSet)):
            if closedSet[i] != start:
                closedSet[i].show(yellow, 0)

    if(initiate):
        Tk().wm_withdraw()
        result = messagebox.askokcancel("Done", ("No Path Found"))
        if result == True:
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            ag = True
            while ag:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.KEYDOWN:
                        ag = False
                        break
        pygame.quit()
    current.closed = True




######### Dijkstras Algorithm ###################
queue = []
queue.append(start)
deque = []
def dijkstras():


    initiate = 1
    if len(queue)>0:
        lowest_index = 0
        ##
        q_dex = {}
        ##
        for i in range((len(queue))):
            q_dex[(queue[i].i, queue[i].j)] = queue[i].g
            if(queue[i].g<queue[lowest_index].g):
                lowest_index = i
        current = queue[lowest_index]
        initiate = 0

        ###### Back_track #########
        if current == end:
            temp = current.g
            start.show((255,0,0), 0)
            for i in range(current.g):
                current.closed = False
                current.show(path, 0)
                current = current.previous
            end.show((255, 0, 0), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', (
                        "Dijkstra's algorithm computed, the shortest distance \n to Be " + str(
                    temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        ###### Back_track #########

        queue.pop(lowest_index)
        deque.append(current)
        neighbors = current.neighbors
        ####
        n_dex = []
        ####
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            n_dex.append((neighbor.i, neighbor.j))
            if neighbor not in deque:
                tempG = current.g + current.value
                if neighbor in queue:
                    if(neighbor.g>tempG):
                        neighbor.g = tempG
                else:
                    neighbor.g = tempG
                    queue.append(neighbor)

            if(neighbor.previous == None):
                neighbor.previous = current
    if (var.get()):
        for i in range(len(queue)):
            queue[i].show(orange, 0)
        for i in range(len(deque)):
            if (deque[i] != start):
                deque[i].show(yellow, 0)
    if (initiate):
        Tk().wm_withdraw()
        result = messagebox.askokcancel("Done", ("No Path Found"))
        if result == True:
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            ag = True
            while ag:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.KEYDOWN:
                        ag = False
                        break
        pygame.quit()
    current.closed=True



breadth_set = []
update_set = []
breadth_set.append(start)
start.visited = True
def breadth_first_search():
    initiate =1
    if len(breadth_set) > 0 :
        current = breadth_set[0]
        initiate = 0
        ################## back-track #################################
        if current == end:
            print("found")
            temp = 1
            previous = current.previous
            start.show((255,0,0),0)
            previous.show(path, 0)
            while previous!=start:
                temp+=1
                previous.closed = False
                previous.show(path, 0)
                previous = previous.previous
            end.show((255,0,0),0)
            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', (
                    "Breadth first search algorithm computed, the shortest distance \n to Be " + str(
                temp) + ' blocks away, \n would you like to re run the program?'))
            if result == True:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()
        ################## back-track #################################
        breadth_set.pop(0)
        update_set.append(current)
        neighbors = current.neighbors
        for i in range(len(neighbors)):
            neighbor = neighbors[i]
            if neighbor.visited == False:
                breadth_set.append(neighbor)
                neighbor.visited = True
            if(neighbor.previous == None):
                neighbor.previous = current
    if(var.get()):
        for i in  range(len(breadth_set)):
            breadth_set[i].show(orange, 0)
        for i in range(len(update_set)):
            if(update_set[i]!=start):
                update_set[i].show(yellow, 0)
    if (initiate):
        Tk().wm_withdraw()
        result = messagebox.askokcancel("Done", ("No Path Found"))
        if result == True:
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            ag = True
            while ag:
                ev = pygame.event.get()
                for event in ev:
                    if event.type == pygame.KEYDOWN:
                        ag = False
                        break
        pygame.quit()
        current.closed = True











while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    pygame.display.update()
    if algorithm.get()==1:
        dijkstras()
    elif algorithm.get()==2:
        A_star()
    elif algorithm.get()==3:
        breadth_first_search()
    else:
        A_star()



