class Settings:
    """存储游戏《外星人入侵》的所有设置"""

    def __init__(self):
        # 游戏基本信息
        self.game_name = "Alien Invasion"

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)  # 浅灰色背景

        # 飞船设置
        self.ship_speed = 10      # 初始速度（会被 initialize_dynamic_settings 覆盖）
        self.ship_limit = 3       # 玩家初始拥有3条命

        # 玩家子弹设置
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5  # 限制同时存在的子弹数量，防止性能下降

        # 外星人基础行为
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1 表示向右，-1 表示向左

        # 难度递增参数
        self.speedup_scale = 1.1   # 每关速度提升 10%
        self.score_scale = 1.5     # 每关得分奖励提升 50%

        # 按钮UI设置
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 135, 0)    # 深绿色
        self.text_color = (255, 255, 255)  # 白色文字
        self.font_size = 48

        # === 自研扩展：外星人子弹系统 ===
        self.alien_bullet_speed = 1.5
        self.alien_bullets_allowed = 10  # 限制敌方子弹总数，平衡游戏难度

        # 初始化随游戏进程变化的动态设置
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """
        初始化在游戏开始或重置时需要恢复的动态参数。
        这些值会在每局开始时重置，并随关卡提升而增强。
        """
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50           # 击败一个外星人的基础得分
        self.alien_bullet_speed = 1.5    # 与上方一致，确保初始化完整

    def increase_speed(self):
        """
        提升游戏难度：加快移动速度，并提高得分倍率。
        在玩家进入新关卡时调用。
        """
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_bullet_speed *= self.speedup_scale  # 同步提升敌方子弹速度

        # 得分必须为整数，避免显示小数
        self.alien_points = int(self.alien_points * self.score_scale)
