import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    """
    程序化生成的护盾道具类（自研扩展功能）
    使用 pygame.draw.ellipse 动态绘制盾牌图标，无需外部图像文件。
    """

    def __init__(self, ai_game):
        """
        初始化护盾道具并设置其初始位置
        :param ai_game: 主游戏实例，用于访问屏幕尺寸和设置
        """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # 创建一个带透明通道的 30x30 表面用于绘制图标
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        
        # === 程序化绘制盾牌图标（三层椭圆构成）===
        # 主体：深蓝色半透明填充椭圆
        pygame.draw.ellipse(self.image, (0, 100, 255, 200), (5, 8, 20, 14))
        # 外轮廓：浅蓝色描边
        pygame.draw.ellipse(self.image, (200, 200, 255, 255), (5, 8, 20, 14), 2)
        # 内部装饰：垂直椭圆增强盾牌感
        pygame.draw.ellipse(self.image, (200, 200, 255, 255), (8, 3, 14, 24), 2)
        
        # 获取矩形区域并随机水平位置（避开边缘）
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, self.settings.screen_width - 80)
        self.rect.y = -self.rect.height  # 从屏幕上方外开始下落
        
        self.speed = 2                   # 下落速度（像素/帧）
        self.y = float(self.rect.y)      # 精确垂直位置（支持浮点）

    def update(self):
        """每帧向下移动道具，并在移出屏幕后自动销毁"""
        self.y += self.speed
        self.rect.y = self.y
        
        # 若完全离开屏幕底部，从精灵组中移除
        if self.rect.top > self.settings.screen_height:
            self.kill()

    def collect(self):
        """
        被飞船拾取时调用，销毁自身并返回道具类型
        返回值用于触发对应效果（如激活护盾）
        """
        self.kill()
        return "shield"  # 目前仅实现护盾，可扩展为多种道具
