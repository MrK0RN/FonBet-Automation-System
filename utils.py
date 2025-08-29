from typing import List, Any
import re

class Utils:
    """Вспомогательные утилиты"""
    
    @staticmethod
    def parse_record_body(record: str) -> List[str]:
        """Парсинг тела записи с разделителями |"""
        return [part for part in re.split(r'\|\|?', record) if part]
    
    @staticmethod
    def format_coordinates(x: int, y: int) -> str:
        """Форматирование координат в строку"""
        return f"|{x}||{y}|"
    
    @staticmethod
    def is_color_match(actual_color: List[int], expected_colors: List[List[int]]) -> bool:
        """Проверка совпадения цвета с ожидаемыми значениями"""
        return any(actual_color == expected for expected in expected_colors)