class Transpiler:
    """Transpiles an AST into Overwatch Workshop source code."""
    def __init__(self, tree):
        self.tree = tree
        self.code = ''
        self.indent_level = 0
        self.maps = {}

    @property
    def tabs(self):
        return '\t' * self.indent_level

    def run(self):
        self.visit(self.tree, inline=False)
        #print(self.code)
        return self.code

    def visit(self, node, inline):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, inline)

    def generic_visit(self, node, inline):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Ruleset(self, node, inline):
        for map_ in node.maps:
            self.visit(map_, inline)
        for rule in node.rules:
            self.visit(rule, inline)

    def visit_Map(self, node, inline):
        self.maps[node.name] = node.value

    def visit_Rule(self, node, inline):
        self.code += f'rule({node.name})\n{self.tabs}' + '{\n'
        self.indent_level += 1
        if node.event:
            self.visit(node.event, inline)
            if node.conditions or node.actions:
                self.code += '\n\n'
        if node.conditions:
            self.visit(node.conditions, inline)
            if node.actions:
                self.code += '\n\n'
        if node.actions:
            self.visit(node.actions, inline)
        self.indent_level -= 1
        self.code += '\n}'

    def visit_Event(self, node, inline):
        self.code += f'{self.tabs}event\n{self.tabs}' + '{\n'
        self.visit(node.block, inline)
        self.code += self.tabs + '}'

    def visit_Conditions(self, node, inline):
        self.code += f'{self.tabs}conditions\n{self.tabs}' + '{\n'
        self.visit(node.block, inline)
        self.code += '\n' + self.tabs + '}'

    def visit_Actions(self, node, inline):
        self.code += f'{self.tabs}actions\n{self.tabs}' + '{\n'
        self.visit(node.block, inline)
        self.code += self.tabs + '}'

    def visit_Condition(self, node, inline):
        self.code += node.cond + '('
        self.visit(node.value, inline)
        self.code += ')'

    def visit_Block(self, node, inline):
        self.indent_level += 1
        for statement in node.statements:
            self.visit(statement, inline)
        self.indent_level -= 1

    def visit_Compare(self, node, inline):
        self.visit(node.left, inline)
        self.code += f' {node.op.value} '
        self.visit(node.right, inline=True)

    def visit_Variable(self, node, inline):
        value = node.value
        while value in self.maps:
            value = self.maps.get(value)
        self.code += value

    def visit_Integer(self, node, inline):
        self.code += node.value

    def visit_Assign(self, node, inline):
        if node.op == '=':
            self.code += self.tabs + 'Set Global Variable('
            self.visit(node.left, inline)
            self.code += ', '
            self.visit(node.right, inline)
            self.code += ')\n'

    def visit_Name(self, node, inline):
        if not inline:
            self.code += self.tabs + node.value
        else:
            self.code += node.value

    def visit_Value(self, node, inline):
        if not inline:
            self.code += self.tabs + node.value
        else:
            self.code += node.value
        if node.params:
            self.code += '('
            for param in node.params:
                self.visit(param, inline=True)
                if param != node.params[-1]:
                    self.code += ', '
            self.code += ')'

    def visit_Group(self, node, inline):
        self.code += self.tabs + node.value
        for child in node.children:
            self.code += '\n'
            self.visit(child, inline)
        self.code += '\n'

    def visit_Array(self, node, inline):
        self.code += node.value + '('
        if node.value == 'All Players':
            self.visit(node.block, inline)
        self.code += ')'