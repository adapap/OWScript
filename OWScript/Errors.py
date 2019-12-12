import sys
TEXT = None

class ExitCode:
    CompileError = 1
    InputNotFound = 2
    OutputNotFound = 3

class Logger:
    INFO = 1
    WARN = 2
    DEBUG = 3
    def __init__(self, log_level=WARN):
        self.log_level = log_level

    def info(self, *msg):
        if self.log_level >= Logger.INFO:
            sys.stderr.write('[INFO] {}\n'.format(' '.join(map(str, msg))))

    def warn(self, *msg):
        if self.log_level >= Logger.WARN:
            sys.stderr.write('[WARNING] {}\n'.format(' '.join(map(str, msg))))

    def debug(self, *msg):
        if self.log_level >= Logger.DEBUG:
            sys.stderr.write('[DEBUG] {}\n'.format(' '.join(map(str, msg))))

class OWSError(Exception):
    def __init__(self, msg, pos=None):
        global TEXT
        if pos:
            line, col = pos
            text = '\n' + TEXT.split('\n')[line - 1].replace('\t', ' ' * 4)
            char = '\n' + ' ' * (col - 1) + '^\n'
            msg = 'Line {}'.format(line) + text + char + msg
        super().__init__(msg)

class LexError(OWSError):
    pass

class ParseError(OWSError):
    pass

class ImportError(OWSError):
    pass

class SyntaxError(OWSError):
    pass

class InvalidParameter(SyntaxError):
    pass

class StringError(SyntaxError):
    pass

class NameError(SyntaxError):
    pass

class AttributeError(SyntaxError):
    pass

class FileNotFoundError(OWSError):
    pass

class NotImplementedError(OWSError):
    pass

class ReturnError(Exception):
    def __init__(self, value):
        self.value = value