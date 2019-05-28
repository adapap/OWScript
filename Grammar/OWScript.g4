grammar OWScript;

/* Parser Rules */
tokens { INDENT, DEDENT, ACTION, VALUE, NUMBER }

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
        ('ACTIONS', 'ACTIONS'),
        ('CONDITIONS', 'CONDITIONS'),
        ('EVENT', 'EVENT'),
        ('ON EACH PLAYER', 'NAME'),
        ('ON GLOBAL', 'NAME'),
        ('ONGOING - EACH PLAYER', 'NAME'),
        ('ONGOING - GLOBAL', 'NAME'),
        ('PLAYER DEALT DAMAGE', 'NAME'),
        ('PLAYER DEALT FINAL BLOW', 'NAME'),
        ('PLAYER DIED', 'NAME'),
        ('PLAYER EARNED ELIMINATION', 'NAME'),
        ('PLAYER TOOK DAMAGE', 'NAME'),
        ('ABSOLUTE VALUE', 'NUMBER'),
        ('ALTITUDE OF', 'NUMBER'),
        ('ANGLE DIFFERENCE', 'NUMBER'),
        ('CONTROL MODE SCORING PERCENTAGE', 'NUMBER'),
        ('COS', 'NUMBER'),
        ('COSINE FROM DEGREES', 'NUMBER'),
        ('COSINE FROM RADIANS', 'NUMBER'),
        ('COSR', 'NUMBER'),
        ('COUNT OF', 'NUMBER'),
        ('DISTANCE BETWEEN', 'NUMBER'),
        ('DOT PRODUCT', 'NUMBER'),
        ('EVENT DAMAGE', 'NUMBER'),
        ('HEALTH', 'NUMBER'),
        ('HEALTH PERCENT', 'NUMBER'),
        ('HORIZONTAL ANGLE FROM DIRECTION', 'NUMBER'),
        ('HORIZONTAL ANGLE TOWARDS', 'NUMBER'),
        ('HORIZONTAL FACING ANGLE OF', 'NUMBER'),
        ('HORIZONTAL SPEED OF', 'NUMBER'),
        ('LAST DAMAGE MODIFICATION ID', 'NUMBER'),
        ('LAST DAMAGE OVER TIME ID', 'NUMBER'),
        ('LAST HEAL OVER TIME ID', 'NUMBER'),
        ('LAST TEXT ID', 'NUMBER'),
        ('MATCH ROUND', 'NUMBER'),
        ('MATCH TIME', 'NUMBER'),
        ('MAX', 'NUMBER'),
        ('MAX HEALTH', 'NUMBER'),
        ('MIN', 'NUMBER'),
        ('MODULO', 'NUMBER'),
        ('NUMBER', 'NUMBER'),
        ('NUMBER OF DEAD PLAYERS', 'NUMBER'),
        ('NUMBER OF DEATHS', 'NUMBER'),
        ('NUMBER OF ELIMINATIONS', 'NUMBER'),
        ('NUMBER OF FINAL BLOWS', 'NUMBER'),
        ('NUMBER OF HEROES', 'NUMBER'),
        ('NUMBER OF LIVING PLAYERS', 'NUMBER'),
        ('NUMBER OF PLAYERS', 'NUMBER'),
        ('NUMBER OF PLAYERS ON OBJECTIVE', 'NUMBER'),
        ('OBJECTIVE INDEX', 'NUMBER'),
        ('PAYLOAD PROGRESS PERCENTAGE', 'NUMBER'),
        ('POINT CAPTURE PERCENTAGE', 'NUMBER'),
        ('RAISE TO POWER', 'NUMBER'),
        ('RANDOM INTEGER', 'NUMBER'),
        ('RANDOM REAL', 'NUMBER'),
        ('ROUND', 'NUMBER'),
        ('ROUND TO INTEGER', 'NUMBER'),
        ('SCORE OF', 'NUMBER'),
        ('SIN', 'NUMBER'),
        ('SINE FROM DEGREES', 'NUMBER'),
        ('SINE FROM RADIANS', 'NUMBER'),
        ('SINR', 'NUMBER'),
        ('SLOT OF', 'NUMBER'),
        ('SPEED OF', 'NUMBER'),
        ('SPEED OF IN DIRECTION', 'NUMBER'),
        ('SQUARE ROOT', 'NUMBER'),
        ('TEAM SCORE', 'NUMBER'),
        ('TOTAL TIME ELAPSED', 'NUMBER'),
        ('ULTIMATE CHARGE PERCENT', 'NUMBER'),
        ('VERTICAL ANGLE FROM DIRECTION', 'NUMBER'),
        ('VERTICAL ANGLE TOWARDS', 'NUMBER'),
        ('VERTICAL FACING ANGLE OF', 'NUMBER'),
        ('VERTICAL SPEED OF', 'NUMBER'),
        ('X COMPONENT OF', 'NUMBER'),
        ('Y COMPONENT OF', 'NUMBER'),
        ('Z COMPONENT OF', 'NUMBER'),
        ('ADD', 'VALUE'),
        ('ALL DEAD PLAYERS', 'VALUE'),
        ('ALL HEROES', 'VALUE'),
        ('ALL LIVING PLAYERS', 'VALUE'),
        ('ALL PLAYERS', 'VALUE'),
        ('ALL PLAYERS NOT ON OBJECTIVE', 'VALUE'),
        ('ALL PLAYERS ON OBJECTIVE', 'VALUE'),
        ('ALLOWED HEROES', 'VALUE'),
        ('AND', 'VALUE'),
        ('APPEND TO ARRAY', 'VALUE'),
        ('ARRAY SLICE', 'VALUE'),
        ('ATTACKER', 'VALUE'),
        ('BACKWARD', 'VALUE'),
        ('CLOSEST PLAYER TO', 'VALUE'),
        ('COMPARE', 'VALUE'),
        ('CONTROL MODE SCORING TEAM', 'VALUE'),
        ('CROSS PRODUCT', 'VALUE'),
        ('CURRENT ARRAY ELEMENT', 'VALUE'),
        ('DIRECTION FROM ANGLES', 'VALUE'),
        ('DIRECTION TOWARDS', 'VALUE'),
        ('DIVIDE', 'VALUE'),
        ('DOWN', 'VALUE'),
        ('EMPTY ARRAY', 'VALUE'),
        ('ENTITY EXISTS', 'VALUE'),
        ('EVENT PLAYER', 'VALUE'),
        ('EVENT WAS CRITICAL HIT', 'VALUE'),
        ('EYE POSITION', 'VALUE'),
        ('FACING DIRECTION OF', 'VALUE'),
        ('FALSE', 'VALUE'),
        ('FARTHEST PLAYER FROM', 'VALUE'),
        ('FILTERED ARRAY', 'VALUE'),
        ('FIRST OF', 'VALUE'),
        ('FLAG POSITION', 'VALUE'),
        ('FORWARD', 'VALUE'),
        ('GLOBAL VARIABLE', 'VALUE'),
        ('HAS SPAWNED', 'VALUE'),
        ('HAS STATUS', 'VALUE'),
        ('HERO', 'VALUE'),
        ('HERO ICON STRING', 'VALUE'),
        ('HERO OF', 'VALUE'),
        ('INDEX OF ARRAY VALUE', 'VALUE'),
        ('IS ALIVE', 'VALUE'),
        ('IS ASSEMBLING HEROES', 'VALUE'),
        ('IS BETWEEN ROUNDS', 'VALUE'),
        ('IS BUTTON HELD', 'VALUE'),
        ('IS COMMUNICATING', 'VALUE'),
        ('IS COMMUNICATING ANY', 'VALUE'),
        ('IS COMMUNICATING ANY EMOTE', 'VALUE'),
        ('IS COMMUNICATING ANY VOICE LINE', 'VALUE'),
        ('IS CONTROL MODE POINT LOCKED', 'VALUE'),
        ('IS CROUCHING', 'VALUE'),
        ('IS CTF MODE IN SUDDEN DEATH', 'VALUE'),
        ('IS DEAD', 'VALUE'),
        ('IS FIRING PRIMARY', 'VALUE'),
        ('IS FIRING SECONDARY', 'VALUE'),
        ('IS FLAG AT BASE', 'VALUE'),
        ('IS FLAG BEING CARRIED', 'VALUE'),
        ('IS GAME IN PROGRESS', 'VALUE'),
        ('IS HERO BEING PLAYED', 'VALUE'),
        ('IS IN AIR', 'VALUE'),
        ('IS IN LINE OF SIGHT', 'VALUE'),
        ('IS IN SETUP', 'VALUE'),
        ('IS IN SPAWN ROOM', 'VALUE'),
        ('IS IN VIEW ANGLE', 'VALUE'),
        ('IS MATCH COMPLETE', 'VALUE'),
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
        ('IS WAITING FOR PLAYERS', 'VALUE'),
        ('LAST CREATED ENTITY', 'VALUE'),
        ('LAST OF', 'VALUE'),
        ('LEFT', 'VALUE'),
        ('LOCAL VECTOR OF', 'VALUE'),
        ('MULTIPLY', 'VALUE'),
        ('NEAREST WALKABLE POSITION', 'VALUE'),
        ('NORMALIZE', 'VALUE'),
        ('NOT', 'VALUE'),
        ('NULL', 'VALUE'),
        ('OBJECTIVE POSITION', 'VALUE'),
        ('OPPOSITE TEAM OF', 'VALUE'),
        ('OR', 'VALUE'),
        ('PAYLOAD POSITION', 'VALUE'),
        ('PLAYER CARRYING FLAG', 'VALUE'),
        ('PLAYER CLOSEST TO RETICLE', 'VALUE'),
        ('PLAYER VARIABLE', 'VALUE'),
        ('PLAYERS IN RADIUS', 'VALUE'),
        ('PLAYERS IN SLOT', 'VALUE'),
        ('PLAYERS IN VIEW ANGLE', 'VALUE'),
        ('PLAYERS ON HERO', 'VALUE'),
        ('PLAYERS WITHIN RADIUS', 'VALUE'),
        ('POSITION OF', 'VALUE'),
        ('RANDOM VALUE IN ARRAY', 'VALUE'),
        ('RANDOMIZED ARRAY', 'VALUE'),
        ('RAY CAST HIT NORMAL', 'VALUE'),
        ('RAY CAST HIT PLAYER', 'VALUE'),
        ('RAY CAST HIT POSITION', 'VALUE'),
        ('REMOVE FROM ARRAY', 'VALUE'),
        ('RIGHT', 'VALUE'),
        ('SORTED ARRAY', 'VALUE'),
        ('STRING', 'VALUE'),
        ('SUBTRACT', 'VALUE'),
        ('TEAM', 'VALUE'),
        ('TEAM OF', 'VALUE'),
        ('THROTTLE OF', 'VALUE'),
        ('TRUE', 'VALUE'),
        ('UP', 'VALUE'),
        ('VALUE IN ARRAY', 'VALUE'),
        ('VECTOR', 'VALUE'),
        ('VECTOR TOWARDS', 'VALUE'),
        ('VELOCITY OF', 'VALUE'),
        ('VICTIM', 'VALUE'),
        ('WORLD VECTOR OF', 'VALUE')
    ])
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
        self.emitToken(self.common_token(OWScriptLexer.NEWLINE, '\n'));

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
    from OWScriptParser import OWScriptParser
    dedent = self.common_token(OWScriptParser.DEDENT, '')
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

script : (NEWLINE | stmt)* EOF;
stmt : (funcdef | ruleset);

funcdef : '%' NAME;// funcbody?;
//funcbody : '1';

ruleset : ruledef+;
ruledef : 'Rule' rulename rulebody*;
rulename : STRING;
rulebody : NEWLINE INDENT ('Event' | 'Conditions' | 'Actions') block? DEDENT;

block : NEWLINE INDENT line+ DEDENT;
line : action
     | value
     | number
     | assign
     | name
     | NEWLINE;

name : NAME;

action : ACTION after_line;
value : VALUE after_line;
number : NUMBER after_line;

assign : INTEGER ASSIGN INTEGER;

after_line : NEWLINE;

/* Lexer Rules */
STRING : '"' ~[\\\r\n\f"]* '"';
INTEGER : [0-9]+;
FLOAT : [0-9]+'.'[0-9]+;
NAME : [_a-zA-Z0-9\- ]*[_a-zA-Z] {
    from OWScriptParser import OWScriptParser
    if self.text.upper() in self.workshop_rules:
        attr = self.workshop_rules.get(self.text.upper())
        print('attr:', attr)
        self.type = getattr(OWScriptParser, attr)
    };
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
            self.emitToken(self.common_token(OWScriptParser.INDENT, spaces))
        else:
            while len(self.indents) > 0 and self.indents[-1] > indent:
                self.emitToken(self.create_dedent())
                del self.indents[-1]
};
SKIP_ : (SPACES | COMMENT) -> skip;
UNKNOWN_CHAR : .;

fragment SPACES : [ \t]+;
fragment COMMENT : '/*' .*? '*/';