import time
import logging
import os
os.system("")  # enables ansi escape characters in windows terminals
import re



class ColorPrint:
    def print_red(message):
        return f'\x1b[1;31m{message}\x1b[0m'

    def print_green(message):
        return f'\x1b[1;32m{message}\x1b[0m'

    def print_yellow(message):
        return f'\x1b[1;33m{message}\x1b[0m'

    def print_blue(message):
        return f'\x1b[1;34m{message}\x1b[0m'

    def print_purple(message):
        return f'\x1b[1;35m{message}\x1b[0m'

    def print_cyan(message):
        return f'\x1b[1;36m{message}\x1b[0m'

    def print_bold(message):
        return f'\x1b[1;37m{message}\x1b[0m'



class TermEscapeCodeFormatter(logging.Formatter):
    """
    A class to strip the color escape codes when printing to non ANSI terminals, like a text file
    """
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True):
        super().__init__(fmt, datefmt, style, validate)

    def format(self, record):
        escape_re = re.compile(r'\x1b\[[0-9;]*m')
        record.msg = re.sub(escape_re, "", str(record.msg))
        return super().format(record)

class LogFormatHandler():
    """
    A class to act as an interface to the python logger and handle adding font colors depending on log level
    """
    def __init__(self, stream_level, file_level=logging.WARN, output_to_file=False):
        LOGS_FILE_PATH = f'logs_{time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(time.time()))}.txt'

        lger = logging.getLogger()
        lger.setLevel(logging.DEBUG) # do not change - logging level set individually below

        stdo = logging.StreamHandler()
        stdo.setLevel(stream_level)
        fmer = logging.Formatter('%(asctime)s %(message)s')
        stdo.setFormatter(fmer)
        lger.addHandler(stdo)

        if output_to_file:
            fhdr = logging.FileHandler(LOGS_FILE_PATH, "w")
            fhdr.setLevel(file_level)
            cfmer = TermEscapeCodeFormatter('%(asctime)s %(message)s')
            fhdr.setFormatter(cfmer)
            lger.addHandler(fhdr)

        self.logger = lger

    def debug(self, message):
        self.logger.debug(ColorPrint.print_purple(f'[DEBUG] {message}'))

    def info(self, message):
        self.logger.info(ColorPrint.print_blue(f'[INFO] {message}'))

    def success(self, message):
        self.logger.info(ColorPrint.print_green(f'[SUCCESS] {message}'))

    def warning(self, message):
        self.logger.warning(ColorPrint.print_yellow(f'[WARN] {message}'))

    def error(self, message):
        self.logger.error(ColorPrint.print_red(f'[ERROR] {message}'))

    def critical(self, message):
        self.logger.critical(ColorPrint.print_red(f'[CRITICAL] {message}'))

    def exception(self, message):
        self.logger.exception(ColorPrint.print_yellow(f'[EXCEPTION] {message}'))



script_info = ["===================================================================",
               "= Bulk Update Findings   Script                                   =",
               "=-----------------------------------------------------------------=",
               "=  The user can select a Client to update all findings across     =",
               "=  each report on the client.                                     =",
               "=                                                                 =",
               "==================================================================="
            ]

def print_script_info():
    for i in script_info:
        print(i)



console_log_level = logging.INFO
file_log_level = logging.WARN
log = LogFormatHandler(console_log_level, file_log_level, output_to_file=False) # change out_to_file to write console logs to file
