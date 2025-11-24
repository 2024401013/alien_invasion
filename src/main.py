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
    """《外星人入侵》主游戏控制器，集成所有自研扩展系统"""

    def __init__(self):
        """初始化游戏核心组件"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption(self.settings.game_name)

        # 游戏状态与UI
        self.stats = GameStats(self)          # 包含最高分持久化
        self.sb = Scoreboard(self)            # 显示得分/飞船/等级

        # 玩家实体
        self.ship = Ship(self)                # 含盾牌系统

        # 精灵组管理
        self.bullets = pygame.sprite.Group()           # 玩家子弹
        self.aliens = pygame.sprite.Group()            # 外星人舰队
        self.alien_bullets = pygame.sprite.Group()     # 自研：敌方子弹
        self.power_ups = pygame.sprite.Group()         # 自研：随机道具

        # 音效系统（程序化合成，无外部文件）
        self.sound_manager = SoundManager()

        # 初始化游戏场景
        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play")

    def run_game(self):
        """主游戏循环"""
        while True:
            self._check_event()
            if self.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
                self._update_alien_bullets()   # 更新敌方子弹
                self._update_power_ups()       # 更新道具
                
            self._update_screen()
            self.clock.tick(60)  # 锁定60 FPS

    def _check_event(self):
        """响应用户输入与系统事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()  # 退出前保存最高分
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """点击“Play”按钮开始新游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # 清空旧精灵，重置场景
            self.bullets.empty()
            self.aliens.empty()
            self.alien_bullets.empty()
            self.power_ups.empty()

            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """处理按键按下事件"""
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
            # 自研：消耗1000分激活盾牌（与 Shield 系统联动）
            if self.stats.score >= 1000:
                self.stats.score -= 1000
                self.sb.prep_score()  # 实时更新显示
                self.ship.activate_shield()
                print("消耗1000分获得盾牌！")

    def _check_keyup_events(self, event):
        """处理按键释放事件"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """发射玩家子弹并播放音效"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.sound_manager.play_shoot()  # 触发音效系统

    def _update_bullet(self):
        """更新玩家子弹位置并检测碰撞"""
        self.bullets.update()
        # 移除飞出屏幕的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _update_alien_bullets(self):
        """更新外星人子弹（自研敌方攻击系统）"""
        self.alien_bullets.update()
        for bullet in self.alien_bullets.copy():
            if bullet.rect.top > self.settings.screen_height:
                self.alien_bullets.remove(bullet)

        self._check_alien_bullet_collisions()  # 与盾牌系统交互

    def _check_bullet_alien_collisions(self):
        """检测玩家子弹与外星人碰撞"""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sound_manager.play_explosion()  # 播放爆炸音效
            self.sb.prep_score()
            self.sb.check_high_score()

        # 全歼外星人后进入下一关
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()  # 提升难度
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """更新外星人舰队行为"""
        self._check_fleet_edges()
        self.aliens.update()

        # 检测飞船与外星人直接碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _update_power_ups(self):
        """管理能量道具（自研随机掉落系统）"""
        self.power_ups.update()
        self._create_power_ups()
        self._check_power_up_collisions()

    def _create_power_ups(self):
        """以低概率生成道具（限制同时存在数量）"""
        if (random.random() < 0.001 and 
            len(self.power_ups) < 2 and 
            self.game_active):
            power_up = PowerUp(self)
            self.power_ups.add(power_up)

    def _create_fleet(self):
        """创建多行外星人舰队"""
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
        """在指定位置创建单个外星人"""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """检测舰队是否触碰边界，触发转向"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """舰队整体下移并反向移动"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """处理飞船被击中逻辑"""
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # 清空当前所有动态对象
            self.bullets.empty()
            self.alien_bullets.empty()
            self.aliens.empty()
            self.power_ups.empty()

            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)  # 短暂暂停增强反馈
        else:
            self.sound_manager.play_game_over()  # 播放结束音效
            self.game_active = False
            self.stats.save_high_score()         # 保存最终高分
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检测外星人到达屏幕底部"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_power_up_collisions(self):
        """拾取道具：目前仅支持盾牌"""
        collisions = pygame.sprite.spritecollide(self.ship, self.power_ups, True)
        for power_up in collisions:
            power_type = power_up.collect()
            if power_type == "shield":
                self.ship.activate_shield()
                self.sound_manager.play_power_up()  # 播放拾取音效

    def _check_alien_bullet_collisions(self):
        """
        处理外星人子弹与飞船的碰撞逻辑（核心：盾牌方向判定）
        - 正面攻击：盾牌可抵挡
        - 侧面攻击：盾牌无效，视为直接命中
        """
        if self.ship.has_shield:
            for bullet in self.alien_bullets.sprites():
                if pygame.sprite.collide_rect(bullet, self.ship):
                    # 判定是否从飞船左右两侧射入（盾牌无法覆盖区域）
                    if (bullet.rect.left < self.ship.rect.left or 
                        bullet.rect.right > self.ship.rect.right):
                        bullet.kill()
                        self._ship_hit()
                        print("侧面攻击！盾牌无效")
                    else:
                        bullet.kill()
                        print("盾牌挡住了正面攻击！")
        else:
            # 无盾牌时，任何命中均造成伤害
            collisions = pygame.sprite.spritecollide(self.ship, self.alien_bullets, True)
            if collisions:
                self._ship_hit()
                print("飞船被击中！")

    def _update_screen(self):
        """绘制当前帧画面"""
        self.screen.fill(self.settings.background_color)
        
        # 绘制所有子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.alien_bullets.sprites():
            bullet.draw_bullet()
        
        # 绘制道具、飞船、外星人
        self.power_ups.draw(self.screen)
        self.ship.blitme()      # 自动绘制盾牌（如激活）
        self.aliens.draw(self.screen)

        # 绘制UI
        self.sb.show_score()

        # 非活动状态显示开始按钮
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
