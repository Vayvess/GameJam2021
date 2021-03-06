import os
import sys
import json
import socket
import threading
import pygame as pg

from const import *
from GraphicEngine import GraphicEngine

pg.init()
clock = pg.time.Clock()
screen = pg.display.set_mode(DIM)
pg.display.set_caption("UDP GAME")
font = pg.font.SysFont("comicsansms", 24)

dt = 0
run = True
ge = GraphicEngine(screen, font)
srv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if os.name == 'nt':
    srv.bind(("", 45632))


def handle_srv():
    while run:
        data = srv.recv(DATA_LEN)
        ge.data = json.loads(data.decode("utf-8"))


srv_th = threading.Thread(target=handle_srv)
srv_th.start()
while True:
    left, _, right = False, False, False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            srv.close()
            pg.quit()
            srv_th.join()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            left, _, right = pg.mouse.get_pressed(3)

    inputs = {
        "pos": pg.mouse.get_pos(),
        "ml": left,
        "mr": right
    }

    ge.render(int(clock.get_fps()))
    srv.sendto(json.dumps(inputs).encode("utf-8"), SRV_ADDRESS)
    dt = clock.tick(60)
