import os
import pygame
import neat 
import time 
import ground
import pipe
from bird import Bird
from ground import Ground
from pipe import Pipe

pygame.display.set_caption("Flappy Bird Clone")
pygame.font.init()

WIDTH = 570
HEIGHT = 800

CSANS_FONT = pygame.font.SysFont("comicsans", 50)
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))


def setup():
    window = pygame.display.set_mode((WIDTH,HEIGHT))

    player = Bird(200,200)
    base = Ground(HEIGHT-ground.GROUND_IMG.get_height()/2)
    pipes = [Pipe(700)]
    running = True
    simulation_speed = 30

    clock = pygame.time.Clock()

    add_pipe = False
    while running:
        clock.tick(simulation_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        player.update()
        base.update()
        for pipe in pipes:
            if pipe.collide(player):
                   print("you lose") # no real game end 
                
            if not pipe.passed and pipe.x < player.x:
                pipe.passed = True
                add_pipe = True

            if pipe.x + pipe.img.get_width() < 0 :
                pipes.remove(pipe)

            if add_pipe:
                pipes.append(Pipe(700))
                add_pipe = False
                
            pipe.update()

        draw(window,player,base,pipes)
        

def draw(window,player,base,pipes):
    window.blit(BG_IMG, (0,0))

    base.draw(window)
    player.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    pygame.display.update()


if __name__ == "__main__":
    setup()
    