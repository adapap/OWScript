import argparse
import re
import sys
from OWScript.Lexer import Lexer
from OWScript.Parser import Parser
from OWScript.Transpiler import Transpiler

class DEBUG:
    """Bit flags used for debug code."""
    TOKENS = 1
    TREE = 2

def transpile(text, minify=False, save=None, debug=0):
    """Transpiles an OWScript code into Overwatch Workshop rules."""
    lexer = Lexer(text=text)
    tokens = lexer.lex()
    if debug & DEBUG.TOKENS:
        if save:
            with open(save, 'w', errors='ignore') as f:
                f.write(lexer.print_tokens())
        else:
            lexer.print_tokens()
    parser = Parser(tokens=tokens)
    tree = parser.script()
    if debug & DEBUG.TREE:
        print(tree.string())
    transpiler = Transpiler(tree=tree)
    code = transpiler.run()
    if minify:
        code = re.sub(r'[\s\n]*', '', code)
    if not save:
        sys.stdout.write(code)
    else:
        with open(save, 'w') as f:
            f.write(code)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Overwatch Workshop code from OWScript')
    parser.add_argument('input', nargs='*', type=str, help='Standard input to process')
    parser.add_argument('-m', '--min', action='store_true', help='Minifies the output by removing whitespace')
    parser.add_argument('-s', '--save', help='Save the output to a file instead of printing it')
    parser.add_argument('-d', '--debug', type=int, help='Debugging tool used for development')
    args = parser.parse_args()
    file_input = args.input[0] if args.input else sys.stdin
    with open(file_input) as f:
        text = f.read()
    transpile(text, minify=args.min, save=args.save, debug=args.debug or 0)
    