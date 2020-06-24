import pygame.font

class Scoreboard():
    def __init__(self,screen,GS):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        self.bgcolour=GS.bgcolour

    def blitme(self,screen,score):
        score_str = "Score: "+str(score)
        score_image = self.font.render(score_str, True, self.text_color,self.bgcolour)
        score_rect = score_image.get_rect()
        self.screen.blit(score_image, score_rect)
