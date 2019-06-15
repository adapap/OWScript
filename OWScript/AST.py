class AST:
    def __init__(self):
        self.children = []

    @property 
    def format_children(self):
        return ', '.join(map(repr, self.children))

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

class Numeral(Terminal):
    pass

class OWID(Data):
    pass

class Array(AST):
    def __init__(self):
        self.elements = []

    def append(self, elem):
        self.elements.append(elem)

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