# utils/loggers.py
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(nombre="logistica_pro", nivel=logging.INFO):
    """Configura un logger con formato estándar."""
    
    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Nombre del archivo de log con fecha
    fecha = datetime.now().strftime("%Y-%m-%d")
    log_file = log_dir / f"{nombre}_{fecha}.log"
    
    # Configurar logger
    logger = logging.getLogger(nombre)
    logger.setLevel(nivel)
    
    # Evitar duplicados si ya tiene handlers
    if not logger.handlers:
        # Handler para archivo
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(nivel)
        
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(nivel)
        
        # Formato
        formato = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formato)
        console_handler.setFormatter(formato)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger()