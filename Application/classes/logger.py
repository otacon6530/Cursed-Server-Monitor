import logging
import os
import sys
from logging.handlers import RotatingFileHandler

class Logger:
    """
    A simple logger class that wraps Python's logging module.
    Logs to both console and a rotating file (logs/application.log) in the application root directory.
    """

    def __init__(self, name: str = "ServerMonitor", log_dir: str = "logs", level: int = logging.INFO,
                 max_bytes: int = 5 * 1024 * 1024, backup_count: int = 5):
        # Determine the application root directory
        if hasattr(sys, 'frozen'):
            # If bundled by PyInstaller, use the bundle dir
            app_root = os.path.dirname(sys.executable)
        else:
            app_root = os.path.dirname(os.path.abspath(__file__))
            # Go up to the Application root if inside classes/
            if os.path.basename(app_root) == "classes":
                app_root = os.path.dirname(app_root)

        log_path = os.path.join(app_root, log_dir)
        os.makedirs(log_path, exist_ok=True)
        log_file = os.path.join(log_path, "application.log")

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Rotating file handler
        file_handler = RotatingFileHandler(
            log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(level)

        # Avoid duplicate handlers if re-instantiated
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        self.logger.exception(message, *args, **kwargs)