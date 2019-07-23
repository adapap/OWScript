from . import Errors
from .Lexer import Lexer
from .Parser import Parser

def import_file(path):
    error_text = Errors.TEXT
    with open(path) as f:
        text = f.read()
    try:
        Errors.TEXT = text
        lexer = Lexer(text=text)
        tokens = lexer.lex()
        parser = Parser(tokens=tokens)
        tree = parser.script()
        Errors.TEXT = error_text
        return tree
    except Exception as ex:
        Errors.TEXT = error_text
        raise ex