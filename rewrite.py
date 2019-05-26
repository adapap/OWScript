from Lexer import Lexer
from Parser import Parser
from Transpiler import Transpiler

file = 'Tests/radial_menu_test'
with open(file + '.ows') as f:
    text = f.read()

# Lex / Parse / Transpile
Lexer.input(text)
# for token in Lexer:
#     print(token)
tree = Parser.parse(lexer=Lexer, debug=0)
print(tree)
transpiler = Transpiler(tree)
code = transpiler.run()
with open(file + '.txt', 'w') as f:
    f.write(code)