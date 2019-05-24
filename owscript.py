from Lexer import Lexer
from Parser import Parser
from Transpiler import Transpiler

file = 'Tests/test0.ows'
with open(file) as f:
    text = f.read()

lexer = Lexer(text)
tokens = lexer.lex()
parser = Parser(tokens)
# print(tokens)
tree = parser.parse()
transpiler = Transpiler(tree)
code = transpiler.run()