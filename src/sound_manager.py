import pygame
import numpy as np
import math

class SoundManager:
    """程序化生成游戏音效（无需外部音频文件）——自研核心扩展"""

    def __init__(self):
        """初始化混音器并预生成所有合成音效"""
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self._create_synthetic_sounds()
    
    def _create_synthetic_sounds(self):
        """使用数学函数动态合成五类游戏音效"""
        # 射击：短促高频蜂鸣（100ms）
        self.shoot_sound = self._generate_beep(800, 100, volume=0.3)
        
        # 爆炸：带噪声衰减的低频爆破声（500ms）
        self.explosion_sound = self._generate_explosion(volume=0.5)
        
        # 盾牌激活：频率上升的科幻扫频音（400ms）——呼应盾牌视觉效果
        self.shield_sound = self._generate_sweep(300, 600, 400, volume=0.4)
        
        # 游戏结束：频率下降的警示音（800ms）
        self.game_over_sound = self._generate_sweep(400, 200, 800, volume=0.6)
        
        # 道具拾取：双频叠加的欢快提示音（600ms）
        self.power_up_sound = self._generate_power_up(volume=0.5)

    def _generate_beep(self, frequency, duration, volume=0.5):
        """生成单频衰减正弦波（适用于射击等瞬时音效）"""
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))

        buf = np.zeros((n_samples, 2), dtype=np.int16)  # 双声道
        max_amplitude = np.power(2, 15) - 1  # 16位音频最大振幅
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            envelope = np.exp(-t * 5)  # 指数衰减包络，模拟真实发声
            sample = volume * envelope * math.sin(2 * math.pi * frequency * t)
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    def _generate_explosion(self, volume=0.5):
        """生成含随机噪声的爆炸音效（低频+衰减+扰动）"""
        sample_rate = 44100
        duration = 500 
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            freq = 100 + 50 * math.exp(-t * 10)   # 初始低频快速衰减
            envelope = np.exp(-t * 8)             # 快速衰减
            # 主波形 + 白噪声增强“爆破感”
            sample = volume * envelope * (0.7 * math.sin(2 * math.pi * freq * t) + 
                                        0.3 * np.random.uniform(-1, 1))
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    def _generate_sweep(self, start_freq, end_freq, duration, volume=0.5):
        """生成线性扫频音效（用于盾牌/游戏结束等状态提示）"""
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            # 频率从 start_freq 线性变化到 end_freq
            freq = start_freq + (end_freq - start_freq) * (i / n_samples)
            sample = volume * math.sin(2 * math.pi * freq * t)
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    def _generate_power_up(self, volume=0.5):
        """生成双频和声道具音效（营造“奖励感”）"""
        sample_rate = 44100
        duration = 600  
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = np.zeros((n_samples, 2), dtype=np.int16)
        max_amplitude = np.power(2, 15) - 1
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            # 两个频率同步上升，形成和谐和声
            freq1 = 400 + 200 * (i / n_samples)
            freq2 = 600 + 300 * (i / n_samples)
            # 前80%持续发声，后20%指数淡出
            envelope = 1.0 if i < n_samples * 0.8 else np.exp(-(i - n_samples * 0.8) / (n_samples * 0.2))
            
            sample = volume * envelope * (0.6 * math.sin(2 * math.pi * freq1 * t) + 
                                        0.4 * math.sin(2 * math.pi * freq2 * t))
            buf[i][0] = int(max_amplitude * sample)
            buf[i][1] = int(max_amplitude * sample)
        
        return pygame.sndarray.make_sound(buf)

    # === 公共播放接口 ===
    def play_shoot(self):
        self.shoot_sound.play()

    def play_explosion(self):
        self.explosion_sound.play()

    def play_shield(self):
        self.shield_sound.play()

    def play_game_over(self):
        self.game_over_sound.play()

    def play_power_up(self):
        self.power_up_sound.play()
