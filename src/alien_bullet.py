import pygame
from pygame.sprite import Sprite

class AlienBullet(Sprite):
    """表示外星人发射的子弹的类（自研扩展功能）"""
    
    def __init__(self, ai_game, x, y):
        """
        在指定位置 (x, y) 创建一个外星人子弹对象
        :param ai_game: 主游戏实例，用于访问屏幕和设置
        :param x: 子弹水平起始位置（通常为外星人中心）
        :param y: 子弹垂直起始位置（通常为外星人底部）
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = (255, 50, 50)  # 鲜红色，区别于玩家子弹
        
        # 创建细长矩形作为子弹（宽3像素，高15像素）
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.centerx = x      # 水平居中对齐发射源
        self.rect.top = y          # 从外星人底部开始
        
        # 存储子弹的精确垂直位置，支持浮点速度
        self.y = float(self.rect.y)
    
    def update(self):
        """每帧向下移动子弹，并在移出屏幕后自动销毁"""
        self.y += self.settings.alien_bullet_speed
        self.rect.y = self.y
        
        # 若子弹完全离开屏幕底部，从精灵组中移除以节省内存
        if self.rect.top > self.screen.get_rect().bottom:
            self.kill()
    
    def draw_bullet(self):
        """在屏幕上绘制子弹（由主循环调用）"""
        pygame.draw.rect(self.screen, self.color, self.rect)
