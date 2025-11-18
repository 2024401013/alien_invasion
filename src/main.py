import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from power_up import PowerUp  
from alien_bullet import AlienBullet  
from sound_manager import SoundManager
import random

class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption(self.settings.game_name)

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.alien_bullets = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        self.sound_manager = SoundManager()

        self._create_fleet()

        self.game_active = False

        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_event()
            if self.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
                self._update_alien_bullets()
                self._update_power_ups()
                
            self._update_screen()
            self.clock.tick(60)    

    def _check_event(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stats.save_high_score()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()

            pygame.mouse.set_visible(False)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_s:
            if self.stats.score >= 1000:
                self.stats.score -= 1000
                self.sb.prep_score()
                self.ship.activate_shield()
                print("消耗1000分获得盾牌！")
                


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)     
            self.sound_manager.play_shoot()

    def _update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        """更新外星人子弹位置"""
        self.alien_bullets.update()
        
        # 删除飞出屏幕的子弹
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        self._check_alien_bullet_collisions()
    
    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sound_manager.play_explosion()
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            self.stats.level += 1
            self.sb.prep_level()
    
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_power_ups(self):
        """更新能量道具"""
        self.power_ups.update()
        self._create_power_ups()

        self._check_power_up_collisions()

    def _create_power_ups(self):
        """随机创建能量道具"""
        if (random.random() < 0.001 and 
            len(self.power_ups) < 2 and 
            self.game_active):
            power_up = PowerUp(self)
            self.power_ups.add(power_up)
        

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 5 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ships()
        
            self.bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()
            self.power_ups.empty() 

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.sound_manager.play_game_over()
            self.game_active = False
            self.stats.save_high_score()
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_power_up_collisions(self):
        """检查能量道具与飞船的碰撞"""
        collisions = pygame.sprite.spritecollide(self.ship, self.power_ups, True)
        for power_up in collisions:
            power_type = power_up.collect()
            if power_type == "shield":
                self.ship.activate_shield()  
                self.sound_manager.play_power_up()

    def _check_alien_bullet_collisions(self):
        """检查外星人子弹与飞船的碰撞"""
        if self.ship.has_shield:
            # 有盾牌时，只检查从两侧射来的子弹
            for bullet in self.alien_bullets.sprites():
                if pygame.sprite.collide_rect(bullet, self.ship):
                    if (bullet.rect.left < self.ship.rect.left or 
                        bullet.rect.right > self.ship.rect.right):
                        bullet.kill()
                        self._ship_hit()
                        print("侧面攻击！盾牌无效")
                    else:

                        bullet.kill()
                        print("盾牌挡住了正面攻击！")
        else:
            # 无盾牌时，所有子弹都能伤害飞船
            collisions = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)
            if collisions:
                self._ship_hit()
                print("飞船被击中！")

    def _update_screen(self):
        self.screen.fill(self.settings.background_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        
        self.power_ups.draw(self.screen)

        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__=='__main__':
    ai = AlienInvasion()
    ai.run_game()