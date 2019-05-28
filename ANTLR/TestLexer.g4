lexer grammar Test;

STRING : '"' ~[\\\r\n\f"]* '"';
INTEGER : [0-9]+;
NAME : [_a-zA-Z][_a-zA-Z0-9]*;

@lexer::members {
    # A queue where extra tokens are pushed on (see the NEWLINE lexer rule).
    self.tokens = []

    # The stack that keeps track of the indentation level.
    self.indents = []

    # The amount of opened braces, brackets and parenthesis.
    self.opened = 0

    # The most recently produced token.
    self.last_token = None

def emitToken(self, t):
    super().emitToken(t)
    self.tokens.append(t)

def nextToken(self):
    if self._input.LA(1) == Token.EOF and len(self.indents) > 0:
        while len(self.tokens) > 0 and self.tokens[-1].type == Token.EOF:
            del self.tokens[-1]

        # First emit an extra line break that serves as the end of the statement.
        self.emitToken(self.common_token(TestLexer.NEWLINE, '\n'));

        # Now emit as much DEDENT tokens as needed.
        while len(self.indents) != 0:
            self.emitToken(self.create_dedent())
            del self.indents[-1]

        # Put the EOF back on the token stream.
        self.emitToken(self.common_token(Token.EOF, '<EOF>'));

    next = super().nextToken();

    if next.channel == Token.DEFAULT_CHANNEL:
        # Keep track of the last token on the default channel.
        self.last_token = next

    if len(self.tokens) == 0:
        return next
    else:
        t = self.tokens[0]
        del self.tokens[0]
        return t

def create_dedent(self):
    from TestParser import TestParser
    dedent = self.common_token(TestParser.DEDENT, '')
    dedent.line = self.last_token.line
    return dedent

def common_token(self, _type, text, alias=None):
    from antlr4.Token import CommonToken
    stop = self.getCharIndex() - 1
    if len(self.text) == 0:
        start = stop
    else:
        start = stop - len(self.text) + 1
    token = CommonToken(self._tokenFactorySourcePair, _type, Lexer.DEFAULT_TOKEN_CHANNEL, start, stop)
    token._text = ''
    return token

def getIndentationCount(self, spaces):
    count = 0
    for ch in spaces:
        if ch == '\t':
            count += 8 - (count % 8)
        else:
            count += 1
    return count

def atStartOfInput(self):
    return self._interp.column == 0 and self._interp.line == 1
}

NEWLINE : ( {self.atStartOfInput()}? SPACES
        | ( '\r'? '\n' | '\r' | '\f' ) SPACES?
        )
{
    import re
    from TestParser import TestParser
    new_line = re.sub(r"[^\r\n\f]+", "", self._interp.getText(self._input)) #.replaceAll("[^\r\n\f]+", "")
    spaces = re.sub(r"[\r\n\f]+", "", self._interp.getText(self._input)) #.replaceAll("[\r\n\f]+", "")
    next = self._input.LA(1)

    if self.opened > 0 or next == '\r' or next == '\n' or next == '\f':
        self.skip()
    else:
        self.emitToken(self.common_token(self.NEWLINE, new_line))

        indent = self.getIndentationCount(spaces)
        if len(self.indents) == 0:
            previous = 0
        else:
            previous = self.indents[-1]

        if indent == previous:
            self.skip()
        elif indent > previous:
            self.indents.append(indent)
            self.emitToken(self.common_token(TestParser.INDENT, spaces))
        else:
            while len(self.indents) > 0 and self.indents[-1] > indent:
                self.emitToken(self.create_dedent())
                del self.indents[-1]
};
SKIP_ : (SPACES | COMMENT) -> skip;
UNKNOWN_CHAR : .;

fragment SPACES : [ \t]+;
fragment COMMENT : '/*' .*? '*/';