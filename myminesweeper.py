import pygame
from pygame import gfxdraw
import numpy as np
import pygame.freetype
from timeit import default_timer as timer

pygame.init()
gameDisplay = pygame.display.set_mode((600, 600))
FONT = pygame.freetype.SysFont("Courier New", 14, bold=True)
SUB_FONT = pygame.freetype.SysFont("", 26)
colours = [(0, 0, 0), (4, 0, 255), (0, 148, 32), (224, 7, 7), (0, 5, 94), (94, 0, 0), (50, 156, 143),
           (0, 0, 0), (100, 100, 100)]
WIN_FONT = pygame.freetype.SysFont("", 120)
pause = False


class Square(pygame.rect.Rect):
    def __init__(self, x, y):
        super()
        self.x = x
        self.y = y
        self.w = 20
        self.h = 20
        self.bomb = Square.bombs()
        self.bombs_close = 0
        self.open = False
        self.visited = False
        self.x_index = 0
        self.y_index = 0
        self.safe = False

    def show(self, display):
        if self.open and not self.safe:
            if self.bomb:
                pygame.gfxdraw.filled_circle(display, self.x + 10, self.y + 10, 5, (0, 0, 20))
                pygame.gfxdraw.aacircle(display, self.x + 10, self.y + 10, 5, (0, 0, 20))
            else:
                pygame.draw.rect(display, (200, 200, 200), self)
                pygame.draw.rect(display, (100, 100, 100), self, 1)
                if self.bombs_close > 0:
                    FONT.render_to(display, (self.x + 7, self.y + 5), str(self.bombs_close), colours[self.bombs_close])

        else:
            pygame.draw.rect(display, (150, 150, 150), self)
            pygame.draw.rect(display, (100, 100, 100), self, 1)
            if self.bomb and bomb_found is not None:
                pygame.gfxdraw.filled_circle(display, self.x + 10, self.y + 10, 5, (0, 0, 20))
                pygame.gfxdraw.aacircle(display, self.x + 10, self.y + 10, 5, (0, 0, 20))
            if self.safe:
                pygame.draw.rect(display, (77, 51, 34, 200), [self.x + 4, self.y + 4, 2, 12])
                pygame.gfxdraw.filled_polygon(display, [(self.x + 6, self.y + 4), (self.x + 15, self.y + 7),
                                                        (self.x + 6, self.y + 10)], (245, 30, 0, 175))
                pygame.gfxdraw.aapolygon(display, [(self.x + 6, self.y + 4), (self.x + 15, self.y + 7),
                                                   (self.x + 6, self.y + 10)], (245, 30, 0, 175))
        if self.safe and self.open and not self.bomb:
            pygame.draw.aaline(display, (255, 0, 0), (s.x, s.y), (s.x + w, s.y + h))
            pygame.draw.aaline(display, (255, 0, 0), (s.x + w, s.y), (s.x, s.y + h))

    @staticmethod
    def bombs():
        return np.random.uniform(0, 10) < 1.3


gameEnd = False

w, h = 20, 20

grid = []
grid_size = 30


def load_game():
    for i1 in range(grid_size):
        row1 = []
        for j1 in range(grid_size):
            s1 = Square(j1 * w, i1 * w)
            s1.x_index = i1
            s1.y_index = j1
            row1.append(s1)
        grid.append(row1)

    for i in range(grid_size):
        for j in range(grid_size):
            count = 0
            if not grid[i][j].bomb:
                n = neighbours(grid[i][j])

                for q in range(len(n)):
                    count += n[q].bomb

                grid[i][j].bombs_close = count


def uncover(cell3):
    cell3.visited = True
    cell3.open = True
    all_visited = True
    for n_square in neighbours(cell3):
        if n_square.bombs_close > 0 and not n_square.safe:
            n_square.open = True
            n_square.visited = True
        if n_square.bombs_close == 0 and not n_square.visited and not n_square.safe:
            n_square.open = True
            n_square.visited = True
            uncover(n_square)
        elif n_square.bombs_close >= 0 and n_square.safe:
            n_square.visited = True

        for bordering_square in neighbours(n_square):
            if not (bordering_square.visited or bordering_square.safe):
                all_visited = False

    if all_visited:
        return


def neighbours(cell2):
    x = cell2.x_index
    y = cell2.y_index
    if x == 0 and y == 0:
        return [grid[x][y+1], grid[x+1][y+1], grid[x+1][y]]
    elif x == 0 and 0 < y < grid_size - 1:
        return [grid[x][y+1], grid[x+1][y+1], grid[x+1][y], grid[x+1][y-1], grid[x][y-1]]
    elif x == 0 and y == grid_size - 1:
        return [grid[x+1][y], grid[x+1][y-1], grid[x][y-1]]
    elif 0 < x < grid_size - 1 and y == grid_size - 1:
        return [grid[x-1][y], grid[x-1][y-1], grid[x][y-1], grid[x+1][y-1], grid[x+1][y]]
    elif x == grid_size - 1 and y == grid_size - 1:
        return [grid[x-1][y], grid[x-1][y-1], grid[x][y-1]]
    elif x == grid_size - 1 and 0 < y < grid_size - 1:
        return [grid[x-1][y], grid[x-1][y-1], grid[x][y-1], grid[x-1][y+1], grid[x][y+1]]
    elif x == grid_size - 1 and y == 0:
        return [grid[x-1][y], grid[x-1][y+1], grid[x][y+1]]
    elif 0 < x < grid_size - 1 and y == 0:
        return [grid[x-1][y], grid[x-1][y+1], grid[x][y+1], grid[x+1][y+1], grid[x+1][y]]
    elif 0 < x < grid_size - 1 and 0 < y < grid_size - 1:
        return [grid[x-1][y], grid[x-1][y+1], grid[x][y+1], grid[x+1][y+1],
                grid[x+1][y], grid[x+1][y-1], grid[x][y-1], grid[x-1][y-1]]


def check_win():
    for row5 in grid:
        for s5 in row5:
            if not s5.bomb and not s5.open:
                return False
    return True


gameDisplay.fill((0, 0, 0))

bomb_found = None

begin_game = True

can_start = False

stop_timer = False

load_game()

pause_list = []

start_time = 0
end_time = 0

win = False

while not gameEnd:

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and begin_game\
                and 0 < event.pos[0] < 600 and 0 < event.pos[1] < 600:
            begin_game = False
            break_bool = False
            x_pos, y_pos = 0, 0
            for row4 in grid:
                for s4 in row4:
                    if s4.collidepoint(event.pos):
                        x_pos = s4.x_index
                        y_pos = s4.y_index
                        break_bool = True
                        break

                if break_bool:
                    break

            while grid[x_pos][y_pos].bomb or grid[x_pos][y_pos].bombs_close > 0:
                grid.clear()
                load_game()

            start_time = timer()

        if event.type == pygame.QUIT:
            gameEnd = True
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and bomb_found is None and not pause and not win:
            if event.button == 1:
                for row in grid:
                    for c in row:
                        if c.collidepoint(event.pos) and not c.safe:
                            if not c.bomb and c.bombs_close == 0:
                                uncover(c)
                            elif c.bomb:
                                bomb_found = c
                            elif c.bombs_close > 0:
                                c.open = True
                        if bomb_found is not None:
                            c.open = True
            elif event.button == 3:
                for row in grid:
                    for c in row:
                        if c.collidepoint(event.pos) and not c.open:
                            c.safe = not c.safe

            if bomb_found is not None:
                exit_loop = False
                for row in grid:
                    for cell in row:
                        cell.open = True
                        if cell.x_index == bomb_found.x_index and cell.y_index == bomb_found.y_index:
                            break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and bomb_found is None and not win:
                pause = not pause
                pause_list.append(timer())

    if not pause and not win:
        for row in grid:
            for s in row:
                if not pause:
                    s.show(gameDisplay)
    elif not win:
        gameDisplay.fill((255, 255, 255))
        WIN_FONT.render_to(gameDisplay, (60, 150), "paused.", (30, 30, 30))

    if check_win() and bomb_found is None:
        pause = False
        if stop_timer is False:
            end_time = timer()
            stop_timer = True
        colour1 = np.random.randint(0, 3)  # directs which rgb value set to 255
        colour2 = [e for e in [0, 1, 2] if e != colour1][np.random.randint(0, 2)]  # 0 rgb value
        colour3 = [e for e in [0, 1, 2] if e not in (colour1, colour2)][0]  # random rgb value

        win_colours = [0, 0, 0]
        win_colours[colour1] = 255
        win_colours[colour2] = 0
        win_colours[colour3] = np.random.randint(0, 256)

        pause_time = 0

        for i in range(len(pause_list)):
            pause_time += ((-1)**(i+1))*pause_list[i]

        WIN_FONT.render_to(gameDisplay, (50, 50), "You Win!", win_colours)

        if not win:
            final_time = end_time - start_time - pause_time
            time_end = str(round(final_time, 2)) + "s"
            WIN_FONT.render_to(gameDisplay, (200, 300), time_end, (0, 0, 0))

            f = open("minesweeper_times.txt", "a+")
            f.write(time_end + "\n")
            f.close()
            f = open("minesweeper_times.txt", "r+")

            best_times = [line.strip("\n") for line in f]
            f.close()
            print(type(f))
            print("best times ", best_times)
            best_times.sort()
            best_time = best_times[0]

            SUB_FONT.render_to(gameDisplay, (210, 430), "Best time: " + best_time, (0, 0, 0))
            win = True

    pygame.display.update()
