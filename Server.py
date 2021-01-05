import pygame
from grid import  Grid
import os
import threading
import socket

try:
    def create_thread(target):
        thread = threading.Thread(target=target)
        # https://stackoverflow.com/questions/190010/daemon-threads-explanation
        thread.daemon = True
        thread.start()
except:
    print('Exception occured')
# https://realpython.com/python-sockets/
HOST = '127.0.0.1' #localhost
PORT = 65432
connectionEstablished = False
#...............................IPv4.........TCP...........
sockett = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # ustvarim vticnico
sockett.bind((HOST, PORT))
sockett.listen(1)
conn, addr = None, None

try:
    def receive():
        global turn
        while True:
            data = conn.recv(1024).decode()
            data = data.split('-')
            x, y = int(data[0]), int(data[1])
            if data[2] == 'your turn':
                turn = True
            if data[3] == 'False':
                grid.game_over = True
            if grid.get_cell_value(x, y) == 0:
                grid.set_cell_value(x, y, 'O')
except:
    print('Exception occured')

        #print (data)
try:
    def waitingConnetion():
        global connectionEstablished, conn, addr
        conn, addr = sockett.accept()  # caka na konekcijo, ko se konektira, odpre igro
        print('Client se je povezal')
        connectionEstablished = True
        receive()
except:
    print('Exception occured')
try:
    create_thread(waitingConnetion)
except:
    print('Exception occured')

os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'

surface = pygame.display.set_mode((600,600))
pygame.display.set_caption('Krizec-krozec')

running = True
player = "X"
turn = True
playing = 'True'

grid = Grid()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and connectionEstablished:
            if pygame.mouse.get_pressed()[0]:  # samo sa desnim gumbom
                if turn and not grid.game_over:
                    position = pygame.mouse.get_pos()
                    cellX, cellY = position[0] // 150, position[1] // 150 # vsak pravougaonik je 200x200
                    grid.get_mouse(cellX, cellY, player)
                    if grid.game_over:
                        playing = 'False'
                    try:
                        send_data = '{}-{}-{}-{}'.format(cellX, cellY, 'your turn', playing).encode() # formatira v string potem zakodira da lahko posljemo v TCP
                        conn.send(send_data)
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
