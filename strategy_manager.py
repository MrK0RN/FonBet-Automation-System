from typing import List, Tuple, Dict, Any
from position import PositionManager
from color_detector import ColorDetector
from config import Config
from file_manager import FileManager
import re

class StrategyManager:
    """Управление стратегией торговли"""
    
    def __init__(self):
        self.position_manager = PositionManager()
        self.color_detector = ColorDetector()
        self.file_manager = FileManager()
        self.config = Config()
    
    def create_strategy(self):
        """Создание новой стратегии"""
        print("Создание новой стратегии...")
        
        with self.file_manager.open_file(self.config.STRATEGY_FILE, 'a') as f:
            self._record_bullids(f)
            self._record_voting_strategy(f)
            self._record_bet_location(f)
            self._record_outcome_location(f)
        
        print("Стратегия успешно создана!")
    
    def _record_bullids(self, file_handle):
        """Запись координат буллидов"""
        print("Определение буллидов по порядку на одной стороне, потом на другой...")
        
        for side in range(2):
            for bullid_num in range(self.config.BULLID_COUNT // 2):
                input("Готовы? Нажмите Enter")
                x, y = self.position_manager.get_position_with_delay(5)
                position_str = self.position_manager.format_position(x, y)
                record = f"|1||{side}||{bullid_num}|{position_str}$"
                file_handle.write(record)
    
    def _record_voting_strategy(self, file_handle):
        """Запись стратегии голосования"""
        print("""
        Зададим Стратегию при которой голосуем
        Например: |WLW||LLI| означает:
        Счет 1: Попал-Не попал-Попал
        Счет 2: Не попал-Не попал-Еще не ударил
        
        W - Попал
        L - Не попал
        I - Еще не ударил
        """)
        
        strategy = input("Введите стратегию: ")
        file_handle.write(f"|2|{strategy}$")
    
    def _record_bet_location(self, file_handle):
        """Запись местоположения ставки"""
        print("Определим место, где находится ставка, которую вы хотите ставить")
        input("Готовы? Нажмите Enter")
        x, y = self.position_manager.get_position_with_delay(5)
        position_str = self.position_manager.format_position(x, y)
        file_handle.write(f"|3|{position_str}$")
    
    def _record_outcome_location(self, file_handle):
        """Запись местоположения исхода"""
        print("Определим место, где находится исход, который вы планируете")
        input("Готовы? Нажмите Enter")
        x, y = self.position_manager.get_position_with_delay(5)
        position_str = self.position_manager.format_position(x, y)
        file_handle.write(f"|4|{position_str}")
    
    def load_strategy(self) -> Dict[str, Any]:
        """Загрузка и парсинг стратегии из файла"""
        content = self.file_manager.read_file(self.config.STRATEGY_FILE)
        if not content:
            raise ValueError("Файл стратегии пуст или не существует")
        
        records = content.split("$")
        strategy_data = {
            'bullid_coords': [],
            'voting_strategy': [],
            'bet_location': None,
            'outcome_location': None
        }
        
        for record in records:
            if not record:
                continue
            
            record_type = record[1] if len(record) > 1 else None
            
            if record_type == '1':  # Bullid coordinates
                self._parse_bullid_record(record, strategy_data)
            elif record_type == '2':  # Voting strategy
                self._parse_strategy_record(record, strategy_data)
            elif record_type == '3':  # Bet location
                strategy_data['bet_location'] = self._parse_coordinate_record(record)
            elif record_type == '4':  # Outcome location
                strategy_data['outcome_location'] = self._parse_coordinate_record(record)
        
        return strategy_data
    
    def _parse_bullid_record(self, record: str, strategy_data: Dict[str, Any]):
        """Парсинг записи буллида"""
        parts = self._parse_record_body(record)
        if len(parts) >= 5:
            x, y = int(float(parts[3])), int(float(parts[4]))
            strategy_data['bullid_coords'].append([x, y])
    
    def _parse_strategy_record(self, record: str, strategy_data: Dict[str, Any]):
        """Парсинг записи стратегии"""
        parts = self._parse_record_body(record)
        if len(parts) > 1:
            strategy_str = ''.join(parts[1:])
            strategy_data['voting_strategy'] = self._convert_strategy_to_colors(strategy_str)
    
    def _parse_coordinate_record(self, record: str) -> Tuple[int, int]:
        """Парсинг координатной записи"""
        parts = self._parse_record_body(record)
        if len(parts) >= 3:
            return int(float(parts[1])), int(float(parts[2]))
        return None
    
    def _parse_record_body(self, record: str) -> List[str]:
        """Парсинг тела записи"""
        return [part for part in re.split(r'\|\|?', record) if part]
    
    def _convert_strategy_to_colors(self, strategy_str: str) -> List[List[int]]:
        """Конвертация строковой стратегии в цвета"""
        color_map = {
            'W': self.config.WIN,
            'L': self.config.MISS,
            'I': self.config.INACTIVE
        }
        
        strategy_colors = []
        for char in strategy_str:
            if char in color_map:
                strategy_colors.append(color_map[char])
            else:
                raise ValueError(f"Неизвестный символ стратегии: {char}")
        
        return strategy_colors