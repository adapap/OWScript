class AST:
    pass

class Ruleset(AST):
    def __init__(self, rules=None):
        self.rules = rules or []

    def __repr__(self):
        return ('_' * 50 + '\n').join(repr(x) for x in self.rules)

class Rule(AST):
    def __init__(self, rulename, event=None, conditions=None, actions=None):
        self.rulename = rulename
        self.event = event
        self.conditions = conditions
        self.actions = actions

    def __repr__(self):
        return 'Rule {}\n\t{}\n\t{}\n\t{}\n' \
            .format(self.rulename, self.event, self.conditions, self.actions)

class Ruleblock(AST):
    def __init__(self, block=None):
        self.block = block

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.block}'

class Event(Ruleblock):
    pass

class Conditions(Ruleblock):
    pass

class Actions(Ruleblock):
    pass

class Block(AST):
    def __init__(self, statements=None):
        self.statements = statements or []

    def __repr__(self):
        return f'{self.statements}'

class Value(AST):
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []

    def __repr__(self):
        return f'{self.name}: {self.args}'

class GlobalVar(Value):
    def __repr__(self):
        return f'gVar {self.name}'

class PlayerVar(Value):
    def __repr__(self):
        return f'pVar {self.name}'

class Type(AST):
    def __init__(self, value, args=None):
        self.value = value
        self.args = args or []

    def __repr__(self):
        return f'{self.value} {self.args}'

class Number(Type):
    pass

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f'<{self.left} {self.op} {self.right}>'

class Assign(BinaryOp):
    pass

class Compare(BinaryOp):
    pass