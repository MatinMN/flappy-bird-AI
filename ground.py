import pygame
import os

GROUND_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","ground.png")))

class Ground:
    velocity = 5
    width = GROUND_IMG.get_width()
    img = GROUND_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

    def update(self):
        self.x1 -= self.velocity
        self.x2 -= self.velocity

        if (self.x1 + self.width < 0):
            self.x1 = self.x2 + self.width
        if (self.x2 + self.width < 0):
            self.x2 = self.x1 + self.width

    def draw(self,window):
        window.blit(self.img,(self.x1,self.y))
        window.blit(self.img,(self.x2,self.y))