import pygame
import random
import time
import multiprocessing
from listen import warp_main
import sys


width = 800
height = 560
width_center = (0, 730)
height_center = (280, 490)
font_size = 10
move = 40
people = {}
size = 70


from PIL import Image
import pygame
from pygame.locals import *
import time

class GIFImage(object):
	"""
		This module is used for displaying gif images.
		filename: The filepath of the input image.
	"""
	def __init__(self, filename):
		self.filename = filename
		self.image = Image.open(filename)
		self.frames = []
		self.get_frames()

		self.cur = 0
		self.ptime = time.time()

		self.running = True
		self.breakpoint = len(self.frames)-1
		self.startpoint = 0
		self.reversed = False

	def get_frames(self):
		image = self.image

		pal = image.getpalette()
		base_palette = []
		for i in range(0, len(pal), 3):
			rgb = pal[i:i+3]
			base_palette.append(rgb)

		all_tiles = []
		try:
			while 1:
				if not image.tile:
					image.seek(0)
				if image.tile:
					all_tiles.append(image.tile[0][3][0])
				image.seek(image.tell()+1)
		except EOFError:
			image.seek(0)

		all_tiles = tuple(set(all_tiles))

		try:
			while 1:
				try:
					duration = image.info["duration"]
				except:
					duration = 100

				duration *= .001 #convert to milliseconds!
				cons = False

				x0, y0, x1, y1 = (0, 0) + image.size
				if image.tile:
					tile = image.tile
				else:
					image.seek(0)
					tile = image.tile
				if len(tile) > 0:
					x0, y0, x1, y1 = tile[0][1]


				if all_tiles:
					if all_tiles in ((6,), (7,)):
						cons = True
						pal = image.getpalette()
						palette = []
						for i in range(0, len(pal), 3):
							rgb = pal[i:i+3]
							palette.append(rgb)
					elif all_tiles in ((7, 8), (8, 7)):
						pal = image.getpalette()
						palette = []
						for i in range(0, len(pal), 3):
							rgb = pal[i:i+3]
							palette.append(rgb)
					else:
						palette = base_palette
				else:
					palette = base_palette


				pi = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
				# pi.set_palette(palette)
				if "transparency" in image.info:
					pi.set_colorkey(image.info["transparency"])
				pi2 = pygame.Surface(image.size, SRCALPHA)
				if cons:
					for i in self.frames:
						pi2.blit(i[0], (0,0))
				pi2.blit(pi, (x0, y0), (x0, y0, x1-x0, y1-y0))

				self.frames.append([pi2, duration])
				image.seek(image.tell()+1)
		except EOFError:
			pass

	def render(self, screen, pos):
		if self.running:
			if time.time() - self.ptime > self.frames[self.cur][1]:
				if self.reversed:
					self.cur -= 1
					if self.cur < self.startpoint:
						self.cur = self.breakpoint
				else:
					self.cur += 1
					if self.cur >= self.breakpoint:
						self.cur = self.startpoint

				self.ptime = time.time()

		screen.blit(self.frames[self.cur][0], pos)

	def seek(self, num):
		self.cur = num
		if self.cur < 0:
			self.cur = 0
		if self.cur >= len(self.frames):
			self.cur = len(self.frames)-1

	def set_bounds(self, start, end):
		if start < 0:
			start = 0
		if start >= len(self.frames):
			start = len(self.frames) - 1
		if end < 0:
			end = 0
		if end >= len(self.frames):
			end = len(self.frames) - 1
		if end < start:
			end = start
		self.startpoint = start
		self.breakpoint = end

	def pause(self):
		self.running = False

	def play(self):
		self.running = True

	def rewind(self):
		self.seek(0)
	def fastforward(self):
		self.seek(self.length()-1)

	def get_height(self):
		return self.image.size[1]
	def get_width(self):
		return self.image.size[0]
	def get_size(self):
		return self.image.size
	def length(self):
		return len(self.frames)
	def reverse(self):
		self.reversed = not self.reversed
	def reset(self):
		self.cur = 0
		self.ptime = time.time()
		self.reversed = False

	def copy(self):
		new = GIFImage(self.filename)
		new.running = self.running
		new.breakpoint = self.breakpoint
		new.startpoint = self.startpoint
		new.cur = self.cur
		new.ptime = self.ptime
		new.reversed = self.reversed
		return new

def create_person(screen, raw_pic, font, name, gif):
    person = Person(name, raw_pic, font,screen, gif)
    people[name] = person


def show_people(screen):
    for name in people:
        if time.time() - people[name].time > 1800:
            people.pop(name)
        # screen.blit(people[name].pic, (people[name].w, people[name].h))
        people[name].gif.render(screen, (people[name].w, people[name].h))

    for name in people:
        screen.blit(people[name].name, (people[name].w+20, people[name].h - 10))


def play_music():
    # music
    pygame.mixer.init()
    pygame.mixer.music.load("music/red_shoes.mp3") # 加载歌曲
    pygame.mixer.music.play(loops = -1) # 播放


def game_init():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('hello world')
    return screen


def RunDemo(queue):
    screen = game_init()

    # pic
    background = pygame.image.load("pic/background.jpeg").convert()
    dijia = pygame.image.load("pic/dijia.png").convert_alpha()
    hulk = GIFImage("pic/avatar.gif")
    # font
    font = pygame.font.Font("font/BOBOHEI-2.otf", font_size)
    # music
    play_music()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        # backgroud
        screen.blit(background, (0, 0))
	
        # people
        if not queue.empty():
            chat = queue.get()
            if chat[0] not in people and chat[1] == "加入":
                create_person(screen, dijia, font, chat[0], hulk)
            if chat[0] in people:
                people[chat[0]].update(chat[1])
        show_people(screen)
        
        # display
        pygame.display.update()


class Person:
    def __init__(self, name, raw_pic, font,screen, gif):
        self.name = font.render(name, True, (255, 255, 255))
        self.w = random.randint(*width_center)
        self.h = random.randint(*height_center)
        self.screen = screen
        self.person_size = int((self.h + size) / height * size)
        self.pic = pygame.transform.scale(raw_pic, (self.person_size, self.person_size))
        self.time = time.time()
        self.gif = gif

    def update(self, word):
        if word == "w":
            self.h = max(0, self.h - move)
            self.person_size = int((self.h + size) / height * size)
        if word == "s":
            self.h = min(height, self.h + move)
            self.person_size = int((self.h + size) / height * size)
        if word == "a":
            self.w = max(0, self.w - move)
            self.person_size = int((self.h + size) / height * size)
        if word == "d":
            self.w = min(width, self.w + move)
            self.person_size = int((self.h + size) / height * size)

if __name__ == "__main__":
    queue = multiprocessing.Queue()

    listen = multiprocessing.Process(target=warp_main, args=(queue,))
    listen.start()
    RunDemo(queue)