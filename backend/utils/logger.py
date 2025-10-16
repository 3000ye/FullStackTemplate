import os
import attrs
import logging
import colorlog
from typing import Optional
from datetime import datetime
from attr.validators import instance_of, min_len, optional

from backend.core import base_config
from backend.utils.dingtalk import post_msg

error_webhook = base_config["dingtalk"]["ERROR"]

levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


@attrs.define(kw_only=True, eq=False)
class Logger:
    """
    一个自定义的日志类，提供带有彩色输出的日志功能

    Attributes:
        name:       日志器的名称
        level:      日志器的级别
        file:       保存日志的文件路径默认为 None
        _logger:    底层的日志器对象

    Methods:
        debug:      记录一个调试级别的消息
        info:       记录一个信息级别的消息
        warning:    记录一个警告级别的消息
        error:      记录一个错误级别的消息
        critical:   记录一个严重级别的消息
    """

    name: str = attrs.field(validator=[instance_of(str), min_len(1)])
    level: str = attrs.field(default="DEBUG")
    file: Optional[str] = attrs.field(validator=optional(instance_of(str)), default=None)
    file_formatter: Optional[str] = attrs.field(default=None)
    _logger = attrs.field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        self._logger = logging.getLogger(self.name)
        for handler in self._logger.handlers[:]:
            self._logger.removeHandler(handler)

        use_color = os.getenv('colorlog', 'true').lower() == 'true'

        if use_color:
            # 彩色控制台 formatter（colorlog）
            console_formatter = colorlog.ColoredFormatter(
            "%(cyan)s[%(asctime)s.%(msecs)03d]%(reset)s | "
                "%(blue)s%(name)s%(reset)s | "
                "%(log_color)s%(levelname)s%(reset)s | "
                "%(log_color)s%(filename)s:%(lineno)d%(reset)s | "
                "%(log_color)s%(message)s",
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    "DEBUG": "bold_cyan",
                    "INFO": "bold_green",
                    "WARNING": "bold_yellow",
                    "ERROR": "bold_red",
                    "CRITICAL": "bold_red,bg_white",
                }
            )
        else:
            console_formatter = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] | "
                "%(name)s | "
                "%(levelname)s | "
                "%(filename)s:%(lineno)d | "
                "%(message)s",
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        # 普通文件 formatter（无颜色）
        file_formatter = logging.Formatter(
            "[%(asctime)s.%(msecs)03d] | %(name)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        # 钉钉 handler
        dingtalk_handler = DingTalkHandler(self.name)
        dingtalk_handler.setFormatter(file_formatter)
        dingtalk_handler.setLevel(logging.ERROR)
        self._logger.addHandler(dingtalk_handler)

        # 控制台 handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(console_formatter)
        stream_handler.setLevel(level=levels[self.level])
        self._logger.addHandler(stream_handler)

        # 文件 handler（无颜色）
        if self.file:
            today = datetime.today().strftime("%Y%m%d")
            self.file = self.file if today in self.file else self.file.replace(".log", f"_{today}.log")
            os.makedirs(os.path.dirname(self.file), exist_ok=True)
            file_handler = logging.FileHandler(self.file, encoding="utf-8")
            file_handler.setFormatter(file_formatter)  # 使用非彩色 formatter
            self._logger.addHandler(file_handler)

        self._logger.setLevel(logging.DEBUG)

    def debug(self, msg: str) -> None:
        """
        记录一个调试级别的消息

        Args:
            msg (str): The message to be logged.
        """
        self._log_with_location(logging.DEBUG, msg)

    def info(self, msg: str) -> None:
        """
        记录一个信息级别的消息

        Args:
            msg (str): The message to be logged.
        """
        self._log_with_location(logging.INFO, msg)

    def warning(self, msg: str) -> None:
        """
        记录一个警告级别的消息

        Args:
            msg (str): The message to be logged.
        """
        self._log_with_location(logging.WARNING, msg)

    def error(self, msg: str) -> None:
        """
        记录一个错误级别的消息，并发送钉钉消息

        Args:
            msg (str): The message to be logged.
        """
        self._log_with_location(logging.ERROR, msg)
        # post_msg(error_webhook, title=f"{self.name} Error", msg=f"{msg}\n{self.file_formatter}", color="red")

    def critical(self, msg: str) -> None:
        """
        记录一个严重级别的消息

        Args:
            msg (str): The message to be logged.
        """
        self._log_with_location(logging.CRITICAL, msg)

    def _log_with_location(self, level: int, msg: str) -> None:
        """
        带文件位置信息的日志记录方法

        Args:
            level: 日志级别
            msg: 日志消息
        """
        # Python 3.8+ 支持stacklevel参数
        self._logger.log(level, msg, stacklevel=3)


class DingTalkHandler(logging.StreamHandler):
    def __init__(self, name):
        super().__init__()
        # self.setLevel(logging.ERROR)
        self.name = name

    def emit(self, record):
        try:
            log_str = self.format(record)
            post_msg(error_webhook, title=f"{self.name} Error", msg=log_str, color="red")
        except Exception:
            self.handleError(record)