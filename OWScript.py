import argparse
import re
import sys
from OWScript import Errors
from OWScript.Lexer import Lexer
from OWScript.Parser import Parser
from OWScript.Transpiler import Transpiler

class DEBUG:
    """Bit flags used for debug code."""
    TOKENS = 1
    TREE = 2

def transpile(text, args):
    """Transpiles an OWScript code into Overwatch Workshop rules."""
    Errors.TEXT = text
    lexer = Lexer(text=text + '\n')
    tokens = lexer.lex()
    if args.debug & DEBUG.TOKENS:
        if args.save:
            with open(args.save, 'w', errors='ignore') as f:
                f.write(lexer.print_tokens())
        else:
            lexer.print_tokens()
    parser = Parser(tokens=tokens)
    tree = parser.script()
    if args.debug & DEBUG.TREE:
        print(tree.string())
    transpiler = Transpiler(tree=tree)
    code = transpiler.run()
    if args.min:
        code = re.sub(r'[\s\n]*', '', code)
    if not args.save:
        sys.stdout.write(code)
    else:
        with open(args.save, 'w') as f:
            f.write(code)
    if args.copy:
        import pyperclip
        pyperclip.copy(code)
        sys.stdout.write('Code copied to clipboard.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Overwatch Workshop code from OWScript')
    parser.add_argument('input', nargs='*', type=str, help='Standard input to process')
    parser.add_argument('-m', '--min', action='store_true', help='Minifies the output by removing whitespace')
    parser.add_argument('-s', '--save', help='Save the output to a file instead of printing it')
    parser.add_argument('-c', '--copy', action='store_true', help='Copies output to clipboard automatically')
    parser.add_argument('-d', '--debug', type=int, default=0, help='Debugging tool used for development')
    args = parser.parse_args()
    file_input = args.input[0] if args.input else sys.stdin
    with open(file_input) as f:
        text = f.read()
    try:
        transpile(text, args=args)
    except Errors.OWSError as ex:
        print('Error:', ex)