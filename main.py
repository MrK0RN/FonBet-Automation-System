from strategy_manager import StrategyManager
from automation_engine import AutomationEngine
from file_manager import FileManager
from config import Config

def main():
    """Главная функция приложения"""
    print("=" * 50)
    print("FonBet Automation System")
    print("=" * 50)
    
    # Инициализация менеджера файлов
    file_manager = FileManager()
    config = Config()
    
    # Проверка существования стратегии
    if not file_manager.file_exists(config.STRATEGY_FILE):
        print("Стратегия не найдена. Создание новой...")
        strategy_manager = StrategyManager()
        strategy_manager.create_strategy()
    else:
        print("Стратегия найдена. Загрузка...")
    
    # Запуск автоматизации
    try:
        engine = AutomationEngine()
        engine.initialize()
        engine.start()
    except Exception as e:
        print(f"Ошибка при запуске: {e}")
    finally:
        print("Работа приложения завершена")

if __name__ == "__main__":
    main()