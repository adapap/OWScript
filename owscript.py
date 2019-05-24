from Lexer import Lexer
from Parser import Parser
from Transpiler import Transpiler

file = 'Tests/test0'
with open(file + '.ows') as f:
    text = f.read()

lexer = Lexer(text)
tokens = lexer.lex()
parser = Parser(tokens)
#print(tokens)
tree = parser.parse()
#print(tree.rules[0].conditions.block.statements[0].params[2].params)

#group = tree.rules[0].conditions.block.statements[0].params[1]
#print(group.statements[1].params)
# transpiler = Transpiler(tree)
# code = transpiler.run()
# with open(file + '.txt', 'w') as f:
#    f.write(code)