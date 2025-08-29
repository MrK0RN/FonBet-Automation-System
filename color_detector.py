import pyautogui as pg
import time
from typing import List, Tuple
from position import PositionManager

class ColorDetector:
    """Детектор цветов пикселей на экране"""
    
    def __init__(self):
        self.position_manager = PositionManager()
    
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Получить цвет пикселя по координатам
        
        Args:
            x: Координата X
            y: Координата Y
            
        Returns:
            Кортеж (R, G, B) цвета
        """
        pixel_color = pg.pixel(x, y)
        return (int(pixel_color.red), int(pixel_color.green), int(pixel_color.blue))
    
    def get_color_at_current_position(self, delay: int = 1) -> Tuple[int, int, int]:
        """
        Получить цвет пикселя в текущей позиции курсора после задержки
        
        Args:
            delay: Задержка в секундах
            
        Returns:
            Кортеж (R, G, B) цвета
        """
        time.sleep(delay)
        x, y = self.position_manager.get_current_position()
        return self.get_pixel_color(x, y)
    
    def format_color_log(self, color: Tuple[int, int, int], key: str) -> str:
        """
        Форматировать информацию о цвете для логирования
        
        Args:
            color: Кортеж (R, G, B)
            key: Ключ для идентификации
            
        Returns:
            Строка с отформатированной информацией
        """
        return f"{key}|{color[0]}||{color[1]}||{color[2]}|"