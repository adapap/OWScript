import argparse
import os
import re
import sys
from antlr4 import *
from src.OWScriptLexer import OWScriptLexer
from src.OWScriptParser import OWScriptParser
from src.ASTBuilder import ASTBuilder
from src.Transpiler import Transpiler

class UppercaseStream(FileStream):
    def _loadString(self):
        self._index = 0
        self.data = [ord(c.upper()) for c in self.strdata]
        self._size = len(self.data)
 
def process(code, minify=False, save=None):
    input_stream = UppercaseStream(code, 'utf-8')
    lexer = OWScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = OWScriptParser(stream)
    ast = ASTBuilder().run(parser.script())
    # print(ast)
    output = Transpiler().run(ast)
    if minify:
        output = re.sub(r'[\s\n]*', '', output)
    if not save:
        sys.stdout.write(output)
    else:
        with open(save, 'w') as f:
            f.write(output)
 
if __name__ == '__main__':
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    parser = argparse.ArgumentParser(description='Generate Overwatch Workshop code from OWScript')
    parser.add_argument('input', nargs='*', type=str, help='Standard input to process')
    parser.add_argument('-m', '--min', action='store_true', help='Minifies the output by removing whitespace')
    parser.add_argument('-s', '--save', help='Save the output to a file instead of printing it')
    args = parser.parse_args()
    if not args.input:
        process(sys.stdin)
    for file in args.input:
        process(file, minify=args.min, save=args.save)