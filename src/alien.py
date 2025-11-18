import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    def __init__(self, aigame):
        super().__init__()
        self.screen = aigame.screen
        self.settings = aigame.settings

        self.image = pygame.image.load('/home/zhang/python/alien_invasion/images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)
        
        self.ai_game = aigame  
        self.shoot_chance = 0.002
        self.last_shot_time = 0
        self.shot_cooldown = 3000 

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
        # === 新增：尝试射击 ===
        self._try_shoot()
    
    def _try_shoot(self):
        """尝试射击"""
        current_time = pygame.time.get_ticks()
        
        # 检查冷却时间且随机概率
        if (current_time - self.last_shot_time > self.shot_cooldown and 
            random.random() < self.shoot_chance and
            self.ai_game.game_active):  # 只在游戏活跃时射击
            
            self._shoot()
            self.last_shot_time = current_time
    
    def _shoot(self):
        """创建外星人子弹"""
        # 检查子弹数量限制
        if len(self.ai_game.alien_bullets) < self.settings.alien_bullets_allowed:
            from alien_bullet import AlienBullet  # 局部导入避免循环导入
            alien_bullet = AlienBullet(self.ai_game, self.rect.centerx, self.rect.bottom)
            self.ai_game.alien_bullets.add(alien_bullet)