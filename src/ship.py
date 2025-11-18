import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self, aigame):
        super().__init__()
        self.screen = aigame.screen
        self.screen_rect = aigame.screen.get_rect()
        self.image = self.load_image()
        self.settings = aigame.settings

        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False

        self.x = float(self.rect.x)

        # === 盾牌系统 ===
        self.has_shield = False
        self.shield_start_time = 0
        self.shield_duration = 5000
        
        self.shield_image = None
        self.shield_rect = None
        
        # 盾牌时间显示
        self.font = pygame.font.SysFont(None, 24)

    def load_image(self):
        image = pygame.image.load('/home/zhang/python/alien_invasion/images/ship.bmp')
        size = image.get_size()
        want_height = 60
        scale = want_height / size[1]
        new_size = (int(size[0] * scale), want_height)
        return pygame.transform.smoothscale(image, new_size)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        if self.has_shield and self.shield_image:
            self.shield_rect.center = self.rect.center
            self.screen.blit(self.shield_image, self.shield_rect)
            
            # 显示盾牌剩余时间
            remaining_time = max(0, self.shield_duration - (pygame.time.get_ticks() - self.shield_start_time))
            seconds = remaining_time // 1000 + 1
            time_text = self.font.render(f"盾牌: {seconds}s", True, (255, 255, 255))
            time_rect = time_text.get_rect()
            time_rect.centerx = self.rect.centerx
            time_rect.bottom = self.rect.top - 10
            self.screen.blit(time_text, time_rect)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

        self._update_shield()

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def _update_shield(self):
        """更新盾牌状态"""
        if self.has_shield:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_start_time > self.shield_duration:
                self.has_shield = False
                self.shield_image = None 
                self.shield_rect = None
                print("盾牌能量耗尽！")

    def activate_shield(self):
        """激活盾牌"""
        self.has_shield = True
        self.shield_start_time = pygame.time.get_ticks()
        
        self.shield_image = pygame.Surface((self.rect.width + 40, self.rect.height + 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.shield_image, (0, 100, 255, 128), self.shield_image.get_rect())
        self.shield_rect = self.shield_image.get_rect()
        
        self.ai_game.sound_manager.play_shield()
        print("盾牌激活！持续5秒")