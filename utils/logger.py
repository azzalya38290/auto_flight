import logging

def setup_logger(name, log_file, level=logging.INFO):
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
    handler = logging.FileHandler(log_file, encoding='utf-8')        
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger

# Utilisation:
# logger = setup_logger('elitebot', 'logs/elitebot.log')
# logger.info("Hello world")
