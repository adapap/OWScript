class AST:
    children = []
    def __init__(self):
        self.children = []

    @property 
    def format_children(self):
        return ', '.join(map(repr, self.children))

    def string(self, indent=0):
        string = ''
        if not self.__class__ == Block:
            string += ' ' * indent + '{}'.format(self.__class__.__name__) + '\n'
        else:
            indent -= 3
        for child in self.children:
            string += child.string(indent=indent + 3)
        return string

    def __repr__(self):
        if not self.children:
            return self.__class__.__name__
        return '{}({})'.format(self.__class__.__name__, self.format_children)

class Terminal(AST):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return '{}'.format(self.value)

class Data(AST):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.__class__.__name__ + self.name)

    def __repr__(self):
        if not self.children:
            return self.name
        return '{}({})'.format(self.name, self.format_children)

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)

class UnaryOp(AST):
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return '{} {}'.format(self.op, self.right)

class Trailer(AST):
    def __init__(self, parent):
        self.parent = parent

class Script(AST):
    pass

class Rule(Data):
    pass

class Ruleblock(Data):
    pass

class Block(AST):
    def __repr__(self):
        return '{}'.format(self.format_children)

class Const(Terminal):
    pass

class String(Terminal):
    pass

class Time(Terminal):
    pass

class Numeral(Terminal):
    pass

class OWID(Data):
    pass

class Array(AST):
    def __init__(self, elements=None):
        self.elements = elements or []

    def append(self, elem):
        self.elements.append(elem)

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __setitem__(self, index, item):
        while index > len(self) - 1:
            self.append(Numeral('0'))
        self.elements.__setitem__(index, item)

    def __repr__(self):
        return '{}'.format(self.elements)

class Compare(BinaryOp):
    pass

class Assign(BinaryOp):
    pass

class Vector(AST):
    pass

class GlobalVar(Data):
    vartype = 'global'

class PlayerVar(Data):
    vartype = 'player'
    def __init__(self, name, player=None):
        super().__init__(name)
        self.player = player or OWID(name='Event Player')

class If(AST):
    def __init__(self, cond, true_block, false_block=None):
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return 'if {}: {} | else: {}'.format(self.cond, self.true_block, self.false_block)

class While:
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body
    
    def __repr__(self):
        return 'while {}: {}'.format(self.cond, self.body)

class For:
    def __init__(self, pointer, iterable, body):
        self.pointer = pointer
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return 'for {} in {}: {}'.format(self.pointer, self.iterable, self.body)

class Function(AST):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params

    def __repr__(self):
        return '%{}({}): {}'.format(self.name, ', '.join(map(repr, self.params)), self.format_children)

class Attribute(Trailer):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.name = name

    def __repr__(self):
        return '{}.{}'.format(self.parent, self.name)

class Call(Trailer):
    def __init__(self, args, parent):
        super().__init__(parent)
        self.args = args

    def __repr__(self):
        return '{}({})'.format(self.parent, self.args)

class Item(Trailer):
    def __init__(self, index, parent):
        super().__init__(parent)
        self.index = index

    def __repr__(self):
        return '{}[{}]'.format(self.parent, self.index)