import AST
from collections import defaultdict
from itertools import count
from string import capwords
class Scope:
    def __init__(self, name):
        self.name = name
        self.namespace = {}

    def __repr__(self):
        return f"<Scope '{self.name}'>"

class Transpiler:
    """Parses an AST into a string of Workshop code."""
    def __init__(self):
        self.indent_size = 3
        self.indent_level = 0
        self.global_vars = {}
        self.player_vars = {}
        self.global_index = count()
        self.player_index = defaultdict(count)
        self.line = 0
        self.functions = {}
        self.arrays = {}
        self.scopes = []

    @property
    def tabs(self):
        return ' ' * self.indent_size * self.indent_level

    def clean(self, str_):
        return '('.join(capwords(s) for s in str_.split('('))

    def assign(self, name, value='0', scope='global', player='Event Player'):
        code = ''
        if scope == 'global':
            index = self.global_vars.get(name)
            if index is None:
                index = next(self.global_index)
                self.global_vars[name] = index
            code += f'Set Global Variable At Index(A, {index}, '
        elif scope == 'player':
            index = self.player_vars.get((player, name))
            if index is None:
                index = next(self.player_index[player])
                self.player_vars[(player, name)] = index
            code += f'Set Player Variable At Index({player}, A, {index}, '
        code += self.visit(value) + ')'
        return code

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
        self.scopes.append(Scope(name='global'))
        code = 'rule("Generated using https://github.com/adapap/OWScript") {\n   Event {\n      Ongoing - Global;\n   }\n}\n'
        for statement in node.statements:
            code += self.visit(statement)
        code = code.rstrip('\n')
        self.scopes.pop()
        return code

    def visitFunction(self, node):
        self.functions[node.name] = {
            'body': node.body,
            'params': node.params
        }
        return ''

    def visitCall(self, node):
        code = ''
        try:
            body = self.functions[node.func].get('body')
            params = self.functions[node.func].get('params')
            scope = Scope(name=node.func)
            if params:
                scope.namespace.update(dict(zip(params, node.args)))
            self.scopes.append(scope)
            code = self.visit(body)
            self.scopes.pop()
        except KeyError:
            code = f'<Unknown function {node.func}>'
        return code

    def visitRuleset(self, node):
        code = ''
        for rule in node.rules:
            code += self.visit(rule)
        return code

    def visitRule(self, node):
        rulename = '"'
        for x in node.rulename:
            if type(x) == str:
                rulename += x[1:-1]
            elif type(x) == AST.Name:
                rulename += self.scopes[-1].namespace.get(x.value).value[1:-1]
        rulename += '"'
        code = f'rule({rulename}) ' + '{\n'
        self.indent_level += 1
        for ruleblock in node.rulebody:
            code += self.visit(ruleblock) + '\n'
        code = code.rstrip('\n') + '\n'
        self.indent_level -= 1
        code += '}\n\n'
        return code

    def visitRuleblock(self, node):
        code = ''
        if node.type == 'Function':
            lines = node.block.lines
            code += ';\n'.join([self.tabs + self.visit(line) for line in lines]).lstrip(' ')
        elif node.type is not None:
            code += self.tabs + node.type + ' {\n'
            self.indent_level += 1
            for line in node.block.lines:
                code += self.tabs + self.visit(line) + ';\n'
                self.line += 1
            self.indent_level -= 1
            code += self.tabs + '}\n'
        else:
            for line in node.block.lines:
                code += self.tabs + self.visit(line) + ';\n'
                self.line += 1
        return code

    def visitBlock(self, node):
        code = ''
        for line in node.lines:
            code += self.visit(line)
        return code

    def visitIf(self, node):
        start_line = self.line
        if_cond = self.visit(node.cond)
        if_block = self.visit(node.block)
        if_line = self.line - start_line
        elif_conds = []
        elif_blocks = []
        elif_lines = []
        else_block = None
        else_line = -1
        if node.elif_conds:
            for elif_ in zip(node.elif_conds, node.elif_blocks):
                cond, block = elif_
                elif_conds.append(self.visit(cond))
                elif_blocks.append(self.visit(block))
                elif_lines.append(self.line - start_line - if_line - sum(elif_lines))
        if node.else_block:
            else_block = self.visit(node.else_block)
            else_line = self.line - start_line - if_line - sum(elif_lines)
        if else_block or elif_conds:
            if_line += 1
            elif_lines = list(map(lambda x: x + 1, elif_lines))
        code = f'Skip If(Not({if_cond}), {if_line});\n{if_block}'
        if else_block or elif_conds:
            num_skips = sum(map(lambda x: x + 1, elif_lines)) + else_line
            code += f'{self.tabs}Skip({num_skips});\n'
        for i, elif_ in enumerate(zip(elif_conds, elif_blocks, elif_lines)):
            cond, block, line = elif_
            code += f'{self.tabs}Skip If(Not({cond}), {line});\n{block}'
            if else_block or elif_conds:
                num_skips = sum(map(lambda x: x + 1, elif_lines[i + 1:])) + else_line
                if num_skips > 0:
                    code += f'{self.tabs}Skip({num_skips});\n'
        if else_block:
            code += f'{else_block}'
        return code.rstrip('\n').rstrip(';')

    def visitWhile(self, node):
        start_line = self.line
        block = self.visit(node.block)
        line = self.line - start_line + 2
        code = f'Skip If(Not({self.visit(node.cond)}), {line});\n'
        code += block
        code += f'{self.tabs}Wait(0.001, Ignore Condition);\n'
        code += f'{self.tabs}Loop If({self.visit(node.cond)})'
        return code

    def visitAssign(self, node):
        code = ''
        name = node.left.name
        value = node.right
        if type(node.right) == AST.Array:
            self.arrays[name] = value
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
        if type(node.left) == AST.ArrayItem:
            item = node.left
            item_index = int(self.visit(item.item))
            array = self.arrays[item.name]
            array[item_index] = value
            value = array
            self.arrays[item.name] = value
        scope = 'player' if type(node.left) == AST.PlayerVar else 'global'
        player = node.left.player if type(node.left) == AST.PlayerVar else 'Event Player'
        code += self.assign(name=name, value=value, scope=scope, player=player)
        return code

    def visitCompare(self, node):
        code = ''
        if node.raw:
            code += f'{self.visit(node.left)} {node.op} {self.visit(node.right)}'
        elif node.op == 'in':
            code += f'Array Contains({self.visit(node.right)}, {self.visit(node.left)})'
        elif node.op == 'not in':
            code += f'Not(Array Contains({self.visit(node.right)}, {self.visit(node.left)}))'
        else:
            code += f'Compare({self.visit(node.left)}, {node.op}, {self.visit(node.right)})'
        return code

    def visitOr(self, node):
        return f'Or({self.visit(node.left)}, {self.visit(node.right)})'

    def visitAnd(self, node):
        return f'And({self.visit(node.left)}, {self.visit(node.right)})'

    def visitNot(self, node):
        return f'Not({self.visit(node.right)})'

    def visitValue(self, node):
        code = node.value
        if node.args:
            code += '('
            for arg in node.args:
                if type(arg) == AST.Block:
                    for line in arg.lines:
                        code += self.visit(line) + ', '
                else:
                    code += self.visit(arg) + ', '
            code = code.rstrip(', ') + ')'
        return code

    def visitAction(self, node):
        code = node.value
        if node.value == 'Wait':
            if len(node.args) == 1: # Default: 'Ignore Condition'
                node.args.append(AST.Name(value='Ignore Condition'))
        if node.args:
            code += '('
            for arg in node.args:
                if type(arg) == AST.Block:
                    for line in arg.lines:
                        code += self.visit(line) + ', '
                else:
                    code += self.visit(arg) + ', '
            code = code.rstrip(', ') + ')'
        return code

    def visitName(self, node):
        for i in range(-1, -len(self.scopes) - 1, -1):
            if node.value in self.scopes[i].namespace:
                value = self.scopes[i].namespace.get(node.value)
                if not (type(value) == AST.Name and value.name == node.value):
                    return self.visit(self.scopes[i].namespace.get(node.value))
        if node.value in self.global_vars:
            index = self.lookup(node.value)
            return f'Value In Array(Global Variable(A), {index})'
        else:
            return self.clean(node.value)

    def visitNumeral(self, node):
        return node.value

    def visitString(self, node):
        code = 'String('
        if node.args:
            code += f'"{node.value[1:-1]}", '
            args = [self.visit(arg) for arg in node.args]
            code += ', '.join(args)
            code += (3 - len(args)) * ', Null'
        else:
            code += f'{node.value}, Null, Null, Null'
        code += ')'
        return code

    def visitBinaryOp(self, node):
        code = ''
        if node.op == '+':
            code = 'Add('
        elif node.op == '-':
            code = 'Subtract('
        elif node.op == '*':
            code = 'Multiply('
        elif node.op == '/':
            code = 'Divide('
        elif node.op == '^':
            code = 'Raise To Power('
        elif node.op == '%':
            code = 'Modulo('
        code += f'{self.visit(node.left)}, {self.visit(node.right)})'
        return code

    def visitUnaryOp(self, node):
        code = ''
        if node.op == '-':
            code += '-'
        code += self.visit(node.right)
        return code

    def visitArray(self, node):
        code = ''
        if not node.elements:
            code += 'Empty Array'
        else:
            num_elems = len(node.elements)
            code += 'Append To Array(' * num_elems
            code += 'Empty Array, '
            for elem in node.elements:
                if type(elem) == str:
                    code += elem + '), '
                else:
                    code += self.visit(elem) + '), '
            code = code.rstrip(', ')
        return code

    def visitArrayItem(self, node):
        return f'Value In Array({self.visit(node.array)}, {self.visit(node.item)})'

    def visitItem(self, node):
        return self.visit(node.index)

    def visitAttribute(self, node):
        code = {
            'x': 'X Component Of',
            'y': 'Y Component Of',
            'z': 'Z Component Of',
            'pos': 'Position Of',
            'eyepos': 'Eye Position',
            'facing': 'Facing Direction Of'
        }.get(node.value.lower()) + '('
        code += self.visit(node.arg) + ')'
        return code

    def visitMethod(self, node):
        code = ''
        if node.value == 'push':
            array = self.arrays[node.parent]
            args = [self.visit(arg) for arg in node.args]
            array.push(*args)
            self.arrays[node.parent] = array
            # Change to append to array?
            code += self.assign(name=node.parent, value=array)
        return code

    def visitTime(self, node):
        time = node.value
        if time.endswith('ms'):
            time = float(time.rstrip('ms')) / 1000
        elif time.endswith('s'):
            time = float(time.rstrip('s'))
        elif time.endswith('min'):
            time = float(time.rstrip('min')) * 60
        return str(round(time, 3))

    def visitPlayerVar(self, node):
        index = self.lookup(name=node.name, scope='player', player=node.player)
        code = f'Value In Array(Player Variable('
        if type(node.player) != str:
            code += self.visit(node.player)
        else:
            code += node.player
        code += f', A), {index})'
        return code

    def visitGlobalVar(self, node):
        index = self.lookup(name=node.name)
        return f'Value In Array(Global Variable(A), {index})'

    def run(self, tree):
        return self.visit(tree)

    def visit(self, node):
        method_name = 'visit' + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node)