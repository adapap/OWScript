import os
import re
from itertools import count
from string import ascii_uppercase as letters

from . import Errors
from . import Importer
from .AST import *

def flatten(l):
    """Helper method to convert a list of lists into a single list."""
    l = list(l)
    while l:
        while l and isinstance(l[0], list):
            l[0:1] = l[0]
        if l:
            yield l.pop(0)

class Scope:
    """Keeps track of defined names in a scope context. Handles lookup and assignment."""
    def __init__(self, name, parent=None, namespace=None):
        self.name = name
        self.parent = parent
        self.namespace = namespace or {}
        self.level = parent.level + 1 if parent else 0

    @property
    def all_vars(self):
        keys = list(self.namespace.keys())
        if self.parent:
            keys.extend(self.parent.all_vars)
        return keys

    def get(self, name):
        value = self.namespace.get(name)
        if value is not None:
            return value
        if self.parent:
            return self.parent.get(name)

    def assign(self, name, var):
        self.namespace[name] = var

    def __repr__(self):
        return f"<Scope '{self.name}'[{self.level}]>"

class Builtin:
    """The funcionality of built-in functions for OWScript."""
    def range(tp, *args):
        args = list(map(int, args))
        elements = list(map(Number, map(str, range(*args))))
        array = Array(elements=elements)
        return array

    def ceil(tp, n):
        node = OWID(name='Round To Integer', args=(Number, Any))
        node._pos = n._pos
        node.children.extend([n, Constant(name='Up')])
        return node

    def floor(tp, n):
        node = OWID(name='Round To Integer', args=(Number, Any))
        node._pos = n._pos
        node.children.extend([n, Constant(name='Down')])
        return node

    def get_map(tp):
        node = OWID(name='Index Of Array Value', args=[None] * 2)
        def map_2pos(a, b):
            node = Raw(code='First Of(Filtered Array(Append To Array(Append To Array(Empty Array, {}), {}), Compare(Current Array Element, ==, Value In Array(Global Variable(A), 0))))'.format(a, b))
            return tp.visit(node, tp.scope)
        elems = list(map(lambda x: Number(value=str(x)), [153, 468, 1196, 135, 139, 477, 184, map_2pos(343, 347), 366, map_2pos(433, 436), 403, map_2pos(382, 384), 993, 386, map_2pos(331, 348), 659, 145, 569, 384, 1150, 371, 179, 497, 374, 312, 324, 434, 297, 276, 330, 376, 347, 480, 310, 342, 360, 364, 372, 370, 450, 356, 305]))
        array = Array(elements=elems)
        value = Raw(code='Value In Array(Global Variable(A), 0)')
        node.children.extend([array, value])
        return node

    range: range
    ceil: ceil
    floor: floor
    get_map: get_map

class Transpiler:
    """Compiles a parse tree into a single string output via the `run` method."""
    def __init__(self, tree, path, logger, indent_size=4):
        self.tree = tree
        self.path = path
        self.logger = logger
        self.indent_size = indent_size
        self.indent_level = 0
        # Reserved Global Indices
        # 0: Map ID
        self.global_reserved = 1
        # Generators to return the next available index (or variable letter for chase variables)
        self.global_index = count(self.global_reserved)
        self.player_index = count()
        self.global_letters = iter(letters[1:])
        self.player_letters = iter(letters[1:])

        self.curblock = []
        # Keeps track of absolute import paths to avoid duplicate imports
        self.imports = set()

    @property
    def tabs(self):
        return ' ' * self.indent_size * self.indent_level

    @property
    def min_wait(self):
        return 'Wait(0.016, Ignore Condition)'

    def base_node(self, node):
        """Gets a node that can be evaluated in the current scope (e.g. not an item, property, or call)."""
        while hasattr(node, 'parent'):
            node = node.parent
        return node

    def resolve_skips(self):
        """Resolves for/while* continue skips from placeholder text."""
        skips = []
        skip_to = []
        for line_no, line in enumerate(self.curblock):
            match = re.match(r'\s*//SKIP TO', line)
            if match:
                skips.append(line_no)
                self.curblock[line_no] = re.sub('//SKIP TO', '', line)
            match = re.match(r'\s*//FOR START', line)
            if match:
                skip_to.append(line_no - 1)
                self.curblock[line_no] = re.sub('//FOR START', '', line)
        for skip, jump in zip(skips, skip_to[::-1]):
            self.curblock[skip] = self.curblock[skip].format(jump)

    def resolve_import(self, node, scope):
        """Extends the current parse tree by evaluating the given import path (recursively)."""
        children = self.visit(node, scope).children
        nodes = []
        for child in children:
            if type(child) == Import:
                cur_path = self.path
                self.path = os.path.join(os.path.dirname(self.path), os.path.dirname(node.path)) + '\\'
                result = self.resolve_import(child, scope)
                self.path = cur_path
                if result:
                    nodes = result + nodes
            else:
                nodes.append(child)
        return nodes

    def resolve_name(self, node, scope):
        if type(node) == Var:
            var = scope.get(node.name)
            if not var:
                raise Errors.NameError('\'{}\' is undefined'.format(node.name), pos=node._pos)
            node = var.value
        elif type(node) == BinaryOp:
            node.left = self.resolve_name(node.left, scope)
            node.right = self.resolve_name(node.right, scope)
        return node

    def visitScript(self, node, scope):
        """Root node generates the final code output and resolves all imports."""
        # Shameless plug + base code for `get_map` functionality
        code = r'rule("Generated by https://github.com/adapap/OWScript") { Event { Ongoing - Global; } Actions { Set Global Variable At Index(A, 0, Round To Integer(Add(Distance Between(Nearest Walkable Position(Vector(-500.000, 0, 0)), Nearest Walkable Position(Vector(500, 0, 0))), Distance Between(Nearest Walkable Position(Vector(0, 0, -500.000)), Nearest Walkable Position(Vector(0, 0, 500)))), Down)); }}' + '\n'
        while len(node.children) > 0:
            child = node.children[0]
            if type(child) == Import:
                node.children = self.resolve_import(child, scope) + node.children[1:]
            else:
                code += self.visit(child, scope)
                node.children = node.children[1:]
        return code.rstrip('\n')

    def visitImport(self, node, scope):
        """Handles `#import` tokens, duplicate imports, and invalid paths."""
        file_dir = os.path.dirname(self.path)
        path = os.path.join(file_dir, node.path) + '.owpy'
        if not os.path.exists(path):
            raise Errors.ImportError('File {} could not be found'.format(node.path), pos=node._pos)
        try:
            if path not in self.imports:
                self.imports.add(path)
                result = Importer.import_file(path)
            else:
                self.logger.info('Skipping duplicate import {}'.format(path))
                result = Script()
            return result
        except Exception as ex:
            raise Errors.ImportError('Failed to import \'{}\' due to the following error:\n{}'.format(node.path, ex), pos=node._pos)
    def visitRule(self, node, scope):
        """Creates a basic workshop rule."""
        code = ''
        if node.disabled:
            code += 'disabled '
        code += 'rule('
        code += '"' + ''.join(x if type(x) == str else self.visit(x, scope) for x in node.name) + '"'
        self.indent_level += 1
        code += ') {\n' + '\n'.join(self.visit_children(node, scope)) + '}\n'
        self.indent_level -= 1
        return code

    def visitRaw(self, node, scope):
        """Returns an exact value for a string without further interpretation."""
        return node.code

    def visitFunction(self, node, scope):
        """Defines a user-created function."""
        var = Var(name=node.name, value=node, type_=Var.INTERNAL)
        scope.assign(node.name, var)
        node.closure = scope
        return ''

    def visitBlock(self, node, scope):
        """Visits a collection of statements."""
        code = ''.join(self.visit_children(node, scope))
        return code

    def visitRuleblock(self, node, scope):
        """A rule category such as Events, Conditions, or Actions."""
        code = self.tabs + node.name + ' {\n'
        self.indent_level += 1
        for ruleblock in node.children:
            self.curblock = []
            for line in ruleblock.children:
                result = self.visit(line, scope)
                if result:
                    result = result.rstrip(';\n').split(';\n')
                    for x in result:
                        if x:
                            child = self.tabs + x
                            # Automatically compare any condition to true
                            if node.name.upper() == 'CONDITIONS':
                                child += ' == True'
                            self.curblock.append(child)
            self.resolve_skips()
            code += ';\n'.join(self.curblock)
        self.indent_level -= 1
        code += ';\n' + self.tabs + '}\n'
        return code

    def visitOWID(self, node, scope):
        """A workshop value that takes any number of parameters, such as `Set Facing(...)`."""
        name = node.name.title()
        code = name
        # Autofill WaitBehavior
        if name == 'Wait' and len(node.children) == 1:
            node.children.append(Constant(name='Ignore Condition'))
        if not len(node.args) == len(node.children):
            raise Errors.SyntaxError('\'{}\' expected {} arguments ({}), received {}'.format(
                name, len(node.args), ', '.join(map(lambda arg: arg.__name__, node.args)), len(node.children)),
                pos=node._pos)
        for index, types in enumerate(zip(node.args, node.children[:])):
            arg, child = types
            if arg is None:
                continue
            elif arg == Variable:
                if not type(child) == Var:
                    raise Errors.InvalidParameter('Expected variable in chase variable expression, received {}'.format(
                        child.__class__.__name__), pos=child._pos)
                var = scope.get(child.name)
                if not var:
                    raise Errors.NameError('\'{}\' is undefined'.format(child.name), pos=node._pos)
                if var.data.letter == 'A':
                    letters = self.global_letters if var.type == Var.GLOBAL else self.player_letters
                    try:
                        letter = next(letters)
                        var.data.letter = letter
                        var.data.index = None
                        if var.type == Var.GLOBAL:
                            code = 'Set Global Variable({}, {});\n'.format(letter, self.visit(var.value, scope)) + code
                        elif var.type == Var.PLAYER:
                            code = 'Set Player Variable({}, {}, {});\n'.format(self.visit(var.data.player, scope), letter, self.visit(var.value, scope)) + code
                    except StopIteration:
                        raise Errors.InvalidParameter('Exceeded maximum number of chase variables (25) for this type.', pos=child._pos)
                node.children[index] = var
                continue
            values = list(map(lambda x: x.replace(',', ''), flatten(arg.get_values())))
            if 'ANY' in values:
                continue
            value = self.visit(child, scope).upper()
            if value not in values:
                raise Errors.InvalidParameter('\'{}\' expected type {} for argument {}'.format(
                    name, arg.__name__, index + 1), pos=child._pos)
        children = [self.visit(child, scope) for child in node.children]
        code += '(' + ', '.join(children) + ')'
        return code

    def visitConstant(self, node, scope):
        """A workshop value with no further parameters, such as `Event Player` or `Yellow`."""
        return node.name.title()

    def visitCompare(self, node, scope):
        """Interprets a comparison expression."""
        if node.op.lower() == 'in':
            return 'Array Contains(' + self.visit(node.right, scope) + ', ' + self.visit(node.left, scope) + ')'
        elif node.op.lower() == 'not in':
            return 'Not(Array Contains(' + self.visit(node.right, scope) + ', ' + self.visit(node.left, scope) + '))'
        return 'Compare(' + self.visit(node.left, scope) + f', {node.op}, ' + self.visit(node.right, scope) + ')'

    def visitAssign(self, node, scope):
        """Handles internal variable definition and assignment."""
        code = ''
        value = {
            '+=': BinaryOp(left=node.left, op='+', right=node.right),
            '-=': BinaryOp(left=node.left, op='-', right=node.right),
            '*=': BinaryOp(left=node.left, op='*', right=node.right),
            '/=': BinaryOp(left=node.left, op='/', right=node.right),
            '^=': BinaryOp(left=node.left, op='^', right=node.right),
            '%=': BinaryOp(left=node.left, op='%', right=node.right)
        }.get(node.op, node.right)
        # Define variables
        if type(node.left) == Var:
            var = node.left
            name = var.name
            cur_var = scope.get(name)
            if not cur_var:
                if var.type == Var.GLOBAL:
                    var.data = GlobalVar(letter='A', index=next(self.global_index))
                elif var.type == Var.PLAYER:
                    player = self.resolve_name(var.player, scope)
                    var.data = PlayerVar(letter='A', index=next(self.player_index), player=player)
            elif var.type != Var.GLOBAL and cur_var.type != var.type:
                self.logger.warn('Ignoring type reassign for \'{}\' (Line {}:{})'.format(var.name, *var._pos))
                var = cur_var
            elif cur_var.type != Var.CONST:
                var = cur_var
            else:
                raise Errors.SyntaxError('Cannot assign to const \'{}\''.format(var.name), pos=node._pos)
            var.value = value
            scope.assign(name=name, var=var)
        elif type(node.left) == Item:
            parent = node.left.parent
            name = parent.name
            var = scope.get(name)
            try:
                assert type(var.value) == Array
                index = int(self.visit(node.left.index, scope))
                var.value[index] = value
            except AssertionError:
                raise Errors.SyntaxError('Cannot assign to \'{}\'using indices (value is not an array)'.format(name), pos=node._pos)
            except ValueError:
                raise Errors.NotImplementedError('Array assignment only supports literal integer indices', pos=node._pos)
            scope.assign(name=name, var=var)
        else:
            raise Errors.NotImplementedError('Cannot assign value to {}'.format(type(node.left).__name__), pos=node._pos)
        var = scope.get(name)
        data = var.data
        if var.type == Var.GLOBAL:
            code += 'Set Global Variable At Index({}, {}, {})'.format(data.letter, data.index, self.visit(var.value, scope))
        elif var.type == Var.PLAYER:
            code += 'Set Player Variable At Index({}, {}, {}, {})'.format(self.visit(data.player, scope), data.letter, data.index, self.visit(var.value, scope))
        return code

    def visitIf(self, node, scope):
        """If blocks contain a true and false block to evaluate. To simulate this in workshop, the false block
        is skipped when the condition is true, and vice-versa."""
        cond = self.visit(node.cond, scope)
        skip_code = 'Skip If(Not({}), {});\n'
        skip_false = ''
        true_code = ';\n'.join(self.visit_children(node.true_block, scope)) + ';\n'
        false_code = ''
        if node.false_block:
            skip_false = 'Skip({});\n'
            if type(node.false_block) == If:
                false_code += self.visit(node.false_block, scope)
            else:
                for line in node.false_block.children:
                    false_code += self.visit(line, scope) + ';\n'
        skip_code = skip_code.format(cond, true_code.count(';\n') + bool(node.false_block))
        if false_code:
            skip_false = skip_false.format(false_code.count(';\n'))
        code = skip_code + true_code + skip_false + false_code
        return code

    def visitWhile(self, node, scope):
        """While loop is simulated by looping the action list while a condition is met.
        Support for while loops is limited."""
        skip_cond = 'Skip If(Not({}), {});\n'
        cond = self.visit(node.cond, scope)
        block = ';\n'.join(self.visit_children(node.body, scope)) + ';\n'
        loop_cond = ';\n{};\nLoop If({})'.format(self.min_wait, cond)
        num_skips = block.count(';\n') + 2 # Include wait/loop skip
        skip_cond = skip_cond.format(self.visit(node.cond, scope), num_skips)
        code = skip_cond + block + loop_cond
        return code

    def visitFor(self, node, scope):
        """For loops store a pointer to each element in an iterable and loop the action list until the pointer
        is at the end of the iterable (length of iterable). If the length is a known value (e.g. user-created array),
        then loop unrolling is possible to reduce time and number of actions."""
        code = ''
        pointer = node.pointer
        iterable = node.iterable
        if type(iterable) == Var:
            lines = []
            array = scope.get(iterable.name).value
            try:
                assert type(array) == Array
            except AssertionError:
                raise Errors.SyntaxError('{} is not iterable'.format(iterable.name), pos=iterable._pos)
            for elem in array.elements:
                scope = Scope(name='for', parent=scope)
                var = Var(name=pointer.name, type_=Var.INTERNAL, value=elem)
                scope.assign(pointer.name, var)
                lines.append(';\n'.join(self.visit_children(node.body, scope)))
            code += ';\n'.join(lines)
        elif type(iterable) == Call:
            func_name = self.base_node(iterable).name
            func = scope.get(func_name).value
            try:
                self.scope = scope
                array = func(*([self] + iterable.args))
                assert type(array) == Array
                lines = []
                for elem in array.elements:
                    for_scope = Scope(name='for', parent=scope)
                    var = Var(name=pointer.name, type_=Var.INTERNAL, value=elem)
                    for_scope.assign(pointer.name, var)
                    result = self.visit_children(node.body, for_scope)
                    if result:
                        lines.append(';\n'.join(result))
                code += ';\n'.join(lines)
            except AssertionError:
                raise Errors.SyntaxError('Function call did not return an array', pos=iterable._pos)
            except TypeError as ex:
                self.logger.debug('For loop TypeError:', ex)
        else:
            for_scope = Scope(name='for', parent=scope)
            value = Number(value='0')
            index = next(self.global_index)
            pointer_var = GlobalVar(letter='A', index=index)
            var = Var(name=pointer.name, type_=Var.GLOBAL, value=value, data=pointer_var)
            for_scope.assign(pointer.name, var)
            reset_pointer = 'Set Global Variable At Index(A, {}, 0);\n'.format(index)
            code += reset_pointer
            skip_code = '//FOR STARTSkip If(Compare(Count Of({}), ==, {}), {})'.format(self.visit(iterable, for_scope), self.visit(pointer, for_scope), '{}')
            block = ';\n'.join(self.visit_children(node.body, for_scope) + [
                'Modify Global Variable At Index(A, {}, Add, 1)'.format(index),
                self.min_wait,
                'Loop',
                reset_pointer])
            code += skip_code.format(block.count(';\n')) + ';\n' + block
            self.curblock.insert(0, self.tabs + '//SKIP TOSkip If(Compare(Value In Array(Global Variable(A), {}), !=, 0), {})'.format(index, '{}'))
        return code

    def visitBinaryOp(self, node, scope):
        """A binary expression takes two operands and one operator (addition, expontentiation, etc)."""
        if type(node.left) == Number and type(node.right) == Number:
            func = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
                '^': lambda a, b: a ** b,
                '%': lambda a, b: a % b
            }.get(node.op, None)
            if func:
                try:
                    result = func(node.left, node.right)
                    return self.visit(Number(value='{}'.format(result)), scope)
                except ZeroDivisionError:
                    return self.visit(Number(value='0'), scope)
        code = {
            '+': 'Add',
            '-': 'Subtract',
            '*': 'Multiply',
            '/': 'Divide',
            '^': 'Raise To Power',
            '%': 'Modulo',
            'or': 'Or',
            'and': 'And'
        }.get(node.op)
        try:
            code += '(' + self.visit(node.left, scope) + ', ' + self.visit(node.right, scope) + ')'
        except RecursionError:
            self.logger.debug('Recursion in BinaryOp from: {}'.format(node))
        return code

    def visitUnaryOp(self, node, scope):
        """A unary expression takes a single operand and operator (e.g. negation)."""
        if node.op == '-':
            code = '-' + self.visit(node.right, scope)
        elif node.op == '+':
            code = 'Abs(' + self.visit(node.right, scope) + ')'
        elif node.op == 'not':
            code = 'Not(' + self.visit(node.right, scope) + ')'
        return code

    def visitVar(self, node, scope):
        """Internal variable object detailing its type, value, data (used for player/global variables), and player (for player variables)."""
        var = scope.get(node.name)
        if not var:
            raise Errors.NameError('\'{}\' is undefined'.format(node.name), pos=node._pos)
        elif node.type == Var.STRING:
            var.type = Var.STRING
        code = ''
        if var.type == Var.GLOBAL:
            if var.data.index is not None:
                code += 'Value In Array(Global Variable({}), {})'.format(var.data.letter, var.data.index)
            else:
                code += 'Global Variable({})'.format(var.data.letter)
        elif var.type == Var.PLAYER:
            if node.player is not None:
                var.data.player = node.player
            player = self.visit(var.data.player, scope)
            if var.data.index is not None:
                code += 'Value In Array(Player Variable({}, {}), {})'.format(player, var.data.letter, var.data.index)
            else:
                code += 'Player Variable({}, {})'.format(player, var.data.letter)
        elif var.type == Var.CONST:
            code += self.visit(var.value, scope)
        elif var.type == Var.INTERNAL:
            code += self.visit(var.value, scope)
        elif var.type == Var.STRING:
            code += var.value.value
        else:
            raise Errors.NotImplementedError('Unexpected Var type {}'.format(var._type), pos=node._pos)
        return code

    def visitString(self, node, scope):
        """A string has three children which can be strings, but each one defaults to null."""
        code = 'String("' + node.value.title() + '", '
        children = ', '.join(self.visit(child, scope) for child in node.children)
        code += children + ')'
        return code

    def visitNumber(self, node, scope):
        """A numeric constant is represented by the value itself in the workshop."""
        return node.value

    def visitTime(self, node, scope):
        """Shorthand for writing time values instead of doing integer arithmetic."""
        time = node.value
        if time.endswith('ms'):
            time = float(time.rstrip('ms')) / 1000
        elif time.endswith('s'):
            time = float(time.rstrip('s'))
        elif time.endswith('min'):
            time = float(time.rstrip('min')) * 60
        return str(round(time, 3))

    def visitVector(self, node, scope):
        """Convenient way to represent vector values."""
        code = 'Vector('
        components = ', '.join(self.visit(x, scope) for x in node.children)
        code += components + ')'
        return code

    def visitArray(self, node, scope):
        """Arrays in OWScript can take any value, including strings and constants such as heroes."""
        if not node.elements:
            return 'Empty Array'
        else:
            elements = []
            for elem in node.elements:
                if type(elem) in (String, Constant):
                    elements.append(Constant(name='Null'))
                else:
                    elements.append(elem)
            num_elems = len(elements)
            if num_elems == 0:
                return 'Empty Array'
            code = 'Append To Array(' * num_elems
            code += 'Empty Array, ' + '), '.join(self.visit(elem, scope) for elem in elements) + ')'
        return code

    def visitItem(self, node, scope):
        """An item is accessing an element of an array."""
        # Try to access an array element by interpreting the number?
        if type(node.index) == Number and type(node.parent) == Var:
            var = scope.get(node.parent.name)
            if not var:
                raise Errors.NameError('\'{}\' is undefined'.format(node.parent.name), pos=node.parent._pos)
            try:
                index = int(node.index.value)
                array = var.value
                assert type(array) == Array
                if not 0 <= index < len(array):
                    item = Number(value='0')
                else:
                    item = var.value[index]
                return self.visit(item, scope)
            except AssertionError:
                raise Errors.SyntaxError('Cannot get item from non-array type {}'.format(type(var.value)), pos=node.parent._pos)
        else:
            try:
                index = int(scope.get(node.index.name).value)
                item = scope.get(node.parent.name).value[index]
                return self.visit(item, scope)
            except (ValueError, TypeError, AttributeError):
                array = self.visit(node.parent, scope)
                index = self.visit(node.index, scope)
                return 'Value In Array({}, {})'.format(array, index)

    def visitAttribute(self, node, scope):
        """Attributes are properties accessed using the dot operator."""
        attr = node.name.lower()
        try:
            attribute = getattr(node.parent, attr)
        except AttributeError:
            raise Errors.AttributeError('\'{}\' has no attribute \'{}\''.format(node.parent.name.title(), attr), pos=node._pos)
        code = attribute.format(self.visit(node.parent, scope))
        return code

    def visitCall(self, node, scope):
        """Calls are either made to built-in functions or user-defined functions. Their arguments must be evaluated beforehand."""
        parent = node.parent
        base_node = self.base_node(node)
        var = scope.get(base_node.name)
        lines = []
        # Handle method (attribute access followed by a call)
        if type(parent) == Attribute:
            if var is not None:
                method = getattr(var.value, parent.name)
            else:
                method = getattr(base_node, parent.name)
            try:
                self.scope = scope
                result = method(self, *node.args)
            except TypeError as ex:
                print('Invalid method arguments:', ex)
                raise Errors.InvalidParameter("'{}' method received invalid arguments".format(parent.name), pos=parent._pos)
            if result:
                lines.append(self.visit(result, scope))
            return ';\n'.join(lines)
        elif type(parent) is not Var:
            self.logger.debug('Called by parent of type {}', type(parent))
        if not var:
            raise Errors.NameError('Undefined function \'{}\''.format(func_name), pos=parent._pos)
        func = var.value
        # Handle user-defined and built-in functions
        if var.type != Var.BUILTIN:
            if not func.arity >= len(node.args) >= func.min_arity:
                raise Errors.InvalidParameter('\'{}\' expected {} or more arguments, received {}'.format(func.name, func.min_arity, len(node.args)), pos=node._pos)
            # Extend default args
            default_args = [p.default for p in func.params[len(node.args):]]
            # Resolve variables in call
            args = [self.resolve_name(arg, scope) for arg in node.args + default_args]
            scope = Scope(name=func.name, parent=scope)
            for param, arg in zip(func.params, args):
                var = Var(name=param.name, type_=Var.INTERNAL, value=arg)
                scope.assign(param.name, var)
            for child in func.children:
                try:
                    lines.append(self.visit(child, scope=scope))
                except Errors.ReturnError as ex:
                    lines.append(self.visit(ex.value, scope=scope))
        elif var.type == Var.BUILTIN:
            try:
                self.scope = scope
                result = func(*([self] + node.args))
                lines.append(self.visit(result, scope))
            except TypeError as ex:
                self.logger.debug('TypeError in built-in function {}:'.format(var.name), ex)
        return ';\n'.join(lines)

    def visitReturn(self, node, scope):
        """Return statements break out of functions early."""
        if node.value is not None:
            raise Errors.ReturnError(value=node.value)
        return ''

    def visit(self, node, scope):
        """Finds the relevant transpiler method for the current node."""
        method_name = 'visit' + type(node).__name__
        visitor = getattr(self, method_name)
        return visitor(node, scope)

    def visit_children(self, node, scope):
        """Convenience function to visit all children of a node."""
        lines = []
        for child in node.children:
            lines.append(self.visit(child, scope))
        return lines

    def run(self):
        """Evaluates the parse tree from the parser into workshop code."""
        global_scope = Scope(name='global')
        for func_name, func in Builtin.__annotations__.items():
            var = Var(name=func_name, type_=Var.BUILTIN, value=func)
            global_scope.assign(func_name, var)
        code = self.visit(self.tree, scope=global_scope)
        return code
