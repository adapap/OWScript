class AST:
    pass

class Script(AST):
    def __init__(self, statements=None):
        self.statements = statements or []

    def __repr__(self):
        return f'{self.statements}'

class Ruleset(AST):
    def __init__(self, rules=None):
        self.rules = rules or []

    def __repr__(self):
        rules = '\n'.join(map(repr, self.rules))
        return f'{rules}'

class Rule(AST):
    def __init__(self, rulename='', rulebody=None):
        self.rulename = rulename
        self.rulebody = rulebody or []

    def __repr__(self):
        ruleblocks = '\n\t'.join(map(repr, self.rulebody))
        return f'Rule {self.rulename}\n\t{ruleblocks}\n'

class Ruleblock(AST):
    def __init__(self, type_=None, block=None):
        self.type = type_
        self.block = block

    def __repr__(self):
        return f'{self.type}: {self.block}'

class Block(AST):
    def __init__(self, lines=None):
        self.lines = lines or []

    def __repr__(self):
        return f'{self.lines}'

class BinaryOp(AST):
    def __init__(self, left=None, op=None, right=None):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'{self.left} {self.op} {self.right}'

class Assign(BinaryOp):
    pass

class Compare(BinaryOp):
    pass

class Or(BinaryOp):
    pass

class And(BinaryOp):
    pass

class UnaryOp(AST):
    def __init__(self, op=None, right=None):
        self.op = op
        self.right = right

    def __repr__(self):
        return f'{self.op}{self.right}'

class Negate(UnaryOp):
    pass

class Not(UnaryOp):
    def __repr__(self):
        return f'{self.op} {self.right}'

class Type(AST):
    def __init__(self, value, args=None):
        self.value = value
        self.args = args or []

    def __repr__(self):
        if self.args:
            return f'{self.value}: {self.args}'
        return f'{self.value}'

class Value(Type):
    pass

class Action(Type):
    pass

class Constant(AST):
    def __init__(self, value):
        self.value = value
        self.name = value

    def __repr__(self):
        return f'{self.value}'

class Numeral(Constant):
    pass

class Name(Constant):
    pass

class Time(Constant):
    pass

class GlobalVar(AST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class PlayerVar(AST):
    def __init__(self, name, player=None):
        self.name = name
        self.player = player or 'Event Player'

    def __repr__(self):
        return f'{self.name}@{self.player}'

class Array(AST):
    def __init__(self, elements=None):
        self.elements = elements or []

    @property
    def length(self):
        return len(self.elements)

    def push(self, elem):
        self.elements.append(elem)

    def pop(self):
        return self.elements.pop()

    def __setitem__(self, index, value):
        if index > self.length - 1:
            while index > self.length - 1:
                self.push(Numeral(value=0))
        self.elements[index] = value

    def __repr__(self):
        return f'{self.elements}'

class Contains(AST):
    def __init__(self, value, array):
        self.value = value
        self.array = array

    def __repr__(self):
        return f'{self.value} in {self.array}'

class ArrayItem(AST):
    def __init__(self, array, item):
        self.array = array
        self.name = array.name
        self.item = item

    def __repr__(self):
        return f'{self.name}{self.item}'

class Item(AST):
    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return f'[{self.index}]'

class Function(AST):
    def __init__(self, name, params=None, body=None):
        self.name = name
        self.params = params or []
        self.body = body

    def __repr__(self):
        return f'%{self.name}({self.params})'

class Call(AST):
    def __init__(self, func, args=None):
        self.func = func
        self.args = args

    def __repr__(self):
        return f'{self.func}({self.args})'

class Attr(AST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'

class Attribute(AST):
    def __init__(self, value, arg):
        self.value = value
        self.arg = arg

    def __repr__(self):
        return f'{self.value}({self.arg})'

class If(AST):
    def __init__(self, cond, block, elif_conds, elif_blocks, else_block):
        self.cond = cond
        self.block = block
        self.elif_conds = elif_conds
        self.elif_blocks = elif_blocks
        self.else_block = else_block

    def __repr__(self):
        return f'if ... elif ... * {len(self.elif_conds)} else ...'

class While(AST):
    def __init__(self, cond, block):
        self.cond = cond
        self.block = block

    def __repr__(self):
        return f'while {self.expr}: ...'