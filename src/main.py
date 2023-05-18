import pygame
from src.scene import Scene


max_comment = 1000
width = 800
height = 560



class Game:
    def __init__(self, width = width, height = height):
        self.w = width
        self.h = height
        self.screen = self.get_screen()
        self.font = pygame.font.Font("font/BOBOHEI-2.otf", 14)
        self.scene = Scene(self.screen)

    def get_screen(self, ):
        pygame.init()
        screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('game')
        return screen

    def run(self, queue):
        # backgroud
        background = pygame.image.load("pic/background.jpeg").convert()
        
        dijia = pygame.image.load("pic/dijia.png").convert_alpha()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    SystemExit()

            count = 0   
            self.screen.blit(background, (0, 0)) 
            while not queue.empty() and count < max_comment:
                chat = queue.get()
                count += 1
                if chat[1] == "加入" or "加入游戏":
                    self.scene.create_person(chat[0],dijia)
                if chat[1] in ['R', 'r', 'y', 'Y', 'b', 'B', 'g', 'G',"w","s","a","d"]:
                    self.scene.change_answer(chat[0], chat[1])
            
            # display
            pygame.display.update()


if __name__ == "__main__":
    game = Game(width, height)
    game.run()