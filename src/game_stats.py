import pygame
import json 
import os

class GameStats:
    """
    跟踪游戏统计信息的类，如得分、剩余飞船数量等。
    """
    def __init__(self, aigame):
        """
        初始化统计信息。
        :param aigame: 游戏实例，通过它访问游戏设置。
        """
        self.settings = aigame.settings
        # 重置统计数据，但不包括最高分
        self.reset_stats()
        # 初始最高分为0
        self.high_score = 0
        # 定义存储最高分的文件名
        self.high_score_file = "high_score.json"
        # 加载已存在的最高分
        self.load_high_score()

    def reset_stats(self):
        """
        初始化在游戏运行期间可能变化的统计信息。
        """
        # 剩余飞船数量等于设置中指定的数量
        self.ship_left = self.settings.ship_limit
        # 初始得分为0
        self.score = 0
        # 初始关卡为1
        self.level = 1

    def load_high_score(self):
        """
        尝试从文件加载最高分，如果文件不存在或读取失败，则将最高分设为0。
        """
        try:
            # 检查文件是否存在
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, 'r') as f:
                    # 从文件加载最高分
                    self.high_score = json.load(f)
            else:
                self.high_score = 0
        except(FileNotFoundError, json.JSONDecodeError):
            # 文件未找到或JSON解码错误时，将最高分初始化为0
            self.high_score = 0

    def save_high_score(self):
        """
        将当前的最高分保存到文件中。
        """
        try:
            # 将最高分写入文件
            with open(self.high_score_file, 'w') as f:
                json.dump(self.high_score, f)
        except Exception as e:
            # 输出任何可能发生的异常信息
            print(f"保存最高分时出错:{e}")
