# import sys
# from antlr4 import *
# from OWScriptLexer import OWScriptLexer
# from OWScriptParser import OWScriptParser
# from ASTBuilder import ASTBuilder
# from Transpiler import Transpiler

# class UppercaseStream(FileStream):
#     def _loadString(self):
#         self._index = 0
#         self.data = [ord(c.upper()) for c in self.strdata]
#         self._size = len(self.data)
 
# def main(argv):
#     input_stream = UppercaseStream(argv[1], 'utf-8')
#     lexer = OWScriptLexer(input_stream)
#     stream = CommonTokenStream(lexer)
#     parser = OWScriptParser(stream)
#     ast = ASTBuilder().run(parser.script())
#     # print(ast)
#     output = Transpiler().run(ast)
#     sys.stdout.write(output)
 
# if __name__ == '__main__':
#     main(sys.argv)

from Lexer import Lexer
from Parser import Parser

def run(file):
    lexer = Lexer(text=file.read())
    print(lexer.tokens)

run(open('../Examples/basic.ows'))