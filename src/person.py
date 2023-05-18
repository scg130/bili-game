import pygame
import random
import time


width = 800
height = 560
width_center = (0, 730)
height_center = (280, 490)
font_size = 10
move = 20
people = {}

class Person:
    def __init__(self, id, name, font, raw_pic):
        self.id = id
        self.name = self.create_name(name, font)
        self.w = random.randint(*width_center)
        self.h = random.randint(*height_center)
        self.person_size = int((self.h + 70) / height * 70)
        self.pic = pygame.transform.scale(raw_pic, (self.person_size, self.person_size))
        self.time = time.time()

    def update_active_time(self, ):
        self.time = time.time()

    def if_delete(self, time):
        if time.time() - self.time > 60:
            return True
        else:
            return False

    def create_name(self, name, font):
        if len(name) > 10:
            name = name[:10]
        return font.render(name, True, (0,0,0))

    def change_answer(self, color):
        self.color = color
        self.update_active_time()

    def update(self, word):
        if word == "w":
            self.h = max(0, self.h - move)
            self.person_size = int((self.h + 70) / height * 70)
        if word == "s":
            self.h = min(height, self.h + move)
            self.person_size = int((self.h + 70) / height * 70)
        if word == "a":
            self.w = max(0, self.w - move)
            self.person_size = int((self.h + 70) / height * 70)
        if word == "d":
            self.w = min(width, self.w + move)
            self.person_size = int((self.h + 70) / height * 70)    
        