import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard:
    """显示得分、最高分、等级和剩余飞船的UI面板"""

    def __init__(self, aigame):
        """
        初始化计分板所需资源
        :param aigame: 主游戏实例，用于访问屏幕、设置和统计数据
        """
        self.aigame = aigame
        self.screen = aigame.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = aigame.settings
        self.stats = aigame.stats  # 包含 score, high_score, level, ship_left 等

        # 文字样式：深灰色文字 + 默认字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 预渲染所有UI元素
        self.prep_score()
        self.prep_high_score()  # 支持从文件加载的最高分（自研持久化功能）
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """将当前得分格式化为带千位分隔符的字符串，并渲染为图像"""
        round_score = round(self.stats.score, -1)      # 四舍五入到十位
        score_str = f"{round_score:,}"                 # 添加逗号分隔符（如 1,230）
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.background_color
        )

        # 定位：右上角，距右边框20像素
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """渲染历史最高分（支持跨会话持久化）"""
        high_score = round(self.stats.high_score, -1)
        score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(
            score_str, True, self.text_color, self.settings.background_color
        )

        # 定位：在当前得分下方10像素处，右对齐
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.right = self.score_rect.right
        self.high_score_rect.top = self.score_rect.bottom + 10

    def prep_level(self):
        """渲染当前关卡等级"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.background_color
        )

        # 定位：在最高分下方40像素处（总偏移50）
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top = self.score_rect.bottom + 50

    def prep_ships(self):
        """创建表示剩余飞船数量的小图标（左上角排列）"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.aigame)  # 复用飞船类，缩小版图标
            ship.rect.x = 10 + ship_number * ship.rect.width  # 水平间隔排列
            ship.rect.y = 10                                   # 距顶部10像素
            self.ships.add(ship)

    def show_score(self):
        """在屏幕上绘制所有计分元素"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)  # 利用精灵组自动绘制所有飞船图标

    def check_high_score(self):
        """检查是否刷新历史最高分，并更新显示（配合持久化保存）"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()  # 重新渲染新最高分
