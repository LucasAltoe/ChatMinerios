import logging
import os

def setup_logging():
    """Configuração de logging robusta."""
    
    # Criação do diretório de logs, caso não exista
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Criação do arquivo de log
    log_file = os.path.join(log_dir, "app.log")
    
    # Configuração básica do logging
    logging.basicConfig(
        level=logging.DEBUG,  # Nível de log global
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),  # Gravar logs no arquivo
            logging.StreamHandler()         # Exibir logs no console
        ]
    )
    
    logger = logging.getLogger("minerio_bot")
    return logger

# Configuração do logger
logger = setup_logging()
