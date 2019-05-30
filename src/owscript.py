import sys
from antlr4 import *
from OWScriptLexer import OWScriptLexer
from OWScriptParser import OWScriptParser
from ASTBuilder import ASTBuilder
from Transpiler import Transpiler
 
def main(argv):
    input_stream = FileStream(argv[1])
    lexer = OWScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = OWScriptParser(stream)
    ast = ASTBuilder().run(parser.script())
    # print(ast)
    output = Transpiler(ast).run()
    sys.stdout.write(output)
 
if __name__ == '__main__':
    main(sys.argv)