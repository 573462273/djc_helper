import datetime
import logging
import multiprocessing
import os
import pathlib
from sys import exit

import colorlog

###########################################################
#                         logging                         #
###########################################################
asciiReset = colorlog.escape_codes['reset']

fileFmtStr = "%(asctime)s %(filename)s:%(lineno)d %(funcName)s %(levelname)-5.5s: %(message)s [%(name)s] [%(processName)s(%(process)d)]"
consoleFmtStr = "{}%(asctime)s{} {}%(funcName)s:%(lineno)-3d{} {}%(levelname)-5.5s: %(message)s{}".format(
    "%(bold_purple)s", asciiReset,
    "%(purple)s", asciiReset,
    "%(log_color)s", asciiReset,
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.name = "djc_helper"

log_directory = "logs"
try:
    pathlib.Path(log_directory).mkdir(parents=True, exist_ok=True)
except PermissionError as err:
    print("创建日志目录logs失败，请确认是否限制了基础的运行权限")
    os.system("PAUSE")
    exit(-1)

process_name = multiprocessing.current_process().name
log_filename_file = ".log.filename"
if "MainProcess" in process_name:
    # 为了兼容多进程模式，仅主进程确定日志文件名并存盘，后续其他进程则读取该文件内容作为写日志的目标地址，比如出现很多日志文件
    time_str = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    log_filename = f"{log_directory}/{logger.name}_{process_name}_{time_str}.log"
    pathlib.Path(log_filename_file).write_text(log_filename, encoding='utf-8')

log_filename = pathlib.Path(log_filename_file).read_text(encoding='utf-8')


def new_file_handler():
    newFileHandler = logging.FileHandler(log_filename, encoding="utf-8", delay=True)
    fileLogFormatter = logging.Formatter(fileFmtStr)
    newFileHandler.setFormatter(fileLogFormatter)
    newFileHandler.setLevel(logging.DEBUG)

    return newFileHandler


fileHandler = new_file_handler()
logger.addHandler(fileHandler)

# hack: 将底层的color暴露出来
COLORS = [
    'black',
    'red',
    'green',
    'yellow',
    'blue',
    'purple',
    'cyan',
    'white'
]

PREFIXES = [
    # Foreground without prefix
    '', 'bold_', 'thin_',
    # Foreground with fg_ prefix
    'fg_', 'fg_bold_', 'fg_thin_',
    # Background with bg_ prefix - bold/light works differently
    'bg_', 'bg_bold_',
]

color_names = {}
for prefix_name in PREFIXES:
    for name in COLORS:
        color_name = prefix_name + name
        color_names[color_name] = color_name

consoleLogFormatter = colorlog.ColoredFormatter(
    consoleFmtStr,
    datefmt="%H:%M:%S",
    reset=True,
    log_colors={**color_names, **{
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'fg_bold_red',
        'CRITICAL': 'fg_bold_red',
    }},
    secondary_log_colors={},
    style='%'
)
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(consoleLogFormatter)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

try:
    from lanzou.api.utils import logger as lanzou_logger

    # 将lanzou的日志也显示
    lanzou_logger.setLevel(logging.INFO)
except Exception:
    pass


def color(color_name):
    return consoleLogFormatter.color(consoleLogFormatter.log_colors, color_name)


if __name__ == '__main__':
    consoleHandler.setLevel(logging.DEBUG)
    logger.debug("debug")
    logger.info("info")
    logger.warning("warn")
    logger.error("error")
    logger.critical("critical")
    logger.exception("exception", exc_info=Exception("测试Exception"))

    for name in color_names:
        print(color(name), name)
