class AST:
    def __repr__(self):
        return f'<{self.__class__.__name__}>'

class Map(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Ruleset(AST):
    def __init__(self, maps=[], rules=[]):
        self.maps = maps
        self.rules = rules

class Rule(AST):
    def __init__(self, name, event=None, conditions=[], actions=[]):
        self.name = name
        self.event = event
        self.conditions = conditions
        self.actions = actions

    def __repr__(self):
        return f'<Rule: {self.name}>'

class Rulegroup(AST):
    def __init__(self, block=None):
        self.block = block

class Block(AST):
    def __init__(self, statements=[]):
        self.statements = statements

class Event(Rulegroup):
    pass

class Conditions(Rulegroup):
    pass

class Condition(AST):
    def __init__(self, cond, value):
        self.cond = cond
        self.value = value

class Actions(Rulegroup):
    pass

class Array(AST):
    def __init__(self, value, block):
        self.value = value
        self.block = block

class Name(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.value}>'

class Value(AST):
    def __init__(self, value, params=[]):
        self.value = value
        self.params = params

class Number(AST):
    def __init__(self, value):
        self.value = value

class Integer(Number):
    pass

class Float(Number):
    pass

class Boolean(Name):
    pass

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'<{self.left} {self.op} {self.right}>'

class Compare(BinaryOp):
    pass

class Assign(BinaryOp):
    pass