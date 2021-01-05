import pygame
import os
iks = pygame.image.load(os.path.join('resursi', 'iks150x150.png'))
oks = pygame.image.load(os.path.join('resursi', 'oks150x150.png'))

class Grid:
    def __init__(self):
        self.grid_lines = [((0, 150), (600, 150)),  # prva horizontalna linija
                           ((0, 300), (600, 300)),  # druga -||-
                           ((0, 450), (600, 450)),
                           ((150, 0), (150, 600)),  # prva vertikalna
                           ((300, 0), (300, 600)),
                           ((450, 0), (450, 600))]  # druga vetrikalna

        self.grid = [[0 for x in range (4)] for y in range(4)] # matrika 3x3, za vsak Y naredim 3 X in vrednost X nastavim na 0
        #print(self.grid)
        self.switchPlayer = True
        #................UP......UPLEFT....LEFT.....DLEFT...DOWN....DRIGHT..RIGHT...UPRIGHT
        self.search = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]
        self.game_over = False

#metoda za risanje linij
    def draw(self, surface):
        for line in self.grid_lines:
            pygame.draw.line(surface, (90,90,90), line[0], line[1], 2)

        for y in range(len(self.grid)): #gre skozi vsak element zunanjih elementov matrike
            for x in range(len(self.grid[y])): #gre skozi vsak elemenit notranjih elementov matrike
                if self.get_cell_value(x, y) == "X":
                    surface.blit(iks, (x*150, y*150))
                elif self.get_cell_value(x, y) == "O":
                     surface.blit(oks, (x*150, y*150))

#geter
    def get_cell_value(self, x, y):
        return self.grid[y][x]
#seter
    def set_cell_value(self, x, y, value):
        self.grid[y][x] = value

    def get_mouse(self, x, y, player):
        if self.get_cell_value(x, y) == 0:
            self.set_cell_value(x, y, player)
            self.preveri_polje(x, y, player)
        else:
            self.switchPlayer = False

    def a_je_v_meji(self, x, y):
        return x >= 0 and x < 4 and y >= 0 and y < 4

    def preveri_polje(self, x, y, player):
        count = 1
        for index, (dirx, diry) in enumerate(self.search):
            if self.a_je_v_meji(x + dirx, y + diry) and self.get_cell_value(x + dirx, y + diry) == player:
                count += 1
                xx = x + dirx
                yy = y + diry
                if self.a_je_v_meji(xx + dirx, yy + diry) and self.get_cell_value(xx + dirx, yy + diry) == player:
                    count += 1
                    if count == 3:
                        break
                if count < 3:
                    new_dir = 0

                    if index == 0:
                        new_dir = self.search[4]  # UP to DOWN
                    elif index == 1:
                        new_dir = self.search[5]
                    elif index == 2:
                        new_dir = self.search[6]
                    elif index == 3:
                        new_dir = self.search[7]
                    elif index == 4:
                        new_dir = self.search[0]
                    elif index == 5:
                        new_dir = self.search[1]
                    elif index == 6:
                        new_dir = self.search[2]
                    elif index == 7:
                        new_dir = self.search[3]

                    if self.a_je_v_meji(x + new_dir[0], y + new_dir[1]) \
                            and self.get_cell_value(x + new_dir[0], y + new_dir[1]) == player:
                        count += 1
                        if count == 3:
                            break
                    else:
                        count = 1

        if count == 3:
            print(player, 'Pobedio!')
            self.game_over = True
        else:
            self.game_over = self.if_grid_is_full()
            if self.if_grid_is_full():
                print('Nima pobednika')

    def if_grid_is_full(self):
        for row in self.grid:
            for value in row:
                if value == 0:
                    return False
        return True

    def playVsComputer(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.get_cell_value(x, y) == False:
                    value = oks
                    break

    def clear_grid(self):
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.set_cell_value(x, y, 0)

    def printGrid(self):
        for row in self.grid:
            print(row)