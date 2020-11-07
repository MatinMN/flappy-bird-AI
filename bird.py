import pygame
import os

# 32 x 24 scaled 2x
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))
]

class Bird:
    images = BIRD_IMGS
    angle = 0
    rotation_velocity = 0
    rotatation_acc = 0.7
    max_rotation_speed = 20
    jump_speed = 130
    animation_speed = 5
    animation_counter = 0
    current_animation_frame = 0
    y_velocity = 0
    gravity = 0.8
    max_y_velocity = 13

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = self.images[0]
    
    def update(self):
        self.update_animation()
        self.apply_gravity()

        self.rotation_velocity -= self.rotatation_acc 

        if self.rotation_velocity >= self.max_rotation_speed:
            self.rotation_velocity = self.max_rotation_speed
        elif self.rotation_velocity <= -self.max_rotation_speed:
            self.rotation_velocity = -self.max_rotation_speed

        self.angle += self.rotation_velocity
        
        if self.angle <= -45:
            self.angle = -45
        elif self.angle >= 45:
            self.angle = 45


        self.y += self.y_velocity

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

    def apply_gravity(self):
        self.y_velocity += self.gravity

        if self.y_velocity >= self.max_y_velocity :
            self.y_velocity = self.max_y_velocity
        elif self.y_velocity <= -self.max_y_velocity :
            self.y_velocity = -self.max_y_velocity

    def jump(self):
        self.y_velocity -= self.jump_speed
        self.rotation_velocity = self.max_rotation_speed/1.7 #counter act the fall roation
        if self.y_velocity <= -300:
            self.y_velocity = -300

    def update_animation(self):
        self.animation_counter += 1 # not using delta time so we can speed simulation for model training

        if self.animation_counter > self.animation_speed:
            if self.current_animation_frame >= len(self.images):
                self.current_animation_frame = 0

            self.img = self.images[self.current_animation_frame]

            self.current_animation_frame += 1
            self.animation_counter = 0 #reset animation cycle


    def draw(self, window):
        rotated_image = pygame.transform.rotate(self.img,self.angle)

        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)

        window.blit(rotated_image,new_rect.topleft)

