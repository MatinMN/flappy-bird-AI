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
generation = 0

def setup(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True)) # add stats
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    best_model = population.run(train_model,100)
        

def train_model(genomes, config):
    global generation
    nets = []
    ge = []
    birds = []

    generation += 1

    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        birds.append(Bird(200,200))
        g.fitness = 0
        ge.append(g)

    window = pygame.display.set_mode((WIDTH,HEIGHT))

    base = Ground(HEIGHT-ground.GROUND_IMG.get_height()/2)
    pipes = [Pipe(700)]
    running = True
    simulation_speed = 30

    clock = pygame.time.Clock()

    add_pipe = False
    score = 0
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

        pipe_index = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].img.get_width():
                pipe_index = 1
        else:
            running = False
            break #end generation
        
        base.update()

        for index, bird in enumerate(birds):
            bird.update()
            ge[index].fitness += 0.3

            output = nets[index].activate((bird.y,abs(bird.y - pipes[pipe_index].height), abs(bird.y - pipes[pipe_index].bottom)))

            if output[0] > 0.5 :
                bird.jump()

        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[index].fitness =- 0.5
                    birds.pop(index)
                    nets.pop(index)
                    ge.pop(index)
                
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.img.get_width() < 0 :
                pipes.remove(pipe)

            if add_pipe:
                score += 1 
                for g in ge:
                    g.fitness += 5
                pipes.append(Pipe(700))
                add_pipe = False
                
            pipe.update()

            for index,bird in enumerate(birds):
                if bird.y + bird.img.get_height() >= HEIGHT - 100 or bird.y < 0:
                    bird.y = HEIGHT- bird.img.get_height() - 100
                    birds.pop(index)
                    nets.pop(index)
                    ge.pop(index)

        draw(window,birds,base,pipes,score,generation)

def draw(window,birds,base,pipes,score,generation):
    window.blit(BG_IMG, (0,0))

    base.draw(window)

    for index,bird in enumerate(birds):
        bird.draw(window)

    for pipe in pipes:
        pipe.draw(window)

    text = CSANS_FONT.render("Score : " + str(score), 1 , (255,255,255))
    window.blit(text,(WIDTH-10 - text.get_width(),10))
    text = CSANS_FONT.render("Generation : " + str(generation), 1 , (255,255,255))
    window.blit(text,(10,10)) 

    pygame.display.update()


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neat.config")
    setup(config_path)
    