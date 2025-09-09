import logging
from pathlib import Path

LOG_FILE = Path("logs/app.log")

def setup_logger():
    """Configura el logger de la aplicación."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("main")

def get_logger():
    """Obtiene una instancia del logger."""
    return logging.getLogger("app")