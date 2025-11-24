import pygame.font

class Button:
    """创建一个可点击的按钮，用于显示文本消息（如“Play”）"""

    def __init__(self, aigame, msg):
        """
        初始化按钮属性
        :param aigame: 主游戏实例，用于访问屏幕和设置
        :param msg: 按钮上显示的文本（如 "Play"）
        """
        self.screen = aigame.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = aigame.settings

        # 从设置中读取按钮尺寸与颜色
        self.width, self.height = self.settings.button_width, self.settings.button_height
        self.button_color = self.settings.button_color
        self.text_color = self.settings.text_color
        self.font = pygame.font.SysFont(None, self.settings.font_size)  # 使用默认字体

        # 创建按钮的 rect 对象并居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 将消息渲染为图像
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        将文本消息渲染为图像，并使其在按钮中居中
        """
        # 渲染文本：开启抗锯齿（True），指定文字颜色和背景色
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """在屏幕上绘制按钮（先填充背景，再绘制文本）"""
        self.screen.fill(self.button_color, self.rect)           # 绘制按钮底色
        self.screen.blit(self.msg_image, self.msg_image_rect)    # 绘制居中文本
