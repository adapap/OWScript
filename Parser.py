import sys
import typing

import Definitions
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

    def ahead(self, n=1):
        """Checks n tokens ahead."""
        return self.tokens[self.index + n].type

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
        """statement: (event? conditions? actions?|expr?)"""
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
        if self.cur_token.type == 'ASSIGN':
            self.assign()
        node = self.compare()
        return node

    def compare(self):
        """compare: primary (COMPARE primary)*"""
        node = self.primary()
        while self.cur_token.type == 'COMPARE':
            op = self.cur_token
            self.eat('COMPARE')
            node = Compare(left=node, op=op, right=self.block())
        return node

    def primary(self):
        """primary: NAME
                  | NUMBER
                  | BOOLEAN
                  | ARRAY
                  | VALUE
                  | CONDITION
        """
        token = self.cur_token.value
        if self.cur_token.type == 'VALUE':
            node = Value(value=token)
            defs = self.cur_token.definitions
            self.eat('VALUE')
            # First Param
            if defs and defs.__origin__ is typing.Union:
                if self.cur_token.type == 'NEWLINE':
                    self.eat('NEWLINE')
                self.eat('INDENT')
                if self.cur_token.type == 'NAME':
                    self.eat('NAME')
                    self.eat('COLON')
                for value in defs.__args__:
                    if value.__name__.upper() == self.cur_token.type:
                        param = Value(value=self.cur_token.value)
                        self.eat(self.cur_token.type)
                        break
                node.params.append(param)
                if self.cur_token.type == 'NEWLINE':
                    self.eat('NEWLINE')
                self.eat('DEDENT')
            elif defs and defs.__origin__ is tuple: #please send help
                for arg in defs.__args__:
                    name = arg.__name__.upper()
                    if self.cur_token.type == 'NEWLINE':
                        self.eat('NEWLINE')
                    if self.cur_token.type == 'INDENT':
                        self.eat('INDENT')
                    if self.cur_token.type == 'NAME':
                        self.eat('NAME')
                        self.eat('COLON')
                    param = self.primary()
                    node.params.append(param)
                    if self.cur_token.type == 'DEDENT':
                        self.eat('DEDENT')
            else:
                pass
                # print(self.tokens[:self.index])
                # print(defs.__origin__)
                # print('not typing union', self.cur_token, defs)
                # sys.exit(0)
                #param = self.block()
                #node.params.append(param)
        elif self.cur_token.type == 'ARRAY':
            self.eat('ARRAY')
            node = Array(token, block=self.block())
        elif self.cur_token.type == 'CONDITION':
            self.eat('CONDITION')
            node = Condition(cond=token, value=self.block())
        elif self.cur_token.type in Definitions.type_names:
            node = Name(value=token)
            defs = self.cur_token.definitions
            self.eat(self.cur_token.type)
            self.eat('NEWLINE')
            if defs and hasattr(defs, '__args__'):
                node = Group(value=token)
                for d in defs.__args__:
                    if self.cur_token.type == 'NAME':
                        # Eat comment
                        self.eat('NAME')
                        self.eat('COLON')
                    child_node = self.expr()
                    node.children.append(child_node)
        elif self.cur_token.type == 'NAME':
            if self.peek == 'COLON':
                self.eat('NAME')
                self.eat('COLON')
                node = self.expr()
            elif self.peek == 'ASSIGN': # Variable Assign
                name = Variable(value=token)
                self.eat('NAME')
                op = self.cur_token.value
                self.eat('ASSIGN')
                value = self.expr()
                node = Assign(left=name, op=op, right=value)
            else:
                node = Name(token)
                self.eat('NAME')
        elif self.cur_token.type == 'INTEGER':
            node = Integer(token)
            self.eat('INTEGER')
        # elif self.cur_token.type == 'BOOLEAN':
        #     node = Boolean(token)
        #     self.eat('BOOLEAN')
        else:
            print('No token found:', self.cur_token)
        return node

    def parse(self):
        """Parses the tokens into an AST."""
        return self.ruleset()