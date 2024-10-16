from tkinter import messagebox, Tk
import pygame
import math

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
COLUMNS = 50
ROWS = 50
BOX_WITDH = math.floor(WINDOW_WIDTH / COLUMNS)
BOX_HEIGHT = math.floor(WINDOW_HEIGHT / ROWS)

RGB = "#646464"
RED = "#C80000"
GREEN = "#00C800"
BLUE = "#0000C8"
TURQUOISE = "#00C8C8"
GRAY = "#0A0A0A"
YELLOW = "#C8C800"

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pathfinding Franck Fongang - 2024")

GRID = []
QUEUE = []
PATH = []


class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbours = []

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * BOX_WITDH, self.y * BOX_HEIGHT, BOX_WITDH - 2, BOX_HEIGHT - 2))

    def set_neighbours(self):
        if self.x > 0:
            self.neighbours.append(GRID[self.x - 1][self.y])
        if self.x < COLUMNS - 1:
            self.neighbours.append(GRID[self.x + 1][self.y])
        if self.y > 0:
            self.neighbours.append(GRID[self.x][self.y - 1])
        if self.y < ROWS - 1:
            self.neighbours.append(GRID[self.x][self.y + 1])


for i in range(COLUMNS):
    arr = []
    for j in range(ROWS):
        arr.append(Box(i, j))
    GRID.append(arr)

for i in range(COLUMNS):
    for j in range(ROWS):
        GRID[i][j].set_neighbours()

def draw2():
    window.fill((0, 0, 0))
    for i in range(COLUMNS):
        for j in range(ROWS):
            box = GRID[i][j]
            box.draw(window, (RGB))
            if box.queued:
                box.draw(window, (RED))
            if box.visited:
                box.draw(window, (GREEN))
            if box in PATH:
                box.draw(window, (BLUE))
            if box.start:
                box.draw(window, (TURQUOISE))
            if box.wall:
                box.draw(window, (GRAY))
            if box.target:
                box.draw(window, (YELLOW))


def main():
    begin_search = False
    target_box_set = False
    searching = True
    target_box = None
    start_box_set = False

    run = True
    while run:
        draw2()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    i = math.floor(x / BOX_WITDH)
                    j = math.floor(y / BOX_HEIGHT)
                    if not start_box_set and not GRID[i][j].wall:
                        start_box = GRID[i][j]
                        start_box.start = True
                        start_box.visited = True
                        QUEUE.append(start_box)
                        start_box_set = True
                        
            elif event.type == pygame.MOUSEMOTION:
                x = pygame.mouse.get_pos()[0]
                y = pygame.mouse.get_pos()[1]
                if event.buttons[0]:
                    i = math.floor(x / BOX_WITDH)
                    j = math.floor(y / BOX_HEIGHT)
                    GRID[i][j].wall = True

                if event.buttons[2] and not target_box_set:
                    i = math.floor(x / BOX_WITDH)
                    j = math.floor(y / BOX_HEIGHT)
                    target_box = GRID[i][j]
                    target_box.target = True
                    target_box_set = True
            if event.type == pygame.KEYDOWN and target_box_set:
                begin_search = True

        if begin_search:
            if len(QUEUE) > 0 and searching:
                current_box = QUEUE.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        PATH.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbour in current_box.neighbours:
                        if not neighbour.queued and not neighbour.wall:
                            neighbour.queued = True
                            neighbour.prior = current_box
                            QUEUE.append(neighbour)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "No solution has been found")
                    searching = False

        pygame.display.flip()


if __name__ == "__main__":
    main()