import pygame
import numpy as np
import math

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self._create_synthetic_sounds()
    
    def _create_synthetic_sounds(self):
        """生成合成的音效"""
        # 射击音效 - 短促高音
        self.shoot_sound = self._generate_beep(800, 100, volume=0.3)
        
        # 爆炸音效 - 低沉爆破声
        self.explosion_sound = self._generate_explosion(volume=0.5)
        
        # 盾牌音效 - 科幻上升音
        self.shield_sound = self._generate_sweep(300, 600, 400, volume=0.4)
        
        # 游戏结束音效 - 下降音
        self.game_over_sound = self._generate_sweep(400, 200, 800, volume=0.6)
        
        # 获得道具音效 - 欢快音
        self.power_up_sound = self._generate_power_up(volume=0.5)

    def _generate_beep(self, frequency, duration, volume=0.5):
        """生成简单的哔声音效"""
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))

        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            envelope = np.exp(-t * 5)  
            sample = volume * envelope * math.sin(2 * math.pi * frequency * t)
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    def _generate_explosion(self, volume=0.5):
        """生成爆炸音效"""
        sample_rate = 44100
        duration = 500 
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            freq = 100 + 50 * math.exp(-t * 10)  
            envelope = np.exp(-t * 8) 
            sample = volume * envelope * (0.7 * math.sin(2 * math.pi * freq * t) + 
                                        0.3 * np.random.uniform(-1, 1))
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    def _generate_sweep(self, start_freq, end_freq, duration, volume=0.5):
        """生成扫频音效"""
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            freq = start_freq + (end_freq - start_freq) * (i / n_samples)
            envelope = 1.0  
            sample = volume * envelope * math.sin(2 * math.pi * freq * t)
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    def _generate_power_up(self, volume=0.5):
        """生成获得道具音效"""
        sample_rate = 44100
        duration = 600  
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            freq1 = 400 + 200 * (i / n_samples)
            freq2 = 600 + 300 * (i / n_samples)
            envelope = 1.0 if i < n_samples * 0.8 else np.exp(-(i - n_samples * 0.8) / (n_samples * 0.2))
            
            sample = volume * envelope * (0.6 * math.sin(2 * math.pi * freq1 * t) + 
                                        0.4 * math.sin(2 * math.pi * freq2 * t))
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)


    def play_shoot(self):
        """播放射击音效"""
        self.shoot_sound.play()

    def play_explosion(self):
        """播放爆炸音效"""
        self.explosion_sound.play()

    def play_shield(self):
        """播放盾牌音效"""
        self.shield_sound.play()

    def play_game_over(self):
        """播放游戏结束音效"""
        self.game_over_sound.play()

    def play_power_up(self):
        """播放获得道具音效"""
        self.power_up_sound.play()