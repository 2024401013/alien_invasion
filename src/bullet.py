import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """
    管理飞船发射子弹的类。
    """
    
    def __init__(self, aigame):
        """
        在飞船当前位置创建一个子弹对象。
        :param aigame: 主游戏实例，用于访问屏幕、设置和飞船信息。
        """
        super().__init__()
        self.screen = aigame.screen  # 获取游戏屏幕对象
        self.settings = aigame.settings  # 获取游戏设置
        self.color = self.settings.bullet_color  # 子弹颜色从游戏设置中获取
        
        # 在(0,0)处创建一个表示子弹的矩形，之后再设置正确的位置
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        # 将子弹的初始位置设为飞船顶部中央
        self.rect.midtop = aigame.ship.rect.midtop
        
        # 存储小数表示的子弹位置，便于更精确地控制子弹的速度
        self.y = float(self.rect.y)
    
    def update(self):
        """向上移动子弹"""
        # 更新表示子弹位置的小数值
        self.y -= self.settings.bullet_speed
        # 更新表示子弹位置的rect值
        self.rect.y = self.y
    
    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
