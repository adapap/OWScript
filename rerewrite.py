import sys
from antlr4 import *
from OWScriptLexer import OWScriptLexer
from OWScriptParser import OWScriptParser
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = OWScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = OWScriptParser(stream)
    tree = parser.startRule()
    print(tree)
 
if __name__ == '__main__':
    main(sys.argv)