
import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    def __init__(self, ai_game, x, y):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 50, 50)  
        
        # 创建子弹矩形
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = x
        self.rect.top = y
        
        self.y = float(self.rect.y)
    
    def update(self):
        """向下移动子弹"""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y
        
        if self.rect.top > self.screen.get_rect().bottom:
            self.kill()
    
    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)