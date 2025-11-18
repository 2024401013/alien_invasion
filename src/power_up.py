import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # 创建能量道具图像（盾牌图标）
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # 绘制盾牌形状的图标
        pygame.draw.ellipse(self.image, (0, 100, 255, 200), (5, 8, 20, 14))
        pygame.draw.ellipse(self.image, (200, 200, 255, 255), (5, 8, 20, 14), 2)
        pygame.draw.ellipse(self.image, (200, 200, 255, 255), (8, 3, 14, 24), 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, self.settings.screen_width - 80)
        self.rect.y = -self.rect.height
        
        self.speed = 2
        self.y = float(self.rect.y)

    def update(self):
        """向下移动能量道具"""
        self.y += self.speed
        self.rect.y = self.y
        
        if self.rect.top > self.settings.screen_height:
            self.kill()

    def collect(self):
        """收集道具"""
        self.kill()
        return "shield"