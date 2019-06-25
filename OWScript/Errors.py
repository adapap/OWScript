TEXT = None
POS = None

class OWSError(Exception):
    def __init__(self, msg):
        global POS, TEXT
        if POS:
            line, col = POS
            POS = None
            text = '\n' + TEXT.split('\n')[line - 1]
            char = '\n' + ' ' * (col - 1) + '^\n'
            msg = 'Line {}'.format(line) + text + char + msg
        super().__init__(msg)

class LexError(OWSError):
    pass

class ParseError(OWSError):
    pass

class SyntaxError(OWSError):
    pass

class InvalidParameter(SyntaxError):
    pass

class StringError(SyntaxError):
    pass

class NotImplementedError(OWSError):
    pass