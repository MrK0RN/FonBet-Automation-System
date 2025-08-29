import os
from typing import Optional

class FileManager:
    """Управление файлами приложения"""
    
    def __init__(self, base_directory: str = "clicker"):
        self.base_directory = base_directory
        self._ensure_workspace()
    
    def _ensure_workspace(self):
        """Создание рабочего пространства если необходимо"""
        if not os.path.exists(self.base_directory):
            os.makedirs(self.base_directory)
        
        os.chdir(self.base_directory)
    
    def open_file(self, filename: str, mode: str = 'r'):
        """Открытие файла с автоматическим созданием директорий"""
        return open(filename, mode)
    
    def read_file(self, filename: str) -> Optional[str]:
        """Чтение содержимого файла"""
        try:
            with self.open_file(filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def file_exists(self, filename: str) -> bool:
        """Проверка существования файла"""
        return os.path.exists(filename) and os.path.getsize(filename) > 0
    
    def create_file_if_not_exists(self, filename: str):
        """Создание файла если он не существует"""
        if not self.file_exists(filename):
            with self.open_file(filename, 'w') as f:
                f.write("")