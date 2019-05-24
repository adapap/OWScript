from Nodes import *

class Parser:
    """Generates an abstract syntax tree (AST) of the ruleset."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.num_tokens = len(tokens) - 1
        self.index = 0
        self.last_expr = None
        self.cur_token = self.get_token()
        self.indents = [0]

    @property
    def peek(self):
        """Checks to see the next token."""
        return self.tokens[self.index + 1].type

    def get_token(self):
        """Retrieves the current token."""
        return self.tokens[self.index]

    def eat(self, type_):
        """Consumes the token and advances to the next token."""
        if self.cur_token.type == type_:
            self.index += 1
            self.cur_token = self.get_token()
            while self.cur_token.type == 'WHITESPACE':
                self.index += 1
                self.cur_token = self.get_token()
        else:
            raise ValueError(f'Expected token {type_}, received {self.cur_token.type}')

    def ruleset(self):
        """ruleset: maps* rule*"""
        maps = []
        while self.cur_token.type == 'NAME':
            name = self.cur_token.value
            self.eat('NAME')
            self.eat('MAP')
            value = self.cur_token.value
            self.eat('NAME')
            self.eat('NEWLINE')
            node = Map(name=self.cur_token.value, value=value)
        ruleset = []
        while self.cur_token.type != 'EOF':
            rule = self.rule()
            ruleset.append(rule)
        node = Ruleset(maps=maps, rules=ruleset)
        return node

    def rule(self):
        """rule: 'Rule' STRING block"""
        self.eat('KEYWORD')
        rule_name = self.cur_token.value
        self.eat('STRING')
        rule_block = self.block()
        node = Rule(name=rule_name)
        for statement in rule_block.statements:
            stmt_type = statement.__class__.__name__
            if stmt_type == 'Event':
                node.event = statement
            elif stmt_type == 'Conditions':
                node.conditions = statement
            elif stmt_type == 'Actions':
                node.actions = statement
        return node

    def block(self):
        """block: NEWLINE? INDENT statements* DEDENT"""
        if self.cur_token.type == 'NEWLINE':
            self.eat('NEWLINE')
        self.eat('INDENT')
        statements = []
        while self.cur_token.type != 'DEDENT':
            statements.append(self.statement())
            if self.cur_token.type == 'NEWLINE':
                self.eat('NEWLINE')
        node = Block(statements)
        self.eat('DEDENT')
        return node

    def statement(self):
        """statement: event? conditions? actions?"""
        if self.cur_token.type == 'KEYWORD':
            keyword = self.cur_token.value
            self.eat('KEYWORD')
            block = self.block()
            if keyword == 'Event':
                node = Event(block)
            elif keyword == 'Conditions':
                node = Conditions(block)
            elif keyword == 'Actions':
                node = Actions(block)
        else:
            node = self.expr()
        return node

    def expr(self):
        """expr: compare"""
        node = self.compare()
        return node

    def compare(self):
        """compare: primary (COMPARE primary)*"""
        node = self.primary()
        while self.cur_token.type == 'COMPARE':
            op = self.cur_token
            self.eat('COMPARE')
            node = Compare(left=node, op=op, right=self.compare())
        return node

    def primary(self):
        """primary: NAME
                  | NUMBER
                  | BOOLEAN
                  | ARRAY
        """
        token = self.cur_token.value
        if self.cur_token.type == 'NAME':
            if self.peek == 'COLON':
                self.eat('NAME')
                self.eat('COLON')
                node = self.expr()
            else:
                node = Name(token)
                self.eat('NAME')
        elif self.cur_token.type == 'NUMBER':
            node = Number(token)
            self.eat('NUMBER')
        elif self.cur_token.type == 'BOOLEAN':
            node = Boolean(token)
            self.eat('BOOLEAN')
        elif self.cur_token.type == 'CONDITION':
            cond = self.cur_token.value
            self.eat('CONDITION')
            comp_op = self.cur_token.value
            self.eat('COMPARE')
            value = self.expr()
            node = Condition(cond=cond, comp_op=comp_op, value=value, block=self.block())
        elif self.cur_token.type == 'ARRAY':
            if token == 'All Players':
                self.eat('ARRAY')
                node = Array(token, block=self.block())
        else:
            print('No token found:', self.cur_token)
        return node

    def parse(self):
        """Parses the tokens into an AST."""
        return self.ruleset()