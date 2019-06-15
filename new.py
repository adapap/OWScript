import argparse
import sys
from OWScript.Lexer import Lexer
from OWScript.Parser import Parser
from OWScript.TranspilerNew import Transpiler

def transpile(text, minify=False, save=None):
    """Transpiles an OWScript code into Overwatch Workshop rules."""
    lexer = Lexer(text=text)
    tokens = lexer.lex()
    # lexer.print_tokens()
    parser = Parser(tokens=tokens)
    tree = parser.script()
    transpiler = Transpiler(tree=tree)
    code = transpiler.run()
    print(code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Overwatch Workshop code from OWScript')
    parser.add_argument('input', nargs='*', type=str, help='Standard input to process')
    parser.add_argument('-m', '--min', action='store_true', help='Minifies the output by removing whitespace')
    parser.add_argument('-s', '--save', help='Save the output to a file instead of printing it')
    args = parser.parse_args()
    file_input = args.input[0] if args.input else sys.stdin
    with open(file_input) as f:
        text = f.read()
    transpile(text, minify=args.min, save=args.save)