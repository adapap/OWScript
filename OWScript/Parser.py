from collections import deque
from functools import partial

try:
    from . import Errors
    from .AST import *
except ImportError:
    import Errors
    from AST import *

class Parser:
    """OWScript Grammar
script : (NEWLINE | stmt)* EOF
stmt : (funcdef | ruleset | NAME call)

funcdef : '%' NAME param_list? funcbody
funcbody : (NEWLINE INDENT (ruleset | ruledef | rulebody) DEDENT) | block

ruleset : (ruledef NEWLINE?)+;
ruledef : RULE rulename (NEWLINE INDENT rulebody+ DEDENT)+
rulename : (STRING | name)+;
rulebody : RULEBLOCK ruleblock #RulebodyBlock
         | primary call NEWLINE #RCall

ruleblock : block;
block : NEWLINE INDENT line+ DEDENT
      | line;
line : assign
     | if_stmt
     | while_stmt
     | for_stmt
     | const
     | action
     | value
     | expr comp_op=('<'|'>'|'=='|'>='|'<='|'!=') expr
     | name (call | method)?
     | ANNOTATION line
     | NEWLINE;

assign : expr ASSIGN expr
if_stmt : IF expr ':' block (ELIF expr ':' block)* (ELSE ':' else_block=block)?
while_stmt : WHILE expr ':' block
for_stmt : FOR NAME IN expr ':' block
expr : logic_or;
logic_or : logic_and (OR logic_and)*
logic_and : logic_not (AND logic_not)*
logic_not : (NOT logic_not) | compare
compare : arith (('<'|'>'|'=='|'>='|'<='|'!='|IN|NOT IN) arith)*?
arith : unary ('^' arith)* # Pow
      | unary ('*' arith)* # Mul
      | unary ('/' arith)* # Div
      | unary ('+' arith)* # Add
      | unary ('-' arith)* # Sub
      | unary ('%' arith)* # Mod
unary : ('+' | '-') unary | primary

primary : ( action
        | value
        | const
        | name
        | variable
        | vector
        | time
        | numeral
        | array
        | string
        | '(' expr ')') trailer*
action : ACTION after_line
value : VALUE after_line attribute*
const : CONST attribute*
string : STRING
       | F_STRING after_line;
after_line : '(' arg_list ')'
           | NEWLINE INDENT (expr|ANNOTATION expr|NEWLINE)+ DEDENT
           | NEWLINE
param_list : '(' NAME (',' NAME)* ')'
arg_list : expr (',' expr)*

trailer : item
        | method
        | call
item : '[' primary ']'
call : '(' arg_list? ')'
attribute : '.' name
method : attribute call

name : NAME;
time : numeral ('MS' | 'S' | 'MIN')
numeral : num_const=FLOAT
        | num_const=INTEGER
variable : global_var
         | player_var
         | name
global_var : GVAR varname=NAME
player_var : PVAR varname=NAME ('@' primary)?
vector : '<' unary ',' unary ',' unary '>'
array : '[' arg_list? ']'
"""
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
    def curvalue(self):
        """Returns the value of the current token."""
        return self.curtoken.value

    def peek(self, n=1):
        """Returns the nth upcoming token."""
        try:
            return self.tokens[self.pos + n]
        except IndexError:
            print('Cannot peek further than token length.')
    
    def eat(self, *tokens):
        """Consumes a token and moves on to the next one."""
        if len(tokens) > 1:
            for token in tokens:
                self.eat(token)
            return
        # print(self.curtoken)
        token_type = tokens[0]
        if self.curtype == token_type:
            self.pos += 1
        else:
            raise Errors.ParseError('Expected token of type {}, but received {} on line {}:{}'.format(token_type, self.curtype, self.curtoken.line, self.curtoken.column))

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
        """stmt : (funcdef | ruledef | call)"""
        if self.curvalue == '%':
            print('funcdef!')
        elif self.curtype == 'RULE':
            return self.ruledef()
        else:
            print('call!', self.curtype)

    def ruledef(self):
        """ruledef : RULE STRING block"""
        self.eat('RULE')
        node = Rule(name=self.string())
        node.children.append(self.ruleblock())
        return node

    def ruleblock(self):
        """ruleblock : NEWLINE INDENT RULEBLOCK block DEDENT"""
        node = Block()
        self.eat('NEWLINE', 'INDENT')
        while self.curtype == 'RULEBLOCK':
            ruleblock = Ruleblock(name=self.curvalue)
            self.eat('RULEBLOCK')
            ruleblock.children.append(self.block())
            node.children.append(ruleblock)
        self.eat('DEDENT')
        return node

    def block(self):
        """block : NEWLINE INDENT line DEDENT
                 | line"""
        node = Block()
        if self.curtype == 'NEWLINE':
            self.eat('NEWLINE', 'INDENT')
            while self.curtype != 'DEDENT':
                line = self.line()
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
                | expr ASSIGN expr
                | expr COMPARE expr
                | expr
                )? NEWLINE"""
        if self.curtype == 'NEWLINE':
            return self.eat('NEWLINE')
        if self.curtype == 'IF':
            return self.if_stmt()
        node = self.expr()
        if self.curtype == 'ASSIGN':
            op = self.curvalue
            self.eat('ASSIGN')
            node = Assign(left=node, op=op, right=self.expr())
        elif self.curtype == 'COMPARE':
            op = self.curvalue
            self.eat('COMPARE')
            node = Compare(left=node, op=op, right=self.expr())
        while self.curtype == 'NEWLINE':
            self.eat('NEWLINE')
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

    def expr(self):
        """expr : logic_or"""
        return self.logic_or()

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
        while self.curtype == 'COMPARE':
            if node.children:
                break
            op = self.curvalue
            if op == '>' and self.peek().type in ('DEDENT', 'RPAREN', 'COMMA'):
                break
            self.eat('COMPARE')
            node = Compare(left=node, op=op, right=self.term())
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
            node = self.trailer()(parent=node)
        return node

    def atom(self):
        """atom : variable
                | vector
                | string
                | array
                | OWID args?
                | FLOAT
                | INTEGER
                | ( expr )"""
        if self.curtype == 'OWID':
            node = OWID(name=self.curvalue)
            self.eat('OWID')
            args = self.args()
            if args:
                node.children.extend(args)
        elif self.curtype in ('GVAR', 'PVAR', 'NAME'):
            node = self.variable()
        elif self.curtype == 'COMPARE' and self.curvalue == '<':
            node = self.vector()
        elif self.curtype in ('STRING'):
            node = self.string()
        elif self.curtype in ('FLOAT', 'INTEGER'):
            node = Numeral(value=self.curvalue)
            self.eat(self.curtype)
        elif self.curtype == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
        elif self.curtype == 'LBRACK':
            node = self.array()
        else:
            raise Errors.ParseError('Unexpected token of type {} on line {}:{}'.format(self.curtype, self.curtoken.line, self.curtoken.column))
        return node

    def args(self):
        """args : block
                | ( arg_list )"""
        node = None
        if self.peek().type == 'INDENT':
            node = self.block().children
        elif self.curtype == 'LPAREN':
            self.eat('LPAREN')
            node = self.arglist().children
            self.eat('RPAREN')
        return node

    def arglist(self):
        """arglist : expr ( , expr)*"""
        node = Block()
        node.children.append(self.expr())
        while self.curtype == 'COMMA':
            self.eat('COMMA')
            node.children.append(self.expr())
        return node

    def variable(self):
        """variable : GVAR NAME
                    | PVAR (@ primary)? NAME
                    | NAME"""
        if self.curtype == 'GVAR':
            self.eat('GVAR')
            name = self.curvalue
            self.eat('NAME')
            node = GlobalVar(name=name)
        elif self.curtype == 'PVAR':
            self.eat('PVAR')
            name = self.curvalue
            self.eat('NAME')
            node = PlayerVar(name=name)
            if self.curvalue == '@':
                self.eat('AT')
                node.player = self.primary()
        elif self.curtype == 'NAME':
            name = self.curvalue
            self.eat('NAME')
            node = GlobalVar(name=name)
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
            node.elements.extend(self.arglist().children)
        self.eat('RBRACK')
        return node

    def string(self):
        """string : STRING"""
        node = String(value=self.curvalue)
        self.eat('STRING')
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
            args = self.arglist().children
            self.eat('RPAREN')
            return partial(Call, args=args)
        elif self.curtype == 'LBRACK':
            self.eat('LBRACK')
            index = self.expr()
            self.eat('RBRACK')
            return partial(Item, index=index)