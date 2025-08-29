import time
import pyautogui as pg
from typing import Dict, Any
from strategy_manager import StrategyManager
from color_detector import ColorDetector
from position import PositionManager
from config import Config

class AutomationEngine:
    """Движок автоматизации торговли"""
    
    def __init__(self):
        self.strategy_manager = StrategyManager()
        self.color_detector = ColorDetector()
        self.position_manager = PositionManager()
        self.config = Config()
        
        self.is_running = False
        self.is_winning = False
        self.current_strategy = None
        self.current_colors = {}
    
    def initialize(self):
        """Инициализация движка"""
        print("Инициализация движка автоматизации...")
        self.current_strategy = self.strategy_manager.load_strategy()
        print("Стратегия загружена успешно!")
    
    def start(self):
        """Запуск автоматизации"""
        self.is_running = True
        print("Автоматизация запущена...")
        
        try:
            while self.is_running:
                self.check_win_conditions()
                self.execute_anti_bot()
                time.sleep(self.config.DELAY_BETWEEN_CHECKS)
        except KeyboardInterrupt:
            print("Автоматизация остановлена пользователем")
        except Exception as e:
            print(f"Ошибка в работе движка: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Остановка автоматизации"""
        self.is_running = False
        print("Автоматизация остановлена")
    
    def check_win_conditions(self):
        """Проверка условий для победы"""
        self._update_current_colors()
        
        win_detected = True
        match_count = 0
        
        for i, (bullid_idx, current_color) in enumerate(self.current_colors.items()):
            expected_colors = self.current_strategy['voting_strategy'][i]
            
            # Проверяем, совпадает ли текущий цвет с ожидаемым
            color_matched = any(
                current_color == expected_color 
                for expected_color in expected_colors
            )
            
            if not color_matched:
                win_detected = False
            else:
                match_count += 1
                print(f"Совпало: {bullid_idx + 1}")
        
        if win_detected or match_count == 6:
            print("Победа! " + "#" * 60)
            self.is_winning = True
            self.execute_win_actions()
            self.is_winning = False
    
    def _update_current_colors(self):
        """Обновление текущих цветов буллидов"""
        self.current_colors = {}
        for i, (x, y) in enumerate(self.current_strategy['bullid_coords']):
            self.current_colors[i] = self.color_detector.get_pixel_color(x, y)
        
        print(f"Текущие цвета: {self.current_colors}")
    
    def execute_win_actions(self):
        """Выполнение действий при победе"""
        if (self.current_strategy['bet_location'] and 
            self.current_strategy['outcome_location']):
            
            aim_x, aim_y = self.current_strategy['outcome_location']
            bet_x, bet_y = self.current_strategy['bet_location']
            
            self.position_manager.move_to(aim_x, aim_y, self.config.MOUSE_MOVE_DURATION)
            time.sleep(0.5)
            self.position_manager.move_to(bet_x, bet_y, self.config.MOUSE_MOVE_DURATION * 2)
    
    def execute_anti_bot(self):
        """Выполнение anti-bot действий"""
        if not self.is_winning:
            print("AntiBot: active")
            for x, y in self.current_strategy['bullid_coords']:
                self.position_manager.move_to(x, y, 0.1)
                self.position_manager.click(x, y)
        else:
            print("AntiBot: inactive")