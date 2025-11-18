import pygame
import json 
import os

class GameStats:
    def __init__(self, aigame):
        self.settings = aigame.settings
        self.reset_stats()
        self.high_score = 0
        self.high_score_file = "high_score.json"
        self.load_high_score()

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        try:
            if os.path.exists(self.high_score_file):
                with open(self.high_score_file, 'r') as f:
                    self.high_score = json.load(f)
            else:
                self.high_score = 0
        except(FileNotFoundError, json.JSONDecodeError):
            self.high_score = 0

    def save_high_score(self):
        try:
            with open(self.high_score_file, 'w') as f:
                json.dump(self.high_score, f)
        except Exception as e:
            print(f"保存最高分时出错:{e}")