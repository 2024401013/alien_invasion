import pygame
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    def __init__(self, aigame):
        """
        初始化外星人并设置其起始位置
        :param aigame: 主游戏类实例，用于访问游戏设置和其他资源
        """
        super().__init__()
        self.screen = aigame.screen  # 获取屏幕信息
        self.settings = aigage.settings  # 获取游戏设置

        # 加载外星人图像，并获取其矩形
        self.image = pygame.image.load('/home/zhang/python/alien_invasion/images/alien.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人的初始位置设置在其宽度和高度处，以保证它们之间有间隔
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)
        
        self.ai_game = aigame  # 引用主游戏实例，用于调用游戏中的其他方法或属性
        
        # === 新增：射击相关的参数 ===
        self.shoot_chance = 0.002  # 外星人射击的概率
        self.last_shot_time = 0  # 上一次射击的时间戳
        self.shot_cooldown = 3000  # 射击冷却时间（毫秒）

    def check_edges(self):
        """检查是否有外星人位于屏幕边缘"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """
        向右或向左移动外星人，并尝试射击
        """
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        
        # === 新增：尝试射击 ===
        self._try_shoot()
    
    def _try_shoot(self):
        """
        根据一定概率和冷却时间判断是否射击
        """
        current_time = pygame.time.get_ticks()  # 当前时间（毫秒）
        
        # 检查冷却时间和随机概率，且仅在游戏激活时射击
        if (current_time - self.last_shot_time > self.shot_cooldown and 
            random.random() < self.shoot_chance and
            self.ai_game.game_active):  # 只在游戏活跃时射击
            
            self._shoot()
            self.last_shot_time = current_time  # 更新上一次射击时间
    
    def _shoot(self):
        """
        创建一个外星人子弹并添加到游戏中
        """
        # 确保当前外星人子弹数量不超过允许的最大值
        if len(self.ai_game.alien_bullets) < self.settings.alien_bullets_allowed:
            from alien_bullet import AlienBullet  # 局部导入避免循环依赖问题
            # 创建新的外星人子弹，并将其加入子弹组中
            alien_bullet = AlienBullet(self.ai_game, self.rect.centerx, self.rect.bottom)
            self.ai_game.alien_bullets.add(alien_bullet)
