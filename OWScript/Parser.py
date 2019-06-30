import re
from collections import deque
from functools import partial

try:
    from . import Errors
    from .AST import *
    from .Tokens import ALIASES
    from .Workshop import *
except ImportError:
    import Errors
    from AST import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.call_stack = deque(maxlen=5)

    @property
    def curtoken(self):
        """Returns the token at the current index."""
        return self.tokens[self.pos]

    @property
    def curtype(self):
        """Returns the type of the current token."""
        return self.curtoken.type

    @property
    def curpos(self):
        """Returns the tuple (line, column) of the current token position."""
        return self.curtoken.line, self.curtoken.column
    

    @property
    def curvalue(self):
        """Returns the value of the current token."""
        return self.curtoken.value

    def peek(self, n=1):
        """Returns the nth upcoming token."""
        try:
            return self.tokens[self.pos + n]
        except IndexError:
            print('Cannot peek further than token length')
    
    def eat(self, *tokens):
        """Consumes a token and moves on to the next one."""
        if len(tokens) > 1:
            for token in tokens:
                self.eat(token)
            return
        # print(self.curtoken)
        token_type = tokens[0]
        pos = self.curpos
        if self.curtype == token_type:
            self.pos += 1
        else:
            raise Errors.ParseError('Expected token of type {}, but received {}'.format(token_type, self.curtype), pos=pos)

    def parse_string(self, string, formats):
        string = re.sub(r'["\'`]', '', string)
        null = Constant(name='Null')
        if string == '{}':
            node = String(value='{0}')
            node.children = [formats[0]] + [null] * 2
            return node
        elif string == ' ':
            node = String(value='')
            node.children = [null] * 3
            return node
        for pattern in StringConstant.sorted_values:
            patt = re.sub(r'([^a-zA-Z0-9_\s{}])', r'\\\1', pattern)
            patt = re.sub(r'{\d}', r'(.+)', patt)
            match = re.match(patt, string, re.I)
            if match and not match.group(0) == '' and match.end() == len(string):
                groups = match.groups()
                children = []
                try:
                    for group in groups:
                        if group == '{}':
                            child = formats[0]
                            formats = formats[1:]
                        else:
                            child = self.parse_string(group, formats)
                        children.append(child)
                except Errors.StringError:
                    continue
                node = String(value=pattern)
                node.children = children + [null] * (3 - len(children))
                return node
        else:
            raise Errors.StringError('Invalid string \'{}\''.format(string))

    def script(self):
        """script : (NEWLINE | stmt)* EOF"""
        node = Script()
        while self.curtype != 'EOF':
            if self.curtype == 'NEWLINE':
                self.eat('NEWLINE')
            else:
                node.children.append(self.stmt())
        return node

    def stmt(self):
        """stmt : (funcdef | ruledef | line)"""
        if self.curvalue == '%':
            return self.funcdef()
        elif self.curtype in ('DISABLED', 'RULE'):
            return self.ruledef()
        else:
            return self.line()

    def funcdef(self):
        """funcdef : % NAME params? funcbody"""
        self.eat('MOD')
        name = self.curvalue
        self.eat('NAME')
        params = []
        if self.curtype == 'LPAREN':
            params = self.params()
        body = self.funcbody()
        node = Function(name=name, params=params)
        node.children.extend(body)
        return node

    def params(self):
        """params : (expr ( , expr)*)"""
        self.eat('LPAREN')
        params = [self.expr()]
        while self.curtype == 'COMMA':
            self.eat('COMMA')
            params.append(self.expr())
        self.eat('RPAREN')
        return params

    def funcbody(self):
        """funcbody : NEWLINE INDENT (ruledef | ruleblock | block | primary)+ DEDENT"""
        self.eat('NEWLINE', 'INDENT')
        body = []
        while self.curtype != 'DEDENT':
            if self.curtype in ('DISABLED', 'RULE'):
                body.append(self.ruledef())
            elif self.curtype == 'RULEBLOCK':
                body.append(self.ruleblock())
            else:
                body.append(self.block())
        self.eat('DEDENT')
        return body

    def ruledef(self):
        """ruledef : DISABLED? RULE STRING NEWLINE INDENT (ruleblock | call)+ DEDENT"""
        disabled = self.curtype == 'DISABLED'
        if disabled:
            self.eat('DISABLED')
        self.eat('RULE')
        name = self.curvalue
        self.eat('STRING')
        node = Rule(name=name, disabled=disabled)
        self.eat('NEWLINE', 'INDENT')
        while self.curtype != 'DEDENT':
            if self.curtype == 'RULEBLOCK':
                node.children.append(self.ruleblock())
            else:
                node.children.append(self.primary())
                self.eat('NEWLINE')
        self.eat('DEDENT')
        return node

    def ruleblock(self):
        """ruleblock : (RULEBLOCK block)+"""
        node = Block()
        while self.curtype == 'RULEBLOCK':
            ruleblock = Ruleblock(name=self.curvalue)
            self.eat('RULEBLOCK')
            ruleblock.children.append(self.block())
            node.children.append(ruleblock)
        return node

    def block(self):
        """block : NEWLINE INDENT line DEDENT
                 | line"""
        node = Block()
        if self.curtype == 'NEWLINE':
            self.eat('NEWLINE', 'INDENT')
            while self.curtype != 'DEDENT':
                line = self.line()
                self.in_compare_expr = type(line) == Compare
                if line is not None:
                    node.children.append(line)
            self.eat('DEDENT')
        else:
            line = self.line()
            node.children.append(line)
        return node

    def line(self):
        """line : 
                ( if_stmt
                | while_stmt
                | for_stmt
                | return_stmt
                | expr ASSIGN expr
                | expr
                )? NEWLINE"""
        if self.curtype == 'NEWLINE':
            return self.eat('NEWLINE')
        if self.curtype == 'IF':
            return self.if_stmt()
        if self.curtype == 'WHILE':
            return self.while_stmt()
        if self.curtype == 'FOR':
            return self.for_stmt()
        if self.curtype == 'RETURN':
            return self.return_stmt()
        pos = self.curpos
        node = self.expr()
        if self.curtype == 'ASSIGN':
            op = self.curvalue
            self.eat('ASSIGN')
            node = Assign(left=node, op=op, right=self.expr())
        while self.curtype == 'NEWLINE':
            self.eat('NEWLINE')
        node._pos = pos
        return node

    def if_stmt(self):
        """if_stmt : IF expr : block elif_else"""
        self.eat('IF')
        cond = self.expr()
        self.eat('COLON')
        try:
            true_block = self.block()
        except Errors.ParseError:
            raise Errors.SyntaxError('Invalid block after if statement')
        false_block = self.elif_else()
        node = If(cond=cond, true_block=true_block, false_block=false_block)
        return node

    def elif_else(self):
        """elif_else : (elif expr : block)* (else : block)?"""
        if self.curtype == 'ELIF':
            self.eat('ELIF')
        elif self.curtype == 'ELSE':
            self.eat('ELSE')
            self.eat('COLON')
            try:
                return self.block()
            except Errors.ParseError:
                raise Errors.SyntaxError('Invalid block after else statement')
        else:
            return None
        cond = self.expr()
        self.eat('COLON')
        try:
            true_block = self.block()
        except Errors.ParseError:
            raise Errors.SyntaxError('Invalid block after elif statement')
        false_block = self.elif_else()
        return If(cond=cond, true_block=true_block, false_block=false_block)

    def while_stmt(self):
        """while_stmt : WHILE expr : block"""
        self.eat('WHILE')
        cond = self.expr()
        self.eat('COLON')
        body = self.block()
        return While(cond=cond, body=body)

    def for_stmt(self):
        """for_stmt : FOR NAME IN primary : block"""
        self.eat('FOR')
        pointer = self.variable()
        self.eat('IN')
        iterable = self.primary()
        self.eat('COLON')
        body = self.block()
        node = For(pointer=pointer, iterable=iterable, body=body)
        return node

    def return_stmt(self):
        """return_stmt : RETURN expr? NEWLINE"""
        self.eat('RETURN')
        expr = None
        if self.curtype != 'NEWLINE':
            expr = self.expr()
        self.eat('NEWLINE')
        return Return(value=expr)

    def expr(self):
        """expr : logic_or"""
        node = self.logic_or()
        node._pos = self.curpos
        return node

    def logic_or(self):
        """logic_or : logic_and (OR logic_and)*"""
        node = self.logic_and()
        while self.curtype == 'OR':
            self.eat('OR')
            node = BinaryOp(left=node, op='or', right=self.logic_and())
        return node

    def logic_and(self):
        """logic_and : logic_not (AND logic_not)*"""
        node = self.logic_not()
        while self.curtype == 'AND':
            self.eat('AND')
            node = BinaryOp(left=node, op='and', right=self.logic_not())
        return node

    def logic_not(self):
        """logic_not : NOT logic_not
                     | compare"""
        if self.curtype == 'NOT':
            self.eat('NOT')
            return UnaryOp(op='not', right=self.logic_not())
        return self.compare()

    def compare(self):
        """compare : term (COMPARE term)*"""
        node = self.term()
        while self.curtype in ('COMPARE', 'IN', 'NOT_IN') and self.peek().type not in ('COMMA', 'RPAREN', 'RBRACK', 'COMPARE', 'NEWLINE'):
            op = self.curvalue
            self.eat(self.curtype)
            node = Compare(left=node, op=op, right=self.expr())
        return node

    def term(self):
        """term : factor ((PLUS | MINUS) factor)*"""
        node = self.factor()
        while self.curtype in ('PLUS', 'MINUS'):
            op = self.curvalue
            self.eat(self.curtype)
            node = BinaryOp(left=node, op=op, right=self.factor())
        return node

    def factor(self):
        """factor : powmod ((TIMES | DIVIDE) powmod)*"""
        node = self.powmod()
        while self.curtype in ('TIMES', 'DIVIDE'):
            op = self.curvalue
            self.eat(self.curtype)
            node = BinaryOp(left=node, op=op, right=self.powmod())
        return node

    def powmod(self):
        """powmod : unary ((POW | MOD) unary)*"""
        node = self.unary()
        while self.curtype in ('POW', 'MOD'):
            op = self.curvalue
            self.eat(self.curtype)
            node = BinaryOp(left=node, op=op, right=self.unary())
        return node

    def unary(self):
        """unary : (PLUS | MINUS) unary
                 | primary"""
        if self.curtype in ('PLUS', 'MINUS'):
            while self.curtype in ('PLUS', 'MINUS'):
                op = self.curvalue
                self.eat(self.curtype)
                node = UnaryOp(op=op, right=self.unary())
        else:
            node = self.primary()
        return node

    def primary(self):
        """primary : atom trailer*"""
        node = self.atom()
        while self.curtype in ('DOT', 'LPAREN', 'LBRACK'):
            pos = self.curpos
            node = self.trailer()(parent=node)
            node._pos = pos
        return node

    def atom(self):
        """atom : variable
                | vector
                | string
                | array
                | TIME
                | OWID args?
                | FLOAT
                | INTEGER
                | ( expr )"""
        pos = self.curpos
        if self.curtype == 'OWID':
            name = self.curvalue.upper()
            for key, aliases in ALIASES.items():
                name = aliases.get(name, name)
            node = Workshop[name]
            self.eat('OWID')
            if type(node) == OWID:
                args = self.args()
                if args:
                    node.children.extend(args)
        elif self.curtype in ('GVAR', 'PVAR', 'NAME'):
            node = self.variable()
        elif self.curvalue == '<':
            node = self.vector()
        elif self.curtype in ('STRING', 'F_STRING'):
            node = self.string()
        elif self.curtype == 'TIME':
            node = Time(value=self.curvalue)
            self.eat('TIME')
        elif self.curtype in ('FLOAT', 'INTEGER'):
            node = Number(value=self.curvalue)
            self.eat(self.curtype)
        elif self.curtype == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
        elif self.curtype == 'LBRACK':
            node = self.array()
        else:
            pos = (self.curtoken.line, self.curtoken.column)
            raise Errors.ParseError('Unexpected token of type {}'.format(self.curtype), pos=pos)
        node._pos = pos
        return node

    def args(self):
        """args : block
                | ( arg_list )"""
        node = None
        if self.curtype == 'LPAREN':
            self.eat('LPAREN')
            node = self.arglist()
            self.eat('RPAREN')
        elif self.peek().type == 'INDENT':
            node = self.block().children
        return node

    def arglist(self):
        """arglist : expr (, expr)*"""
        node = Block()
        node.children.append(self.expr())
        while self.curtype == 'COMMA':
            self.eat('COMMA')
            node.children.append(self.expr())
        return node.children

    def variable(self):
        """variable : GVAR NAME
                    | PVAR (@ primary)? NAME
                    | NAME"""
        pos = self.curpos
        try:
            if self.curtype == 'GVAR':
                self.eat('GVAR')
                name = self.curvalue
                self.eat('NAME')
                node = GlobalVar(name='gvar_' + name)
            elif self.curtype == 'PVAR':
                self.eat('PVAR')
                name = self.curvalue
                self.eat('NAME')
                node = PlayerVar(name='pvar_' + name)
                if self.curvalue == '@':
                    self.eat('AT')
                    node.player = self.primary()
            elif self.curtype == 'NAME':
                name = self.curvalue
                self.eat('NAME')
                node = GlobalVar(name='gvar_' + name)
        except Errors.ParseError:
            raise Errors.SyntaxError('Invalid variable')
        node._pos = pos
        return node

    def vector(self):
        """vector : < expr , expr , expr >"""
        node = Vector()
        self.eat('COMPARE')
        node.children.append(self.expr())
        self.eat('COMMA')
        node.children.append(self.expr())
        self.eat('COMMA')
        node.children.append(self.expr())
        self.eat('COMPARE')
        return node

    def array(self):
        """array : [ arglist? ]"""
        node = Array()
        self.eat('LBRACK')
        if self.curtype != 'RBRACK':
            node.elements.extend(self.arglist())
        self.eat('RBRACK')
        return node

    def string(self):
        """string : STRING
                  | F_STRING args?"""
        pos = self.curpos
        if self.curtype == 'STRING':
            node = String(value=self.curvalue.strip('"').strip("'"))
            self.eat('STRING')
            node.children = [Constant(name='Null')] * 3
        else:
            string = self.curvalue
            num_params = string.count('{')
            formats = []
            self.eat('F_STRING')
            if num_params > 0:
                formats = self.args()
            try:
                assert len(formats) == num_params
            except AssertionError:
                raise Errors.SyntaxError('String \'{}\' expected {} parameters, received {}'.format(string, num_params, len(formats)))
            node = self.parse_string(string, formats)
        node._pos = pos
        return node

    def trailer(self):
        """trailer : DOT NAME
                   | LPAREN arglist? RPAREN"""
        if self.curtype == 'DOT':
            self.eat('DOT')
            name = self.curvalue
            self.eat('NAME')
            return partial(Attribute, name=name)
        elif self.curtype == 'LPAREN':
            self.eat('LPAREN')
            args = []
            if self.curtype != 'RPAREN':
                args = self.arglist()
            self.eat('RPAREN')
            return partial(Call, args=args)
        elif self.curtype == 'LBRACK':
            self.eat('LBRACK')
            index = self.expr()
            self.eat('RBRACK')
            return partial(Item, index=index)