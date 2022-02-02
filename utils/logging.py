import logging
import sys
import os


class AppParamsFilter(logging.Filter):
    def __init__(self):
        self.app_version = os.environ.get('APP_VERSION')
        self.environment = os.environ.get('ENVIRONMENT')
        self.host_name = os.environ.get('HOST_NAME')

    def filter(self, record):
        record.app_version = self.app_version
        record.environment = self.environment
        record.host_name = self.host_name
        return True


def get_logger(name: str) -> logging.Logger:
    """
    Настраивает и возвращает экземпляр логгера
    """
    logger = logging.getLogger(name=name)

    if logger.hasHandlers() is False:
        formatter = logging.Formatter("[%(process)d/%(processName)s] %(message)s")

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        logger.addFilter(AppParamsFilter())

        logger.setLevel(logging.DEBUG)

    return logger
