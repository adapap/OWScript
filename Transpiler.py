import AST
import string
from collections import defaultdict
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
        self.player_index = defaultdict(count)
        self.inline = 0

    @property
    def tabs(self):
        return '\t' * self.indent_level

    def assign_var(self, name, value='0', scope='global', player='Event Player'):
        if scope == 'global':
            index = self.global_vars.get(name)
            if index is None:
                index = next(self.global_index)
                self.global_vars[name] = index
            self.code += self.tabs + f'Set Global Variable At Index(A, {index}, '
        elif scope == 'player':
            index = self.player_vars.get((player, name))
            if index is None:
                index = next(self.player_index[player])
                self.player_vars[(player, name)] = index
            self.code += self.tabs + f'Set Player Variable At Index({player}, A, {index}, '
        self.visit(value)
        self.code += ');\n'

    def lookup_var(self, name, scope='global', player='Event Player'):
        if scope == 'global':
            index = self.global_vars.get(name)
            if index is None:
                index = self.global_vars[name] = next(self.global_index)
            return index
        elif scope == 'player':
            index = self.player_vars.get((player, name))
            if index is None:
                index = self.player_vars[(player, name)] = next(self.player_index[player])
            return index


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
        self.code += 'rule(' + node.rulename + ') {\n'
        if node.event:
            self.indent_level += 1
            self.code += self.tabs + 'event {\n'
            self.visit(node.event.block)
            self.code += self.tabs + '}\n\n'
            self.indent_level -= 1
        if node.conditions:
            self.indent_level += 1
            self.code += self.tabs + 'conditions {\n'
            self.visit(node.conditions.block)
            self.code += self.tabs + '}\n\n'
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
        name = node.left.value if type(node.left) == AST.Name else node.left.name
        if type(node.left) == AST.GlobalVar or type(node.left) == AST.Name:
            self.assign_var(name=name, value=node.right, scope='global')
        elif type(node.left) == AST.PlayerVar:
            self.assign_var(name=name, value=node.right, scope='player')
        else:
            print('NODE:', node.left, type(node.left))

    def visit_Compare(self, node):
        self.code += self.tabs
        self.visit(node.left)
        self.code += f' {node.op} '
        self.visit(node.right)
        self.code += ';\n'

    def visit_Value(self, node):
        self.code += string.capwords(node.name)
        if node.args:
            self.code += '('
            for arg in node.args:
                if arg != '\n':
                    self.visit(arg)
                self.code += ', '
            self.code = self.code[:-2]
            self.code += ')'

    def visit_Number(self, node):
        self.code += string.capwords(node.value) + '('
        if node.block:
            self.visit(node.block)
        self.code += ')'

    def visit_NumberConst(self, node):
        self.code += node.value

    def visit_Name(self, node):
        if node.value in self.global_vars:
            print('is global var', node.value)
        else:
            self.code += self.tabs + string.capwords(node.value) + ';\n'

    def visit_Array(self, node):
        if not node.values:
            self.code += 'Empty Array'
        else:
            self.code += 'WIP['
            for value in node.values:
                print('arr value:', value)
            self.code += ']'

    def visit_PlayerVar(self, node):
        index = self.lookup_var(node.name, scope='player', player=node.player)
        self.code += f'Value In Array(Player Variable({node.player}, A), {index})'

    def visit_Empty(self, node):
        pass