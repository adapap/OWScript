class OWSError(Exception):
    pass

class LexError(OWSError):
    pass

class ParseError(OWSError):
    pass

class SyntaxError(OWSError):
    pass

class NotImplementedError(OWSError):
    pass