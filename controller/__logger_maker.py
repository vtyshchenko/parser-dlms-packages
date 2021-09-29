"""
logger module
"""

import logging

from datetime import date
from logging.handlers import RotatingFileHandler
from os import mkdir
from os.path import abspath, isdir, join


class Logger:
    """
    logger class
    """

    def __init__(self, ext='.log', log_dir='Logs', is_write=True,
                 fmt='%(asctime)s - [%(levelname)s] [%(module)s.%(funcName)s(%(lineno)d)] %(message)s',
                 datefmt='%d.%m.%Y %H:%M:%S', lvl=logging.DEBUG, size=10, back_cnt=2):

        # TODO settings from config.json
        path = abspath(".")
        self.log_path = join(path, log_dir)
        if not isdir(self.log_path):
            mkdir(self.log_path)
        today = date.today()
        self.log_file_name = join(self.log_path, 'log_' + str(today) + ext)
        self.write = logging.getLogger("main")
        self.write.setLevel(lvl)

        formatter = logging.Formatter(fmt)
        formatter.datefmt = datefmt
        handler = RotatingFileHandler(filename=self.log_file_name, maxBytes=size * 1024 * 1024, backupCount=back_cnt)
        handler.setLevel(lvl)
        handler.setFormatter(formatter)
        self.write.addHandler(handler)
        self.is_write = is_write

    def debug(self, msg, *args, **kwargs):
        if self.is_write:
            self.write.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        if self.is_write:
            self.write.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.is_write:
            self.write.warning(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.is_write:
            self.write.error(msg, *args, **kwargs)

    def exception(self, msg, *args, exc_info=True, **kwargs):
        if self.is_write:
            self.write.exception(msg, *args, exc_info, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.is_write:
            self.write.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        if self.is_write:
            self.write.log(level, msg, *args, **kwargs)


if __name__ == "__main__":
    lg = Logger()
    lg.info("info")
    lg.critical("critical")
    lg.error("error")
