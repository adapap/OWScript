grammar OWScript;

/* Parser Rules */
tokens { INDENT, DEDENT }

@lexer::members {
    self.keywords = ['if', 'in', 'not', 'and', 'or', 'elif', 'else', 'while', 'pVar', 'gVar']

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
stmt : (funcdef | ruleset | NAME call);

funcdef : '%' NAME param_list? funcbody;
funcbody : (NEWLINE INDENT (ruleset | ruledef | rulebody) DEDENT) | block;

ruleset : (ruledef NEWLINE?)+;
ruledef : RULE rulename (NEWLINE INDENT rulebody* DEDENT)+;
rulename : STRING;
rulebody : RULEBLOCK ruleblock #RulebodyBlock
         | primary call NEWLINE #RCall;

ruleblock : block;
block : NEWLINE INDENT line+ DEDENT
      | line;
line : assign
     | if_stmt
     | while_stmt
     | for_stmt
     | const
     | action
     | value
     | (action | value | const) NEWLINE? comp_op=('<'|'>'|'=='|'>='|'<='|'!=') primary
     | name (call | method)?
     | ANNOTATION line
     | NEWLINE;

assign : expr ASSIGN expr;
if_stmt : IF expr ':' block (ELIF expr ':' block)* (ELSE ':' else_block=block)?;
while_stmt : WHILE expr ':' block;
for_stmt : FOR NAME IN expr ':' block;
expr : logic_or;
logic_or : logic_and (OR logic_and)*;
logic_and : logic_not (AND logic_not)*;
logic_not : (NOT logic_not) | compare;
compare : arith (('<'|'>'|'=='|'>='|'<='|'!='|IN|NOT IN) arith)*?;
arith : unary ('^' unary)* # Pow
      | unary ('*' unary)* # Mul
      | unary ('/' unary)* # Div
      | unary ('+' unary)* # Add
      | unary ('-' unary)* # Sub
      | unary ('%' unary)* # Mod;
unary : ('+' | '-') unary | primary;

primary : ( action
        | value
        | const
        | name
        | variable
        | vector
        | time
        | numeral
        | array
        | string
        | '(' expr ')') trailer*;
action : ACTION after_line;
value : VALUE after_line attribute*;
const : CONST attribute*;
string : STRING
       | F_STRING after_line;
after_line : '(' arg_list ')'
           | NEWLINE INDENT (primary|ANNOTATION primary|NEWLINE)+ DEDENT
           | NEWLINE;
param_list : '(' NAME (',' NAME)* ')';
arg_list : primary (',' primary)*;

trailer : item
        | method
        | call;
item : '[' INTEGER ']';
call : '(' arg_list? ')';
attribute : '.' name;
method : attribute call;

name : NAME;
time : numeral ('MS' | 'S' | 'MIN');
numeral : num_const=FLOAT
        | num_const=INTEGER;
variable : global_var
         | player_var
         | name;
global_var : GVAR varname=NAME;
player_var : PVAR varname=NAME ('@' primary)?;
vector : '<' unary ',' unary ',' unary '>';
array : '[' arg_list? ']';

/* Lexer Rules */
ASSIGN : ('='|'+='|'-='|'*='|'/='|'^='|'%=');
STRING : '"' ~[\\\r\n\f"]* '"';
F_STRING : '`' ~[\\\r\n\f`]* '`';
FLOAT : [0-9]+'.'[0-9]+;
INTEGER : [0-9]+;
ANNOTATION : [_a-zA-Z][_a-zA-Z0-9]* ':';
CONST : 'ALL'
      | 'ALL HEROES'
      | 'ATTACKER'
      | 'BACKWARD'
      | 'BAD AURA'
      | 'BAD AURA SOUND'
      | 'BEACON SOUND'
      | 'BLUE'
      | 'CLOUD'
      | 'CONTROL MODE SCORING TEAM'
      | 'CURRENT ARRAY ELEMENT'
      | 'DECAL SOUND'
      | 'DOWN'
      | 'EMPTY ARRAY'
      | 'ENERGY SOUND'
      | 'EVENT PLAYER'
      | 'EVENT WAS CRITICAL HIT'
      | 'FALSE'
      | 'FORWARD'
      | 'GOOD AURA'
      | 'GOOD AURA SOUND'
      | 'GREEN'
      | 'IS ASSEMBLING HEROES'
      | 'IS BETWEEN ROUNDS'
      | 'IS CONTROL MODE POINT LOCKED'
      | 'IS CTF MODE IN SUDDEN DEATH'
      | 'IS GAME IN PROGRESS'
      | 'IS IN SETUP'
      | 'IS MATCH COMPLETE'
      | 'IS WAITING FOR PLAYERS'
      | 'LAST CREATED ENTITY'
      | 'LEFT'
      | 'LIGHT SHAFT'
      | 'NONE'
      | 'NULL'
      | 'OFF'
      | 'ONGOING - EACH PLAYER'
      | 'ONGOING - GLOBAL'
      | 'ORB'
      | 'PAYLOAD POSITION'
      | 'PICK-UP SOUND'
      | 'PLAYER DEALT DAMAGE'
      | 'PLAYER DEALT FINAL BLOW'
      | 'PLAYER DIED'
      | 'PLAYER EARNED ELIMINATION'
      | 'PLAYER TOOK DAMAGE'
      | 'POSITION AND RADIUS'
      | 'PURPLE'
      | 'RED'
      | 'RIGHT'
      | 'RING'
      | 'SMOKE SOUND'
      | 'SPARKLES'
      | 'SPARKLES SOUND'
      | 'SPHERE'
      | 'SURFACES'
      | 'SURFACES AND ALL BARRIERS'
      | 'SURFACES AND ENEMY BARRIERS'
      | 'TEAM 1'
      | 'TEAM 2'
      | 'TRUE'
      | 'UP'
      | 'VICTIM'
      | 'VISIBLE TO'
      | 'VISIBLE TO, POSITION, AND RADIUS'
      | 'WHITE'
      | 'YELLOW';
ACTION : 'ABORT'
       | 'ABORT IF'
       | 'ABORT IF CONDITION IS FALSE'
       | 'ABORT IF CONDITION IS TRUE'
       | 'ALLOW BUTTON'
       | 'APPLY IMPULSE'
       | 'BIG MESSAGE'
       | 'CHASE GLOBAL VARIABLE AT RATE'
       | 'CHASE GLOBAL VARIABLE OVER TIME'
       | 'CHASE PLAYER VARIABLE AT RATE'
       | 'CHASE PLAYER VARIABLE OVER TIME'
       | 'CLEAR STATUS'
       | 'COMMUNICATE'
       | 'CREATE EFFECT'
       | 'CREATE HUD TEXT'
       | 'CREATE ICON'
       | 'CREATE IN-WORLD TEXT'
       | 'DAMAGE'
       | 'DECLARE MATCH DRAW'
       | 'DECLARE PLAYER VICTORY'
       | 'DECLARE ROUND VICTORY'
       | 'DECLARE TEAM VICTORY'
       | 'DESTROY ALL EFFECTS'
       | 'DESTROY ALL HUD TEXT'
       | 'DESTROY ALL ICONS'
       | 'DESTROY ALL IN-WORLD TEXT'
       | 'DESTROY EFFECT'
       | 'DESTROY HUD TEXT'
       | 'DESTROY ICON'
       | 'DESTROY IN-WORLD TEXT'
       | 'DISABLE BUILT-IN GAME MODE ANNOUNCER'
       | 'DISABLE BUILT-IN GAME MODE COMPLETION'
       | 'DISABLE BUILT-IN GAME MODE MUSIC'
       | 'DISABLE BUILT-IN GAME MODE RESPAWNING'
       | 'DISABLE BUILT-IN GAME MODE SCORING'
       | 'DISABLE DEATH SPECTATE ALL PLAYERS'
       | 'DISABLE DEATH SPECTATE TARGET HUD'
       | 'DISALLOW BUTTON'
       | 'ENABLE BUILT-IN GAME MODE ANNOUNCER'
       | 'ENABLE BUILT-IN GAME MODE COMPLETION'
       | 'ENABLE BUILT-IN GAME MODE MUSIC'
       | 'ENABLE BUILT-IN GAME MODE RESPAWNING'
       | 'ENABLE BUILT-IN GAME MODE SCORING'
       | 'ENABLE DEATH SPECTATE ALL PLAYERS'
       | 'ENABLE DEATH SPECTATE TARGET HUD'
       | 'GO TO ASSEMBLE HEROES'
       | 'HEAL'
       | 'KILL'
       | 'LOOP'
       | 'LOOP IF'
       | 'LOOP IF CONDITION IS FALSE'
       | 'LOOP IF CONDITION IS TRUE'
       | 'MODIFY GLOBAL VARIABLE'
       | 'MODIFY PLAYER SCORE'
       | 'MODIFY PLAYER VARIABLE'
       | 'MODIFY TEAM SCORE'
       | 'PAUSE MATCH TIME'
       | 'PLAY EFFECT'
       | 'PRELOAD HERO'
       | 'PRESS BUTTON'
       | 'RESET PLAYER HERO AVAILABILITY'
       | 'RESPAWN'
       | 'RESURRECT'
       | 'SET ABILITY 1 ENABLED'
       | 'SET ABILITY 2 ENABLED'
       | 'SET AIM SPEED'
       | 'SET DAMAGE DEALT'
       | 'SET DAMAGE RECEIVED'
       | 'SET FACING'
       | 'SET GLOBAL VARIABLE'
       | 'SET GLOBAL VARIABLE AT INDEX'
       | 'SET GRAVITY'
       | 'SET HEALING DEALT'
       | 'SET HEALING RECEIVED'
       | 'SET INVISIBLE'
       | 'SET MATCH TIME'
       | 'SET MAX HEALTH'
       | 'SET MOVE SPEED'
       | 'SET OBJECTIVE DESCRIPTION'
       | 'SET PLAYER ALLOWED HEROES'
       | 'SET PLAYER SCORE'
       | 'SET PLAYER VARIABLE'
       | 'SET PLAYER VARIABLE AT INDEX'
       | 'SET PRIMARY FIRE ENABLED'
       | 'SET PROJECTILE GRAVITY'
       | 'SET PROJECTILE SPEED'
       | 'SET RESPAWN MAX TIME'
       | 'SET SECONDARY FIRE ENABLED'
       | 'SET SLOW MOTION'
       | 'SET STATUS'
       | 'SET TEAM SCORE'
       | 'SET ULTIMATE ABILITY ENABLED'
       | 'SET ULTIMATE CHARGE'
       | 'SKIP'
       | 'SKIP IF'
       | 'SMALL MESSAGE'
       | 'START ACCELERATING'
       | 'START CAMERA'
       | 'START DAMAGE MODIFICATION'
       | 'START DAMAGE OVER TIME'
       | 'START FACING'
       | 'START FORCING PLAYER TO BE HERO'
       | 'START FORCING SPAWN ROOM'
       | 'START FORCING THROTTLE'
       | 'START HEAL OVER TIME'
       | 'START HOLDING BUTTON'
       | 'STOP ACCELERATING'
       | 'STOP ALL DAMAGE MODIFICATIONS'
       | 'STOP ALL DAMAGE OVER TIME'
       | 'STOP ALL HEAL OVER TIME'
       | 'STOP CAMERA'
       | 'STOP CHASING GLOBAL VARIABLE'
       | 'STOP CHASING PLAYER VARIABLE'
       | 'STOP DAMAGE MODIFICATION'
       | 'STOP DAMAGE OVER TIME'
       | 'STOP FACING'
       | 'STOP FORCING PLAYER TO BE HERO'
       | 'STOP FORCING SPAWN ROOM'
       | 'STOP FORCING THROTTLE'
       | 'STOP HEAL OVER TIME'
       | 'STOP HOLDING BUTTON'
       | 'TELEPORT'
       | 'UNPAUSE MATCH TIME'
       | 'WAIT';
VALUE : 'ABSOLUTE VALUE'
      | 'ADD'
      | 'ALL DEAD PLAYERS'
      | 'ALL LIVING PLAYERS'
      | 'ALL PLAYERS'
      | 'ALL PLAYERS NOT ON OBJECTIVE'
      | 'ALL PLAYERS ON OBJECTIVE'
      | 'ALLOWED HEROES'
      | 'ALTITUDE OF'
      | 'ANGLE DIFFERENCE'
      | 'APPEND TO ARRAY'
      | 'ARRAY CONTAINS'
      | 'ARRAY SLICE'
      | 'CLOSEST PLAYER TO'
      | 'COMPARE'
      | 'CONTROL MODE SCORING PERCENTAGE'
      | 'COSINE FROM DEGREES'
      | 'COSINE FROM RADIANS'
      | 'COUNT OF'
      | 'CROSS PRODUCT'
      | 'DIRECTION FROM ANGLES'
      | 'DIRECTION TOWARDS'
      | 'DISTANCE BETWEEN'
      | 'DIVIDE'
      | 'DOT PRODUCT'
      | 'ENTITY EXISTS'
      | 'EVENT DAMAGE'
      | 'EYE POSITION'
      | 'FACING DIRECTION OF'
      | 'FARTHEST PLAYER FROM'
      | 'FILTERED ARRAY'
      | 'FIRST OF'
      | 'FLAG POSITION'
      | 'GLOBAL VARIABLE'
      | 'HAS SPAWNED'
      | 'HAS STATUS'
      | 'HEALTH'
      | 'HEALTH PERCENT'
      | 'HERO'
      | 'HERO ICON STRING'
      | 'HERO OF'
      | 'HORIZONTAL ANGLE FROM DIRECTION'
      | 'HORIZONTAL ANGLE TOWARDS'
      | 'HORIZONTAL FACING ANGLE OF'
      | 'HORIZONTAL SPEED OF'
      | 'INDEX OF ARRAY VALUE'
      | 'IS ALIVE'
      | 'IS BUTTON HELD'
      | 'IS COMMUNICATING'
      | 'IS COMMUNICATING ANY'
      | 'IS COMMUNICATING ANY EMOTE'
      | 'IS COMMUNICATING ANY VOICE LINE'
      | 'IS CROUCHING'
      | 'IS DEAD'
      | 'IS FIRING PRIMARY'
      | 'IS FIRING SECONDARY'
      | 'IS FLAG AT BASE'
      | 'IS FLAG BEING CARRIED'
      | 'IS HERO BEING PLAYED'
      | 'IS IN AIR'
      | 'IS IN LINE OF SIGHT'
      | 'IS IN SPAWN ROOM'
      | 'IS IN VIEW ANGLE'
      | 'IS MOVING'
      | 'IS OBJECTIVE COMPLETE'
      | 'IS ON GROUND'
      | 'IS ON OBJECTIVE'
      | 'IS ON WALL'
      | 'IS PORTRAIT ON FIRE'
      | 'IS STANDING'
      | 'IS TEAM ON DEFENSE'
      | 'IS TEAM ON OFFENSE'
      | 'IS TRUE FOR ALL'
      | 'IS TRUE FOR ANY'
      | 'IS USING ABILITY 1'
      | 'IS USING ABILITY 2'
      | 'IS USING ULTIMATE'
      | 'LAST DAMAGE MODIFICATION ID'
      | 'LAST DAMAGE OVER TIME ID'
      | 'LAST HEAL OVER TIME ID'
      | 'LAST OF'
      | 'LAST TEXT ID'
      | 'LOCAL VECTOR OF'
      | 'MATCH ROUND'
      | 'MATCH TIME'
      | 'MAX'
      | 'MAX HEALTH'
      | 'MIN'
      | 'MODULO'
      | 'MULTIPLY'
      | 'NEAREST WALKABLE POSITION'
      | 'NORMALIZE'
      | 'NUMBER'
      | 'NUMBER OF DEAD PLAYERS'
      | 'NUMBER OF DEATHS'
      | 'NUMBER OF ELIMINATIONS'
      | 'NUMBER OF FINAL BLOWS'
      | 'NUMBER OF HEROES'
      | 'NUMBER OF LIVING PLAYERS'
      | 'NUMBER OF PLAYERS'
      | 'NUMBER OF PLAYERS ON OBJECTIVE'
      | 'OBJECTIVE INDEX'
      | 'OBJECTIVE POSITION'
      | 'OPPOSITE TEAM OF'
      | 'PAYLOAD PROGRESS PERCENTAGE'
      | 'PLAYER CARRYING FLAG'
      | 'PLAYER CLOSEST TO RETICLE'
      | 'PLAYER VARIABLE'
      | 'PLAYERS IN SLOT'
      | 'PLAYERS IN VIEW ANGLE'
      | 'PLAYERS ON HERO'
      | 'PLAYERS WITHIN RADIUS'
      | 'POINT CAPTURE PERCENTAGE'
      | 'POSITION OF'
      | 'RAISE TO POWER'
      | 'RANDOM INTEGER'
      | 'RANDOM REAL'
      | 'RANDOM VALUE IN ARRAY'
      | 'RANDOMIZED ARRAY'
      | 'RAY CAST HIT NORMAL'
      | 'RAY CAST HIT PLAYER'
      | 'RAY CAST HIT POSITION'
      | 'REMOVE FROM ARRAY'
      | 'ROUND TO INTEGER'
      | 'SCORE OF'
      | 'SINE FROM DEGREES'
      | 'SINE FROM RADIANS'
      | 'SLOT OF'
      | 'SORTED ARRAY'
      | 'SPEED OF'
      | 'SPEED OF IN DIRECTION'
      | 'SQUARE ROOT'
      | 'STRING'
      | 'SUBTRACT'
      | 'TEAM'
      | 'TEAM OF'
      | 'TEAM SCORE'
      | 'THROTTLE OF'
      | 'TOTAL TIME ELAPSED'
      | 'ULTIMATE CHARGE PERCENT'
      | 'VALUE IN ARRAY'
      | 'VECTOR'
      | 'VECTOR TOWARDS'
      | 'VELOCITY OF'
      | 'VERTICAL ANGLE FROM DIRECTION'
      | 'VERTICAL ANGLE TOWARDS'
      | 'VERTICAL FACING ANGLE OF'
      | 'VERTICAL SPEED OF'
      | 'WORLD VECTOR OF'
      | 'X COMPONENT OF'
      | 'Y COMPONENT OF'
      | 'Z COMPONENT OF';
RULEBLOCK : 'EVENT'
          | 'CONDITIONS'
          | 'ACTIONS';
ALIAS : ('ALL TRUE'
      | 'BIG MSG'
      | 'COS'
      | 'COSR'
      | 'MSG'
      | 'ON GLOBAL'
      | 'ON EACH PLAYER'
      | 'PLAYERS IN RADIUS'
      | 'ROUND'
      | 'SIN'
      | 'SINR'
      | 'SMALL MSG'
      // Builtins
      | 'EVERYONE') {
from OWScriptParser import OWScriptParser
self.text = self.text.strip().upper()
_ACTION = OWScriptParser.ACTION
_VALUE = OWScriptParser.VALUE
_CONST = OWScriptParser.CONST
aliases = dict([
('BIG MSG', ('BIG MESSAGE', _ACTION)),
('MSG', ('SMALL MESSAGE', _ACTION)),
('SMALL MSG', ('SMALL MESSAGE', _ACTION)),

('ABS', ('ABSOLUTE VALUE', _VALUE)),
('ALL TRUE', ('IS TRUE FOR ALL', _VALUE)),
('COS', ('COSINE FROM DEGREES', _VALUE)),
('COSR', ('COSINE FROM RADIANS', _VALUE)),
('PLAYERS IN RADIUS', ('PLAYERS WITHIN RADIUS', _VALUE)),
('ROUND', ('ROUND TO INTEGER', _VALUE)),
('SIN', ('SINE FROM DEGREES', _VALUE)),
('SINR', ('SINE FROM RADIANS', _VALUE)),

('EVERYONE', ('ALL PLAYERS(TEAM(ALL))', _CONST)),
('ON EACH PLAYER', ('ONGOING - EACH PLAYER', _CONST)),
('ON GLOBAL', ('ONGOING - GLOBAL', _CONST))
])
if self.text.upper() in aliases:
    self.text, self.type = aliases.get(self.text.upper())
};
RULE : 'RULE';
IF : 'IF';
ELIF : 'ELIF';
ELSE : 'ELSE';
WHILE : 'WHILE';
FOR : 'FOR';
IN : 'IN';
NOT : 'NOT';
AND : 'AND';
OR : 'OR';
PVAR : 'PVAR';
GVAR : 'GVAR';
NAME : [_a-zA-Z][_\-a-zA-Z0-9]*;
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
fragment COMMENT : '/*' [. \n]*? '*/'
                 | '//' ~[\n]*;