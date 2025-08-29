import pyautogui as pg
import time
from typing import Tuple

class PositionManager:
    """Управление позицией курсора и получением координат"""
    
    def __init__(self):
        pg.FAILSAFE = False
    
    def get_current_position(self) -> Tuple[int, int]:
        """Получить текущую позицию курсора"""
        position = pg.position()
        return position.x, position.y
    
    def get_position_with_delay(self, delay_seconds: int = 5) -> Tuple[int, int]:
        """
        Получить позицию курсора с задержкой
        
        Args:
            delay_seconds: Задержка перед получением позиции
            
        Returns:
            Кортеж (x, y) координат
        """
        print(f"В течение {delay_seconds} секунд наведите курсор на нужное место...")
        time.sleep(delay_seconds)
        return self.get_current_position()
    
    def format_position(self, x: int, y: int) -> str:
        """Форматировать координаты в строку"""
        return f"|{x}||{y}|"
    
    def move_to(self, x: int, y: int, duration: float = 1.0):
        """Плавное перемещение курсора к указанным координатам"""
        pg.moveTo(x, y, duration=duration)
    
    def click(self, x: int, y: int):
        """Клик по указанным координатам"""
        pg.click(x, y)