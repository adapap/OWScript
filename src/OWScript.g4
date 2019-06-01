grammar OWScript;

/* Parser Rules */
tokens { INDENT, DEDENT, ACTION, VALUE, CONST, GLOBAL_VAR, PLAYER_VAR }

@lexer::members {
    # Workshop Ruleset
    self.workshop_rules = dict([
        ('ABORT', 'ACTION'),
        ('ABORT IF', 'ACTION'),
        ('ABORT IF CONDITION IS FALSE', 'ACTION'),
        ('ABORT IF CONDITION IS TRUE', 'ACTION'),
        ('ALLOW BUTTON', 'ACTION'),
        ('APPLY IMPULSE', 'ACTION'),
        ('BIG MESSAGE', 'ACTION'),
        ('CHASE GLOBAL VARIABLE AT RATE', 'ACTION'),
        ('CHASE GLOBAL VARIABLE OVER TIME', 'ACTION'),
        ('CHASE PLAYER VARIABLE AT RATE', 'ACTION'),
        ('CHASE PLAYER VARIABLE OVER TIME', 'ACTION'),
        ('CLEAR STATUS', 'ACTION'),
        ('COMMUNICATE', 'ACTION'),
        ('CREATE EFFECT', 'ACTION'),
        ('CREATE HUD TEXT', 'ACTION'),
        ('CREATE ICON', 'ACTION'),
        ('CREATE IN-WORLD TEXT', 'ACTION'),
        ('DAMAGE', 'ACTION'),
        ('DECLARE MATCH DRAW', 'ACTION'),
        ('DECLARE PLAYER VICTORY', 'ACTION'),
        ('DECLARE ROUND VICTORY', 'ACTION'),
        ('DECLARE TEAM VICTORY', 'ACTION'),
        ('DESTROY ALL EFFECTS', 'ACTION'),
        ('DESTROY ALL HUD TEXT', 'ACTION'),
        ('DESTROY ALL ICONS', 'ACTION'),
        ('DESTROY ALL IN-WORLD TEXT', 'ACTION'),
        ('DESTROY EFFECT', 'ACTION'),
        ('DESTROY HUD TEXT', 'ACTION'),
        ('DESTROY ICON', 'ACTION'),
        ('DESTROY IN-WORLD TEXT', 'ACTION'),
        ('DISABLE BUILT-IN GAME MODE ANNOUNCER', 'ACTION'),
        ('DISABLE BUILT-IN GAME MODE COMPLETION', 'ACTION'),
        ('DISABLE BUILT-IN GAME MODE MUSIC', 'ACTION'),
        ('DISABLE BUILT-IN GAME MODE RESPAWNING', 'ACTION'),
        ('DISABLE BUILT-IN GAME MODE SCORING', 'ACTION'),
        ('DISABLE DEATH SPECTATE ALL PLAYERS', 'ACTION'),
        ('DISABLE DEATH SPECTATE TARGET HUD', 'ACTION'),
        ('DISALLOW BUTTON', 'ACTION'),
        ('ENABLE BUILT-IN GAME MODE ANNOUNCER', 'ACTION'),
        ('ENABLE BUILT-IN GAME MODE COMPLETION', 'ACTION'),
        ('ENABLE BUILT-IN GAME MODE MUSIC', 'ACTION'),
        ('ENABLE BUILT-IN GAME MODE RESPAWNING', 'ACTION'),
        ('ENABLE BUILT-IN GAME MODE SCORING', 'ACTION'),
        ('ENABLE DEATH SPECTATE ALL PLAYERS', 'ACTION'),
        ('ENABLE DEATH SPECTATE TARGET HUD', 'ACTION'),
        ('GO TO ASSEMBLE HEROES', 'ACTION'),
        ('HEAL', 'ACTION'),
        ('KILL', 'ACTION'),
        ('LOOP', 'ACTION'),
        ('LOOP IF', 'ACTION'),
        ('LOOP IF CONDITION IS FALSE', 'ACTION'),
        ('LOOP IF CONDITION IS TRUE', 'ACTION'),
        ('MODIFY GLOBAL VARIABLE', 'ACTION'),
        ('MODIFY PLAYER SCORE', 'ACTION'),
        ('MODIFY PLAYER VARIABLE', 'ACTION'),
        ('MODIFY TEAM SCORE', 'ACTION'),
        ('PAUSE MATCH TIME', 'ACTION'),
        ('PLAY EFFECT', 'ACTION'),
        ('PRELOAD HERO', 'ACTION'),
        ('PRESS BUTTON', 'ACTION'),
        ('RESET PLAYER HERO AVAILABILITY', 'ACTION'),
        ('RESPAWN', 'ACTION'),
        ('RESURRECT', 'ACTION'),
        ('SET ABILITY 1 ENABLED', 'ACTION'),
        ('SET ABILITY 2 ENABLED', 'ACTION'),
        ('SET AIM SPEED', 'ACTION'),
        ('SET DAMAGE DEALT', 'ACTION'),
        ('SET DAMAGE RECEIVED', 'ACTION'),
        ('SET FACING', 'ACTION'),
        ('SET GLOBAL VARIABLE', 'ACTION'),
        ('SET GLOBAL VARIABLE AT INDEX', 'ACTION'),
        ('SET GRAVITY', 'ACTION'),
        ('SET HEALING DEALT', 'ACTION'),
        ('SET HEALING RECEIVED', 'ACTION'),
        ('SET INVISIBLE', 'ACTION'),
        ('SET MATCH TIME', 'ACTION'),
        ('SET MAX HEALTH', 'ACTION'),
        ('SET MOVE SPEED', 'ACTION'),
        ('SET OBJECTIVE DESCRIPTION', 'ACTION'),
        ('SET PLAYER ALLOWED HEROES', 'ACTION'),
        ('SET PLAYER SCORE', 'ACTION'),
        ('SET PLAYER VARIABLE', 'ACTION'),
        ('SET PLAYER VARIABLE AT INDEX', 'ACTION'),
        ('SET PRIMARY FIRE ENABLED', 'ACTION'),
        ('SET PROJECTILE GRAVITY', 'ACTION'),
        ('SET PROJECTILE SPEED', 'ACTION'),
        ('SET RESPAWN MAX TIME', 'ACTION'),
        ('SET SECONDARY FIRE ENABLED', 'ACTION'),
        ('SET SLOW MOTION', 'ACTION'),
        ('SET STATUS', 'ACTION'),
        ('SET TEAM SCORE', 'ACTION'),
        ('SET ULTIMATE ABILITY ENABLED', 'ACTION'),
        ('SET ULTIMATE CHARGE', 'ACTION'),
        ('SKIP', 'ACTION'),
        ('SKIP IF', 'ACTION'),
        ('SMALL MESSAGE', 'ACTION'),
        ('START ACCELERATING', 'ACTION'),
        ('START CAMERA', 'ACTION'),
        ('START DAMAGE MODIFICATION', 'ACTION'),
        ('START DAMAGE OVER TIME', 'ACTION'),
        ('START FACING', 'ACTION'),
        ('START FORCING PLAYER TO BE HERO', 'ACTION'),
        ('START FORCING SPAWN ROOM', 'ACTION'),
        ('START FORCING THROTTLE', 'ACTION'),
        ('START HEAL OVER TIME', 'ACTION'),
        ('START HOLDING BUTTON', 'ACTION'),
        ('STOP ACCELERATING', 'ACTION'),
        ('STOP ALL DAMAGE MODIFICATIONS', 'ACTION'),
        ('STOP ALL DAMAGE OVER TIME', 'ACTION'),
        ('STOP ALL HEAL OVER TIME', 'ACTION'),
        ('STOP CAMERA', 'ACTION'),
        ('STOP CHASING GLOBAL VARIABLE', 'ACTION'),
        ('STOP CHASING PLAYER VARIABLE', 'ACTION'),
        ('STOP DAMAGE MODIFICATION', 'ACTION'),
        ('STOP DAMAGE OVER TIME', 'ACTION'),
        ('STOP FACING', 'ACTION'),
        ('STOP FORCING PLAYER TO BE HERO', 'ACTION'),
        ('STOP FORCING SPAWN ROOM', 'ACTION'),
        ('STOP FORCING THROTTLE', 'ACTION'),
        ('STOP HEAL OVER TIME', 'ACTION'),
        ('STOP HOLDING BUTTON', 'ACTION'),
        ('TELEPORT', 'ACTION'),
        ('UNPAUSE MATCH TIME', 'ACTION'),
        ('WAIT', 'ACTION'),
        ('ALL HEROES', 'CONST'),
        ('ATTACKER', 'CONST'),
        ('BACKWARD', 'CONST'),
        ('CONTROL MODE SCORING TEAM', 'CONST'),
        ('CURRENT ARRAY ELEMENT', 'CONST'),
        ('DOWN', 'CONST'),
        ('EMPTY ARRAY', 'CONST'),
        ('EVENT PLAYER', 'CONST'),
        ('EVENT WAS CRITICAL HIT', 'CONST'),
        ('FALSE', 'CONST'),
        ('FORWARD', 'CONST'),
        ('IS ASSEMBLING HEROES', 'CONST'),
        ('IS BETWEEN ROUNDS', 'CONST'),
        ('IS CONTROL MODE POINT LOCKED', 'CONST'),
        ('IS CTF MODE IN SUDDEN DEATH', 'CONST'),
        ('IS GAME IN PROGRESS', 'CONST'),
        ('IS IN SETUP', 'CONST'),
        ('IS MATCH COMPLETE', 'CONST'),
        ('IS WAITING FOR PLAYERS', 'CONST'),
        ('LAST CREATED ENTITY', 'CONST'),
        ('LEFT', 'CONST'),
        ('NULL', 'CONST'),
        ('PAYLOAD POSITION', 'CONST'),
        ('RIGHT', 'CONST'),
        ('TRUE', 'CONST'),
        ('UP', 'CONST'),
        ('VICTIM', 'CONST'),
        ('ONGOING - EACH PLAYER', 'NAME'),
        ('ONGOING - GLOBAL', 'NAME'),
        ('PLAYER DEALT DAMAGE', 'NAME'),
        ('PLAYER DEALT FINAL BLOW', 'NAME'),
        ('PLAYER DIED', 'NAME'),
        ('PLAYER EARNED ELIMINATION', 'NAME'),
        ('PLAYER TOOK DAMAGE', 'NAME'),
        ('ABSOLUTE VALUE', 'VALUE'),
        ('ADD', 'VALUE'),
        ('ALL DEAD PLAYERS', 'VALUE'),
        ('ALL LIVING PLAYERS', 'VALUE'),
        ('ALL PLAYERS', 'VALUE'),
        ('ALL PLAYERS NOT ON OBJECTIVE', 'VALUE'),
        ('ALL PLAYERS ON OBJECTIVE', 'VALUE'),
        ('ALLOWED HEROES', 'VALUE'),
        ('ALTITUDE OF', 'VALUE'),
        ('ANGLE DIFFERENCE', 'VALUE'),
        ('APPEND TO ARRAY', 'VALUE'),
        ('ARRAY SLICE', 'VALUE'),
        ('CLOSEST PLAYER TO', 'VALUE'),
        ('COMPARE', 'VALUE'),
        ('CONTROL MODE SCORING PERCENTAGE', 'VALUE'),
        ('COSINE FROM DEGREES', 'VALUE'),
        ('COSINE FROM RADIANS', 'VALUE'),
        ('COUNT OF', 'VALUE'),
        ('CROSS PRODUCT', 'VALUE'),
        ('DIRECTION FROM ANGLES', 'VALUE'),
        ('DIRECTION TOWARDS', 'VALUE'),
        ('DISTANCE BETWEEN', 'VALUE'),
        ('DIVIDE', 'VALUE'),
        ('DOT PRODUCT', 'VALUE'),
        ('ENTITY EXISTS', 'VALUE'),
        ('EVENT DAMAGE', 'VALUE'),
        ('EYE POSITION', 'VALUE'),
        ('FACING DIRECTION OF', 'VALUE'),
        ('FARTHEST PLAYER FROM', 'VALUE'),
        ('FILTERED ARRAY', 'VALUE'),
        ('FIRST OF', 'VALUE'),
        ('FLAG POSITION', 'VALUE'),
        ('GLOBAL VARIABLE', 'VALUE'),
        ('HAS SPAWNED', 'VALUE'),
        ('HAS STATUS', 'VALUE'),
        ('HEALTH', 'VALUE'),
        ('HEALTH PERCENT', 'VALUE'),
        ('HERO', 'VALUE'),
        ('HERO ICON STRING', 'VALUE'),
        ('HERO OF', 'VALUE'),
        ('HORIZONTAL ANGLE FROM DIRECTION', 'VALUE'),
        ('HORIZONTAL ANGLE TOWARDS', 'VALUE'),
        ('HORIZONTAL FACING ANGLE OF', 'VALUE'),
        ('HORIZONTAL SPEED OF', 'VALUE'),
        ('INDEX OF ARRAY VALUE', 'VALUE'),
        ('IS ALIVE', 'VALUE'),
        ('IS BUTTON HELD', 'VALUE'),
        ('IS COMMUNICATING', 'VALUE'),
        ('IS COMMUNICATING ANY', 'VALUE'),
        ('IS COMMUNICATING ANY EMOTE', 'VALUE'),
        ('IS COMMUNICATING ANY VOICE LINE', 'VALUE'),
        ('IS CROUCHING', 'VALUE'),
        ('IS DEAD', 'VALUE'),
        ('IS FIRING PRIMARY', 'VALUE'),
        ('IS FIRING SECONDARY', 'VALUE'),
        ('IS FLAG AT BASE', 'VALUE'),
        ('IS FLAG BEING CARRIED', 'VALUE'),
        ('IS HERO BEING PLAYED', 'VALUE'),
        ('IS IN AIR', 'VALUE'),
        ('IS IN LINE OF SIGHT', 'VALUE'),
        ('IS IN SPAWN ROOM', 'VALUE'),
        ('IS IN VIEW ANGLE', 'VALUE'),
        ('IS MOVING', 'VALUE'),
        ('IS OBJECTIVE COMPLETE', 'VALUE'),
        ('IS ON GROUND', 'VALUE'),
        ('IS ON OBJECTIVE', 'VALUE'),
        ('IS ON WALL', 'VALUE'),
        ('IS PORTRAIT ON FIRE', 'VALUE'),
        ('IS STANDING', 'VALUE'),
        ('IS TEAM ON DEFENSE', 'VALUE'),
        ('IS TEAM ON OFFENSE', 'VALUE'),
        ('IS TRUE FOR ALL', 'VALUE'),
        ('IS TRUE FOR ANY', 'VALUE'),
        ('IS USING ABILITY 1', 'VALUE'),
        ('IS USING ABILITY 2', 'VALUE'),
        ('IS USING ULTIMATE', 'VALUE'),
        ('LAST DAMAGE MODIFICATION ID', 'VALUE'),
        ('LAST DAMAGE OVER TIME ID', 'VALUE'),
        ('LAST HEAL OVER TIME ID', 'VALUE'),
        ('LAST OF', 'VALUE'),
        ('LAST TEXT ID', 'VALUE'),
        ('LOCAL VECTOR OF', 'VALUE'),
        ('MATCH ROUND', 'VALUE'),
        ('MATCH TIME', 'VALUE'),
        ('MAX', 'VALUE'),
        ('MAX HEALTH', 'VALUE'),
        ('MIN', 'VALUE'),
        ('MODULO', 'VALUE'),
        ('MULTIPLY', 'VALUE'),
        ('NEAREST WALKABLE POSITION', 'VALUE'),
        ('NORMALIZE', 'VALUE'),
        ('NUMBER', 'VALUE'),
        ('NUMBER OF DEAD PLAYERS', 'VALUE'),
        ('NUMBER OF DEATHS', 'VALUE'),
        ('NUMBER OF ELIMINATIONS', 'VALUE'),
        ('NUMBER OF FINAL BLOWS', 'VALUE'),
        ('NUMBER OF HEROES', 'VALUE'),
        ('NUMBER OF LIVING PLAYERS', 'VALUE'),
        ('NUMBER OF PLAYERS', 'VALUE'),
        ('NUMBER OF PLAYERS ON OBJECTIVE', 'VALUE'),
        ('OBJECTIVE INDEX', 'VALUE'),
        ('OBJECTIVE POSITION', 'VALUE'),
        ('OPPOSITE TEAM OF', 'VALUE'),
        ('PAYLOAD PROGRESS PERCENTAGE', 'VALUE'),
        ('PLAYER CARRYING FLAG', 'VALUE'),
        ('PLAYER CLOSEST TO RETICLE', 'VALUE'),
        ('PLAYER VARIABLE', 'VALUE'),
        ('PLAYERS IN SLOT', 'VALUE'),
        ('PLAYERS IN VIEW ANGLE', 'VALUE'),
        ('PLAYERS ON HERO', 'VALUE'),
        ('PLAYERS WITHIN RADIUS', 'VALUE'),
        ('POINT CAPTURE PERCENTAGE', 'VALUE'),
        ('POSITION OF', 'VALUE'),
        ('RAISE TO POWER', 'VALUE'),
        ('RANDOM INTEGER', 'VALUE'),
        ('RANDOM REAL', 'VALUE'),
        ('RANDOM VALUE IN ARRAY', 'VALUE'),
        ('RANDOMIZED ARRAY', 'VALUE'),
        ('RAY CAST HIT NORMAL', 'VALUE'),
        ('RAY CAST HIT PLAYER', 'VALUE'),
        ('RAY CAST HIT POSITION', 'VALUE'),
        ('REMOVE FROM ARRAY', 'VALUE'),
        ('ROUND TO INTEGER', 'VALUE'),
        ('SCORE OF', 'VALUE'),
        ('SINE FROM DEGREES', 'VALUE'),
        ('SINE FROM RADIANS', 'VALUE'),
        ('SLOT OF', 'VALUE'),
        ('SORTED ARRAY', 'VALUE'),
        ('SPEED OF', 'VALUE'),
        ('SPEED OF IN DIRECTION', 'VALUE'),
        ('SQUARE ROOT', 'VALUE'),
        ('STRING', 'VALUE'),
        ('SUBTRACT', 'VALUE'),
        ('TEAM', 'VALUE'),
        ('TEAM OF', 'VALUE'),
        ('TEAM SCORE', 'VALUE'),
        ('THROTTLE OF', 'VALUE'),
        ('TOTAL TIME ELAPSED', 'VALUE'),
        ('ULTIMATE CHARGE PERCENT', 'VALUE'),
        ('VALUE IN ARRAY', 'VALUE'),
        ('VECTOR', 'VALUE'),
        ('VECTOR TOWARDS', 'VALUE'),
        ('VELOCITY OF', 'VALUE'),
        ('VERTICAL ANGLE FROM DIRECTION', 'VALUE'),
        ('VERTICAL ANGLE TOWARDS', 'VALUE'),
        ('VERTICAL FACING ANGLE OF', 'VALUE'),
        ('VERTICAL SPEED OF', 'VALUE'),
        ('WORLD VECTOR OF', 'VALUE'),
        ('X COMPONENT OF', 'VALUE'),
        ('Y COMPONENT OF', 'VALUE'),
        ('Z COMPONENT OF', 'VALUE')
    ])
    self.aliases = dict([
        ('ALL TRUE', 'IS TRUE FOR ALL'),
        ('COS', 'COSINE FROM DEGREES'),
        ('COSR', 'COSINE FROM RADIANS'),
        ('ON EACH PLAYER', 'ONGOING - EACH PLAYER'),
        ('ON GLOBAL', 'ONGOING - GLOBAL'),
        ('PLAYERS IN RADIUS', 'PLAYERS WITHIN RADIUS'),
        ('ROUND', 'ROUND TO INTEGER'),
        ('SIN', 'SINE FROM DEGREES'),
        ('SINR', 'SINE FROM RADIANS')
    ])
    self.keywords = ['if', 'elif', 'else', 'pVar', 'gVar']

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
        self.emitToken(self.common_token(OWScriptLexer.NEWLINE, '\n', alias='NEWLINE'));

        # Now emit as much DEDENT tokens as needed.
        while len(self.indents) != 0:
            self.emitToken(self.create_dedent())
            del self.indents[-1]

        # Put the EOF back on the token stream.
        self.emitToken(self.common_token(Token.EOF, '<EOF>', alias='EOF'));

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
    from OWScriptParser import OWScriptParser
    dedent = self.common_token(OWScriptParser.DEDENT, '', alias='DEDENT')
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
    if alias is not None:
        pass
        token._text = alias
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
/*
Parser Grammar
*/
script : (NEWLINE | stmt)* EOF;
stmt : (funcdef | ruleset);

funcdef : '%' NAME funcbody;
funcbody : (NEWLINE INDENT (ruleset | ruledef | rulebody) DEDENT) | block;

ruleset : ruledef+;
ruledef : RULE rulename (NEWLINE INDENT rulebody* DEDENT)+;
rulename : STRING;
rulebody : RULEBLOCK ruleblock #RulebodyBlock
         | primary call NEWLINE #RCall;

ruleblock : block;
block : NEWLINE INDENT line+ DEDENT
      | line;
line : expr
     | assign
     | if_stmt
     | ANNOTATION line
     | NEWLINE;

assign : (variable item?) ASSIGN expr;
if_stmt : 'if' expr ':' block ('elif' expr ':' block)* ('else:' block)?;
expr : logic_or;
logic_or : logic_and ('or' logic_and)*;
logic_and : logic_not ('and' logic_not)*;
logic_not : ('not' logic_not) | compare;
compare : arith (('<'|'>'|'=='|'>='|'<='|'!=') arith)*;
arith : primary_expr ('^' arith)* # Pow
      | primary_expr ('*' arith)* # Mul
      | primary_expr ('/' arith)* # Div
      | primary_expr ('+' arith)* # Add
      | primary_expr ('-' arith)* # Sub
      | primary_expr ('%' arith)* # Mod
      | primary_expr #ArithPrimary;

primary_expr : primary_expr item #PItem
             | primary_expr call #PCall
             | primary #PrimaryNone;
primary : action
        | value
        | const
        | variable
        | vector
        | array
        | time
        | numeral
        | name
        | '(' expr ')';
action : ACTION after_line;
value : VALUE after_line;
const : CONST;
after_line : '(' arg_list ')'
           | block
           | NEWLINE;
arg_list : primary (',' primary)*;

item : '[' expr ']';
call : '(' arg_list? ')';

name : NAME;
time : numeral ('ms' | 's' | 'min');
numeral : num_const=FLOAT
        | num_const=INTEGER;
variable : global_var
         | player_var
         | name;
global_var : 'gVar' varname=NAME;
player_var : 'pVar' varname=NAME ('@' primary)?;
vector : '<' primary ',' primary ',' primary '>';
array : '[' arg_list? ']';


/* Lexer Rules */
ASSIGN : ('='|'+='|'-='|'*='|'/='|'^='|'%=');
STRING : '"' ~[\\\r\n\f"]* '"';
INTEGER : [0-9]+;
FLOAT : [0-9]+'.'[0-9]+;
ANNOTATION : [_a-zA-Z][_a-zA-Z0-9]* ':';
RULE : [a-zA-Z]+ {self.text.upper() == 'RULE'}?;
RULEBLOCK : [a-zA-Z]+ {self.text.upper() in ['EVENT', 'ACTIONS', 'CONDITIONS']}?;
NAME : [_a-zA-Z0-9\- ]*[a-zA-Z0-9] {self.text.split()[0] not in self.keywords}?
{from OWScriptParser import OWScriptParser
if self.text.strip().upper() in self.aliases or self.text.strip().upper() in self.workshop_rules:
    text = self.aliases.get(self.text.strip().upper(), self.text.strip().upper())
    attr = self.workshop_rules.get(text)
    self.type = getattr(OWScriptParser, attr)
    self.text = text}
    | [_a-zA-Z0-9][_a-zA-Z0-9]*;
NEWLINE : ( {self.atStartOfInput()}? SPACES
        | ( '\r'? '\n' | '\r' | '\f' ) SPACES?
        )
{
    import re
    from OWScriptParser import OWScriptParser
    new_line = re.sub(r"[^\r\n\f]+", "", self._interp.getText(self._input)) #.replaceAll("[^\r\n\f]+", "")
    spaces = re.sub(r"[\r\n\f]+", "", self._interp.getText(self._input)) #.replaceAll("[\r\n\f]+", "")
    next = self._input.LA(1)

    if self.opened > 0 or next == '\r' or next == '\n' or next == '\f':
        self.skip()
    else:
        self.emitToken(self.common_token(self.NEWLINE, new_line, 'NEWLINE'))

        indent = self.getIndentationCount(spaces)
        if len(self.indents) == 0:
            previous = 0
        else:
            previous = self.indents[-1]

        if indent == previous:
            self.skip()
        elif indent > previous:
            self.indents.append(indent)
            self.emitToken(self.common_token(OWScriptParser.INDENT, spaces, alias='INDENT'))
        else:
            while len(self.indents) > 0 and self.indents[-1] > indent:
                self.emitToken(self.create_dedent())
                del self.indents[-1]
};
SKIP_ : (SPACES | COMMENT | ';') -> skip;
UNKNOWN_CHAR : .;

fragment SPACES : [ \t]+;
fragment COMMENT : '/*' .*? '*/';