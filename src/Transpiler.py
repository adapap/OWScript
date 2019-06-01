import AST
from collections import defaultdict
from itertools import count
from string import capwords
class Scopes:
    def __init__(self):
        pass # do the scope thingy


class Transpiler:
    """Parses an AST into a string of Workshop code."""
    def __init__(self, tree):
        self.tree = tree
        self.code = ''
        self.indent_size = 3
        self.indent_level = 0
        self.global_vars = {}
        self.player_vars = {}
        self.global_index = count()
        self.player_index = defaultdict(count)
        self.line_count = 0
        self.functions = {}

    @property
    def tabs(self):
        return ' ' * self.indent_size * self.indent_level

    def array_modify(self, array, elem, index):
        self.code += f'Append To Array(Append To Array(Array Slice('
        if type(array) == str:
            self.code += array
        else:
            self.visit(array)
        self.code += f', 0, '
        self.visit(index)
        self.code += '), '
        if type(elem) == AST.ArrayModify:
            self.code += 'Append To Array(Empty Array, '
        self.visit(elem)
        if type(elem) == AST.ArrayModify:
            self.code += ')'
        self.code += '), Array Slice('
        if type(array) == str:
            self.code += array
        else:
            self.visit(array)
        self.code += f', Add('
        self.visit(index)
        self.code += ', 1), Count Of('
        if type(array) == str:
            self.code += array
        else:
            self.visit(array)
        self.code += ')))'

    def assign(self, name, value='0', scope='global', player='Event Player'):
        if scope == 'global':
            index = self.global_vars.get(name)
            if index is None:
                index = next(self.global_index)
                self.global_vars[name] = index
            self.code += f'Set Global Variable At Index(A, {index}, '
        elif scope == 'player':
            index = self.player_vars.get((player, name))
            if index is None:
                index = next(self.player_index[player])
                self.player_vars[(player, name)] = index
            self.code += f'Set Player Variable At Index({player}, A, {index}, '
        self.visit(value)
        self.code += ')';

    def lookup(self, name, scope='global', player='Event Player'):
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

    def visitScript(self, node):
        for function in node.functions:
            self.visit(function)
        for ruleset in node.rulesets:
            self.visit(ruleset)
        self.code = self.code.rstrip('\n')

    def visitFunction(self, node):
        self.functions[node.name] = node.body

    def visitCall(self, node):
        try:
            body = self.functions[node.func]
            self.visit(body)
        except KeyError:
            self.code += f'<Unknown function {node.func}>'

    def visitRuleset(self, node):
        for rule in node.rules:
            self.visit(rule)

    def visitRule(self, node):
        self.code += f'rule({node.rulename}) ' + '{\n'
        self.indent_level += 1
        for ruleblock in node.rulebody:
            self.visit(ruleblock)
            self.code += '\n'
        self.code = self.code.rstrip('\n') + '\n'
        self.indent_level -= 1
        self.code += '}\n\n'

    def visitRuleblock(self, node):
        if node.type is not None:
            self.code += self.tabs + node.type + ' {\n'
            self.indent_level += 1
            for line in node.block.lines:
                self.code += self.tabs
                self.visit(line)
                self.code += ';\n'
                self.line_count += 1
            self.indent_level -= 1
            self.code += self.tabs + '}\n'
        else:
            for line in node.block.lines:
                self.code += self.tabs
                self.visit(line)
                self.code += ';\n'
                self.line_count += 1

    def visitBlock(self, node):
        for line in node.lines:
            self.visit(line)

    def visitIf(self, node):
        self.line_count = 0
        self.code += 'Skip If(Not('
        self.visit(node.cond)
        self.code += '), '
        code_index = len(self.code)
        self.visit(node.block)
        code_block = self.code[code_index:]
        self.code = self.code[:code_index] + f'{self.line_count});\n'
        self.code += code_block.rstrip('\n').rstrip(';')

    def visitAssign(self, node):
        value = node.right
        if node.op == '+=':
            value = AST.BinaryOp(left=node.left, op='+', right=value)
        if node.op == '-=':
            value = AST.BinaryOp(left=node.left, op='-', right=value)
        if node.op == '*=':
            value = AST.BinaryOp(left=node.left, op='*', right=value)
        if node.op == '/=':
            value = AST.BinaryOp(left=node.left, op='/', right=value)
        if node.op == '^=':
            value = AST.BinaryOp(left=node.left, op='^', right=value)
        if node.op == '%=':
            value = AST.BinaryOp(left=node.left, op='%', right=value)
        if type(node.left) == AST.Item:
            item = node.left
            index = self.lookup(item.array.name)
            if type(item.array) in (AST.Name, AST.GlobalVar):
                self.code += f'Set Global Variable(A, '
            elif type(item.array) == AST.PlayerVar:
                self.code += f'Set Player Variable({item.array.player}, A, '
            inner = AST.ArrayModify(array=item.array, value=value, index=item.index)
            self.array_modify('Global Variable(A)', inner, AST.Numeral(value=str(index)))
            self.code += ')'
        else:
            name = node.left.name
            scope = 'player' if type(node.left) == AST.PlayerVar else 'global'
            player = node.left.player if type(node.left) == AST.PlayerVar else 'Event Player'
            self.assign(name=name, value=value, scope=scope, player=player)

    def visitArrayModify(self, node):
        self.array_modify(node.array, node.value, node.index)

    def visitCompare(self, node):
        if node.op == '==':
            self.visit(node.left)
            self.code += f' {node.op} '
            self.visit(node.right)
        else:
            self.code += 'Compare('
            self.visit(node.left)
            self.code += ', ' + node.op + ', '
            self.visit(node.right)
            self.code += ')'

    def visitOr(self, node):
        self.code += 'Or('
        self.visit(node.left)
        self.code += ', '
        self.visit(node.right)
        self.code += ')'

    def visitAnd(self, node):
        self.code += 'And('
        self.visit(node.left)
        self.code += ', '
        self.visit(node.right)
        self.code += ')'

    def visitNot(self, node):
        self.code += 'Not('
        self.visit(node.right)
        self.code += ')'

    def visitValue(self, node):
        self.code += node.value
        if node.args:
            self.code += '('
            for arg in node.args:
                if type(arg) == AST.Block:
                    for line in arg.lines:
                        self.visit(line)
                        self.code += ', '
                else:
                    self.visit(arg)
                    self.code += ', '
            self.code = self.code.rstrip(', ') + ')'

    def visitAction(self, node):
        self.code += node.value
        if node.args:
            self.code += '('
            for arg in node.args:
                if type(arg) == AST.Block:
                    for line in arg.lines:
                        self.visit(line)
                        self.code += ', '
                else:
                    self.visit(arg)
                    self.code += ', '
            self.code = self.code.rstrip(', ') + ')'

    def visitName(self, node):
        if node.value in self.global_vars:
            index = self.lookup(node.value)
            self.code += f'Value In Array(Global Variable(A), {index})'
        else:
            self.code += capwords(node.value)

    def visitNumeral(self, node):
        self.code += node.value

    def visitBinaryOp(self, node):
        if node.op == '+':
            self.code += 'Add('
        elif node.op == '-':
            self.code += 'Subtract('
        elif node.op == '*':
            self.code += 'Multiply('
        elif node.op == '/':
            self.code += 'Divide('
        elif node.op == '^':
            self.code += 'Raise To Power('
        elif node.op == '%':
            self.code += 'Modulo('
        self.visit(node.left)
        self.code += ', '
        self.visit(node.right)
        self.code += ')'

    def visitArray(self, node):
        if not node.elements:
            self.code += 'Empty Array'
        else:
            num_elems = len(node.elements)
            self.code += 'Append To Array(' * num_elems
            self.code += 'Empty Array, '
            for elem in node.elements:
                self.visit(elem)
                self.code += '), '
            self.code = self.code.rstrip(', ')

    def visitItem(self, node):
        self.code += 'Value In Array('
        self.visit(node.array)
        self.code += ', '
        self.visit(node.index)
        self.code += ')'

    def visitTime(self, node):
        time = node.value
        if time.endswith('ms'):
            time = float(time.rstrip('ms')) / 1000
        elif time.endswith('s'):
            time = float(time.rstrip('s'))
        elif time.endswith('min'):
            time = float(time.rstrip('min')) * 60
        self.code += str(round(time, 3))

    def visitPlayerVar(self, node):
        index = self.lookup(name=node.name, scope='player', player=node.player)
        self.code += f'Value In Array(Player Variable('
        if type(node.player) != str:
            self.visit(node.player)
        else:
            self.code += node.player
        self.code += f', A), {index})'

    def visitGlobalVar(self, node):
        index = self.lookup(name=node.name)
        self.code += f'Value In Array(Global Variable(A), {index})'

    def run(self):
        self.visit(self.tree)
        #print(self.code)
        return self.code

    def visit(self, node):
        method_name = 'visit' + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node)