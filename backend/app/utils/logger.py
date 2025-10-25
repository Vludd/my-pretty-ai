import logging
import colorlog

LOG_LEVEL_COLORS = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

formatter = colorlog.ColoredFormatter(
    fmt="%(log_color)s%(levelname)-9s%(reset)s (%(cyan)s%(name)s%(reset)s) %(message)s",
    log_colors=LOG_LEVEL_COLORS,
    reset=True,
    style="%",
)

class Logger:
    def __init__(
        self, 
        log_level="INFO",
        exclude_logs=[
            "sqlalchemy.engine.Engine",
            "watchfiles"
        ]
    ) -> None:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        logger = logging.getLogger()
        logger.setLevel(log_level)
        logger.addHandler(handler)
        logger.propagate = False
        
        for exclude in exclude_logs:
            logging.getLogger(exclude).setLevel(logging.WARNING)
        
        self._logger = logger
        

        logger.debug(f"Logger initialized. Level: {log_level}")
    
    def info(self, message="Test info log..."):
        self._logger.info(message)
    
    def debug(self, message="Test debug log..."):
        self._logger.debug(message)
    
    def warning(self, message="Test warning log..."):
        self._logger.warning(message)
    
    def error(self, message="Test error log..."):
        self._logger.error(message)
    
    def critical(self, message="Test critical log..."):
        self._logger.critical(message)
        
    def set_level(self, level="INFO"):
        self._logger.setLevel(level)
        
exclude_loggers = []
logger = Logger("DEBUG", exclude_logs=exclude_loggers)
        