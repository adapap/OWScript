class Transpiler:
    """Transpiles an AST into Overwatch Workshop source code."""
    def __init__(self, tree):
        self.tree = tree
        self.code = ''
        self.indent_level = 0

    @property
    def tabs(self):
        return '\t' * self.indent_level

    def run(self):
        self.visit(self.tree)
        print(self.code)

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Ruleset(self, node):
        for map_ in node.maps:
            self.visit(map_)
        for rule in node.rules:
            self.visit(rule)

    def visit_Map(self, node):
        print(node)

    def visit_Rule(self, node):
        self.code += f'rule({node.name})\n{self.tabs}' + '{\n\t'
        self.indent_level += 1
        self.visit(node.event)
        self.indent_level -= 1
        self.code += '\n}'

    def visit_Event(self, node):
        self.code += f'event\n{self.tabs}' + '{\n'
        self.indent_level += 1
        self.visit(node.block)
        self.indent_level -= 1
        self.code += f'\n{self.tabs}' + '}'

    def visit_Block(self, node):
        self.code += self.tabs + str(node.statements)