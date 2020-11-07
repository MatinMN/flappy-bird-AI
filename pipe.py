import pygame
import random
import os

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))

class Pipe:
    gap = 150
    velocity = 5

    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 200

        self.top = 0
        self.bottom = 0

        self.fliped_img = pygame.transform.flip(PIPE_IMG,False,True)
        self.img = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.fliped_img.get_height()
        self.bottom = self.height + self.gap

    def update(self):
        self.x -= self.velocity
    
    def draw(self, window):
        window.blit(self.fliped_img ,(self.x, self.top))
        window.blit(PIPE_IMG,(self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask =  pygame.mask.from_surface(self.fliped_img)
        bottom_mask =  pygame.mask.from_surface(PIPE_IMG)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask,bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if (t_point or b_point):
            return True
        
        return False
