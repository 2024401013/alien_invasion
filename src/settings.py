class Settings:
    def __init__(self):
        self.game_name = "Alien Invasion"

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.background_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 10
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        # 外星人设置
        self.alien_speed = 2.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1 # 1:right -1:left

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        
        # 按钮设置
        self.button_width = 200
        self.button_height = 50
        self.button_color = (0, 135, 0)
        self.text_color = (255, 255, 255)
        self.font_size = 48

        # 外星人子弹
        self.alien_bullet_speed = 1.5
        self.alien_bullets_allowed = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50

        self.alien_bullet_speed = 1.5

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)

        self.alien_bullet_speed *= self.speedup_scale
    
