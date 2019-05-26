import AST
from itertools import count

class Transpiler:
    """Transpiles an AST into Overwatch Workshop source code."""
    def __init__(self, tree):
        self.tree = tree
        self.code = ''
        self.indent_level = 0
        self.global_vars = {}
        self.player_vars = {}
        self.global_index = count()
        self.player_index = count()

    @property
    def tabs(self):
        return '\t' * self.indent_level

    def define_var(self, name, value, scope='global'):
        if scope == 'global':
            index = next(self.global_index)
            if index == 0:
                self.code += self.tabs + 'Set Global Variable(A, Empty Array)\n'
            self.code += self.tabs + 'Modify Global Variable(A, Append To Array, '
            self.global_vars[name] = index
        elif scope == 'player':
            index = next(self.player_index)
            if index == 0:
                self.code += self.tabs + 'Set Player Variable(A, Empty Array)\n'
            self.code += self.tabs + 'Modify Player Variable(A, Append To Array, '
        self.visit(value)
        self.code += ')\n'

    def assign_var(self, name, value, scope='global'):
        if scope == 'global':
            index = self.global_vars.get(name)
            self.code += f'Set Global Variable At Index(A, {index}, '
        elif scope == 'player':
            index = self.player_vars.get(name)
            self.code += f'Set Player Variable At Index(A, {index}, '
        self.visit(value)
        self.code += ')\n'

    def run(self):
        self.visit(self.tree)
        #print(self.code)
        return self.code

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Ruleset(self, node):
        for rule in node.rules:
            self.visit(rule)

    def visit_Rule(self, node):
        self.code += 'Rule ' + node.rulename + ' {\n'
        if node.event:
            self.indent_level += 1
            self.code += self.tabs + 'event {\n'
            self.visit(node.event.block)
            self.code += self.tabs + '}'
            self.indent_level -= 1
        if node.conditions:
            self.indent_level += 1
            self.code += self.tabs + 'conditions {\n'
            self.visit(node.conditions.block)
            self.code += self.tabs + '}'
            self.indent_level -= 1
        if node.actions:
            self.indent_level += 1
            self.code += self.tabs + 'actions {\n'
            self.visit(node.actions.block)
            self.code += self.tabs + '}'
            self.indent_level -= 1
        self.code += '\n}'

    def visit_Block(self, node):
        self.indent_level += 1
        for statement in node.statements:
            self.visit(statement)
        self.indent_level -= 1

    def visit_Assign(self, node):
        name = node.left if type(node.left) == str else node.left.name
        if type(node.left) == AST.GlobalVar or type(node.left) == str:
            if name not in self.global_vars:
                self.define_var(name=name, value=node.right, scope='global')
            else:
                self.assign_var(name=name, value=node.right, scope='global')
        elif type(node.left) == AST.PlayerVar:
            if name not in self.player_vars:
                self.define_var(name=name, value=node.right, scope='player')
            else:
                self.assign_var(name=name, value=node.right, scope='player')
        else:
            print('NODE:', node.left, type(node.left))

    def visit_Value(self, node):
        self.code += node.name + '('
        for arg in node.args:
            if type(arg) == str:
                self.code += arg + ', '
            else:
                print('Not a string:', arg, type(arg))
                #self.visit(arg)
        self.code = self.code[:-2]
        self.code += ')'