import pygame
from grid import  Grid
import os
import threading
import socket

try:
    def create_thread(target):
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
except:
    print('Exception occured')

HOST = '127.0.0.1'
PORT = 65432

try:
    sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockett.connect((HOST, PORT))
except:
    print('Exception occured')

try:
    def receive():
        global turn
        while True:
            data = sockett.recv(1024).decode()
            data = data.split('-')
            x, y = int(data[0]), int(data[1])
            if data[2] =='your turn':
                turn = True
            if data[3] == 'False':
                grid.game_over = True
            if grid.get_cell_value(x, y) == 0:
                grid.set_cell_value(x, y, 'X')
except:
    print('Exception occured')
        #print(data)
try:
    create_thread(receive)
except:
    print('Exception occured')

os.environ['SDL_VIDEO_WINDOW_POS'] = '700,100'

surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('Krizec-krozec')

running = True
player = "O"
turn = False
playing = 'True'

grid = Grid()



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.game_over:
            if pygame.mouse.get_pressed()[0]:  # samo sa desnim gumbom
                if turn and not grid.game_over:
                    position = pygame.mouse.get_pos()
                    cellx, celly = position[0] // 150, position[1] // 150
                    grid.get_mouse(cellx, celly, player)
                    if grid.game_over:
                        playing = 'False'
                    try:
                        send_data = '{}-{}-{}-{}'.format(cellx, celly, 'your turn', playing).encode()
                        sockett.send(send_data)
                        turn = False
                    except:
                        print('Exception occured')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.game_over:
                grid.clear_grid()
                grid.game_over = False
                playing = 'True'

            elif event.key == pygame.K_ESCAPE:
                running = False

    surface.fill((0,0,0))
    grid.draw(surface)
    pygame.display.flip()