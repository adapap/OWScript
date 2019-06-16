import re
class Token:
    """Stores token information such as data and line number."""
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f'<{self.type}: {self.value} ({self.line}:{self.column})>'

ALIASES = {
    'CONST': {
        'CUR ELEM': 'CURRENT ARRAY ELEMENT',
        'EVERYONE': 'ALL PLAYERS(TEAM(ALL))',
        'LUCIO': 'LÚCIO',
        'ON EACH PLAYER': 'ONGOING - EACH PLAYER',
        'ON GLOBAL': 'ONGOING - GLOBAL',
        'TORBJORN': 'TORBJÖRN',
        'VISIBLE TO, POSITION, AND RADIUS': 'VISIBLE TO POSITION AND RADIUS',
        'VISIBLE TO, POSITION, AND STRING': 'VISIBLE TO POSITION AND STRING'
    },
    'VALUE': {
        'ABS': 'ABSOLUTE VALUE',
        'ANY TRUE': 'IS TRUE FOR ANY',
        'ALL TRUE': 'IS TRUE FOR ALL',
        'ARRAY CONTAINS': 'ARRAY CONTAINS',
        'COS': 'COSINE FROM DEGREES',
        'COSR': 'COSINE FROM RADIANS',
        'INDEX': 'INDEX OF ARRAY VALUE',
        'PLAYERS IN RADIUS': 'PLAYERS WITHIN RADIUS',
        'ROUND': 'ROUND TO INTEGER',
        'SIN': 'SINE FROM DEGREES',
        'SINR': 'SINE FROM RADIANS'
    },
    'ACTION': {
        'BIG MSG': 'BIG MESSAGE',
        'HUD': 'CREATE HUD TEXT',
        'MSG': 'SMALL MESSAGE',
        'SMALL MSG': 'SMALL MESSAGE',
        'TEXT': 'CREATE IN-WORLD TEXT'
    }
}
CONST = ['ABORT WHEN FALSE', 'ALL HEROES', 'ALL', 'ANA', 'ASHE', 'ATTACKER', 'BACKWARD', 'BAD AURA SOUND', 'BAD AURA', 'BAPTISTE', 'BASTION', 'BEACON SOUND', 'BLUE', 'BRIGITTE', 'CLOUD', 'CONTROL MODE SCORING TEAM', 'CURRENT ARRAY ELEMENT', 'D.VA', 'DECAL SOUND', 'DESTINATION AND DURATION', 'DESTINATION AND RATE', 'DOOMFIST', 'DOWN', 'EMPTY ARRAY', 'ENERGY SOUND', 'EVENT PLAYER', 'EVENT WAS CRITICAL HIT', 'FALSE', 'FORWARD', 'GENJI', 'GOOD AURA SOUND', 'GOOD AURA', 'GREEN', 'HANZO', 'IGNORE CONDITION', 'IS ASSEMBLING HEROES', 'IS BETWEEN ROUNDS', 'IS CONTROL MODE POINT LOCKED', 'IS CTF MODE IN SUDDEN DEATH', 'IS GAME IN PROGRESS', 'IS IN SETUP', 'IS MATCH COMPLETE', 'IS WAITING FOR PLAYERS', 'JUNKRAT', 'LAST CREATED ENTITY', 'LEFT', 'LIGHT SHAFT', 'LÚCIO', 'MCCREE', 'MEI', 'MERCY', 'MOIRA', 'NONE', 'NULL', 'OFF', 'ONGOING - EACH PLAYER', 'ONGOING - GLOBAL', 'ORB', 'ORISA', 'PAYLOAD POSITION', 'PHARAH', 'PICK-UP SOUND', 'PLAYER DEALT DAMAGE', 'PLAYER DEALT FINAL BLOW', 'PLAYER DIED', 'PLAYER EARNED ELIMINATION', 'PLAYER TOOK DAMAGE', 'POSITION AND RADIUS', 'PURPLE', 'REAPER', 'RECEIVERS AND DAMAGERS', 'RECEIVERS, DAMAGERS, AND DAMAGE PERCENT', 'RED', 'REINHARDT', 'RESTART WHEN TRUE', 'RIGHT', 'RING', 'ROADHOG', 'SMOKE SOUND', 'SOLDIER: 76', 'SOMBRA', 'SPARKLES SOUND', 'SPARKLES', 'SPHERE', 'STRING', 'SURFACES AND ALL BARRIERS', 'SURFACES AND ENEMY BARRIERS', 'SURFACES', 'SYMMETRA', 'TEAM 1', 'TEAM 2', 'TOP', 'TORBJÖRN', 'TRACER', 'TRUE', 'UP', 'VICTIM', 'VISIBLE TO AND STRING', 'VISIBLE TO', 'VISIBLE TO, POSITION, AND RADIUS', 'VISIBLE TO, POSITION, AND STRING', 'WHITE', 'WIDOWMAKER', 'WINSTON', 'WRECKING BALL', 'YELLOW', 'ZARYA', 'ZENYATTA']
CONST.extend(ALIASES.get('CONST').keys())
VALUE = ['ABSOLUTE VALUE', 'ADD', 'ALL DEAD PLAYERS', 'ALL LIVING PLAYERS', 'ALL PLAYERS NOT ON OBJECTIVE', 'ALL PLAYERS ON OBJECTIVE', 'ALL PLAYERS', 'ALLOWED HEROES', 'ALTITUDE OF', 'ANGLE DIFFERENCE', 'APPEND TO ARRAY', 'ARRAY SLICE', 'CLOSEST PLAYER TO', 'COMPARE', 'CONTROL MODE SCORING PERCENTAGE', 'COSINE FROM DEGREES', 'COSINE FROM RADIANS', 'COUNT OF', 'CROSS PRODUCT', 'DIRECTION FROM ANGLES', 'DIRECTION TOWARDS', 'DISTANCE BETWEEN', 'DIVIDE', 'DOT PRODUCT', 'ENTITY EXISTS', 'EVENT DAMAGE', 'EYE POSITION', 'FACING DIRECTION OF', 'FARTHEST PLAYER FROM', 'FILTERED ARRAY', 'FIRST OF', 'FLAG POSITION', 'GLOBAL VARIABLE', 'HAS SPAWNED', 'HAS STATUS', 'HEALTH PERCENT', 'HEALTH', 'HERO ICON STRING', 'HERO OF', 'HERO', 'HORIZONTAL ANGLE FROM DIRECTION', 'HORIZONTAL ANGLE TOWARDS', 'HORIZONTAL FACING ANGLE OF', 'HORIZONTAL SPEED OF', 'INDEX OF ARRAY VALUE', 'IS ALIVE', 'IS BUTTON HELD', 'IS COMMUNICATING ANY EMOTE', 'IS COMMUNICATING ANY VOICE LINE', 'IS COMMUNICATING ANY', 'IS COMMUNICATING', 'IS CROUCHING', 'IS DEAD', 'IS FIRING PRIMARY', 'IS FIRING SECONDARY', 'IS FLAG AT BASE', 'IS FLAG BEING CARRIED', 'IS HERO BEING PLAYED', 'IS IN AIR', 'IS IN LINE OF SIGHT', 'IS IN SPAWN ROOM', 'IS IN VIEW ANGLE', 'IS MOVING', 'IS OBJECTIVE COMPLETE', 'IS ON GROUND', 'IS ON OBJECTIVE', 'IS ON WALL', 'IS PORTRAIT ON FIRE', 'IS STANDING', 'IS TEAM ON DEFENSE', 'IS TEAM ON OFFENSE', 'IS TRUE FOR ALL', 'IS TRUE FOR ANY', 'IS USING ABILITY 1', 'IS USING ABILITY 2', 'IS USING ULTIMATE', 'LAST DAMAGE MODIFICATION ID', 'LAST DAMAGE OVER TIME ID', 'LAST HEAL OVER TIME ID', 'LAST OF', 'LAST TEXT ID', 'LOCAL VECTOR OF', 'MATCH ROUND', 'MATCH TIME', 'MAX HEALTH', 'MAX', 'MIN', 'MODULO', 'MULTIPLY', 'NEAREST WALKABLE POSITION', 'NORMALIZE', 'NUMBER OF DEAD PLAYERS', 'NUMBER OF DEATHS', 'NUMBER OF ELIMINATIONS', 'NUMBER OF FINAL BLOWS', 'NUMBER OF HEROES', 'NUMBER OF LIVING PLAYERS', 'NUMBER OF PLAYERS ON OBJECTIVE', 'NUMBER OF PLAYERS', 'NUMBER', 'OBJECTIVE INDEX', 'OBJECTIVE POSITION', 'OPPOSITE TEAM OF', 'PAYLOAD PROGRESS PERCENTAGE', 'PLAYER CARRYING FLAG', 'PLAYER CLOSEST TO RETICLE', 'PLAYER VARIABLE', 'PLAYERS IN SLOT', 'PLAYERS IN VIEW ANGLE', 'PLAYERS ON HERO', 'PLAYERS WITHIN RADIUS', 'POINT CAPTURE PERCENTAGE', 'POSITION OF', 'RAISE TO POWER', 'RANDOM INTEGER', 'RANDOM REAL', 'RANDOM VALUE IN ARRAY', 'RANDOMIZED ARRAY', 'RAY CAST HIT NORMAL', 'RAY CAST HIT PLAYER', 'RAY CAST HIT POSITION', 'REMOVE FROM ARRAY', 'ROUND TO INTEGER', 'SCORE OF', 'SINE FROM DEGREES', 'SINE FROM RADIANS', 'SLOT OF', 'SORTED ARRAY', 'SPEED OF IN DIRECTION', 'SPEED OF', 'SQUARE ROOT', 'SUBTRACT', 'TEAM OF', 'TEAM SCORE', 'TEAM', 'THROTTLE OF', 'TOTAL TIME ELAPSED', 'ULTIMATE CHARGE PERCENT', 'VALUE IN ARRAY', 'VECTOR TOWARDS', 'VECTOR', 'VELOCITY OF', 'VERTICAL ANGLE FROM DIRECTION', 'VERTICAL ANGLE TOWARDS', 'VERTICAL FACING ANGLE OF', 'VERTICAL SPEED OF', 'WORLD VECTOR OF', 'X COMPONENT OF', 'Y COMPONENT OF', 'Z COMPONENT OF']
VALUE.extend(ALIASES.get('VALUE').keys())
ACTION = ['ABORT IF CONDITION IS FALSE', 'ABORT IF CONDITION IS TRUE', 'ABORT IF', 'ABORT', 'ALLOW BUTTON', 'APPLY IMPULSE', 'BIG MESSAGE', 'CHASE GLOBAL VARIABLE AT RATE', 'CHASE GLOBAL VARIABLE OVER TIME', 'CHASE PLAYER VARIABLE AT RATE', 'CHASE PLAYER VARIABLE OVER TIME', 'CLEAR STATUS', 'COMMUNICATE', 'CREATE EFFECT', 'CREATE HUD TEXT', 'CREATE ICON', 'CREATE IN-WORLD TEXT', 'DAMAGE', 'DECLARE MATCH DRAW', 'DECLARE PLAYER VICTORY', 'DECLARE ROUND VICTORY', 'DECLARE TEAM VICTORY', 'DESTROY ALL EFFECTS', 'DESTROY ALL HUD TEXT', 'DESTROY ALL ICONS', 'DESTROY ALL IN-WORLD TEXT', 'DESTROY EFFECT', 'DESTROY HUD TEXT', 'DESTROY ICON', 'DESTROY IN-WORLD TEXT', 'DISABLE BUILT-IN GAME MODE ANNOUNCER', 'DISABLE BUILT-IN GAME MODE COMPLETION', 'DISABLE BUILT-IN GAME MODE MUSIC', 'DISABLE BUILT-IN GAME MODE RESPAWNING', 'DISABLE BUILT-IN GAME MODE SCORING', 'DISABLE DEATH SPECTATE ALL PLAYERS', 'DISABLE DEATH SPECTATE TARGET HUD', 'DISALLOW BUTTON', 'ENABLE BUILT-IN GAME MODE ANNOUNCER', 'ENABLE BUILT-IN GAME MODE COMPLETION', 'ENABLE BUILT-IN GAME MODE MUSIC', 'ENABLE BUILT-IN GAME MODE RESPAWNING', 'ENABLE BUILT-IN GAME MODE SCORING', 'ENABLE DEATH SPECTATE ALL PLAYERS', 'ENABLE DEATH SPECTATE TARGET HUD', 'GO TO ASSEMBLE HEROES', 'HEAL', 'KILL', 'LOOP IF CONDITION IS FALSE', 'LOOP IF CONDITION IS TRUE', 'LOOP IF', 'LOOP', 'MODIFY GLOBAL VARIABLE', 'MODIFY PLAYER SCORE', 'MODIFY PLAYER VARIABLE', 'MODIFY TEAM SCORE', 'PAUSE MATCH TIME', 'PLAY EFFECT', 'PRELOAD HERO', 'PRESS BUTTON', 'RESET PLAYER HERO AVAILABILITY', 'RESPAWN', 'RESURRECT', 'SET ABILITY 1 ENABLED', 'SET ABILITY 2 ENABLED', 'SET AIM SPEED', 'SET DAMAGE DEALT', 'SET DAMAGE RECEIVED', 'SET FACING', 'SET GLOBAL VARIABLE AT INDEX', 'SET GLOBAL VARIABLE', 'SET GRAVITY', 'SET HEALING DEALT', 'SET HEALING RECEIVED', 'SET INVISIBLE', 'SET MATCH TIME', 'SET MAX HEALTH', 'SET MOVE SPEED', 'SET OBJECTIVE DESCRIPTION', 'SET PLAYER ALLOWED HEROES', 'SET PLAYER SCORE', 'SET PLAYER VARIABLE AT INDEX', 'SET PLAYER VARIABLE', 'SET PRIMARY FIRE ENABLED', 'SET PROJECTILE GRAVITY', 'SET PROJECTILE SPEED', 'SET RESPAWN MAX TIME', 'SET SECONDARY FIRE ENABLED', 'SET SLOW MOTION', 'SET STATUS', 'SET TEAM SCORE', 'SET ULTIMATE ABILITY ENABLED', 'SET ULTIMATE CHARGE', 'SKIP IF', 'SKIP', 'SMALL MESSAGE', 'START ACCELERATING', 'START CAMERA', 'START DAMAGE MODIFICATION', 'START DAMAGE OVER TIME', 'START FACING', 'START FORCING PLAYER TO BE HERO', 'START FORCING SPAWN ROOM', 'START FORCING THROTTLE', 'START HEAL OVER TIME', 'START HOLDING BUTTON', 'STOP ACCELERATING', 'STOP ALL DAMAGE MODIFICATIONS', 'STOP ALL DAMAGE OVER TIME', 'STOP ALL HEAL OVER TIME', 'STOP CAMERA', 'STOP CHASING GLOBAL VARIABLE', 'STOP CHASING PLAYER VARIABLE', 'STOP DAMAGE MODIFICATION', 'STOP DAMAGE OVER TIME', 'STOP FACING', 'STOP FORCING PLAYER TO BE HERO', 'STOP FORCING SPAWN ROOM', 'STOP FORCING THROTTLE', 'STOP HEAL OVER TIME', 'STOP HOLDING BUTTON', 'TELEPORT', 'UNPAUSE MATCH TIME', 'WAIT']
ACTION.extend(ALIASES.get('ACTION').keys())
OWID = CONST + VALUE + ACTION
OWID.sort(key=len, reverse=True)
#print('|'.join(OWID))

class Tokens:
    """Mapping of token names to regular expressions."""
    COMMENT : r'(\/\*(.|[\n])*?\*\/\n?|\/\/[^\n]*\n?)'
    COMPARE : r'(>=|<=|==|!=|>|<)'
    ASSIGN : r'(=|\+=|-=|\*=|\/=|^=|%=)'
    PLUS : r'\+'
    MINUS : r'\-'
    TIMES : r'\*'
    DIVIDE : r'\/'
    POW : r'\^'
    MOD : r'%'
    AT : r'@'
    COMMA : r','
    LPAREN : r'\('
    RPAREN : r'\)'
    LBRACK : r'\['
    RBRACK : r'\]'
    STRING : r'("[^\\\r\n\f]*?"|\'[^\\\r\n\f]*?\')'
    F_STRING : r'`[^\\\r\n\f]*?`'
    TIME : r'[0-9]+(\.[0-9]+)?(ms|s|min)'
    FLOAT : r'[0-9]+\.[0-9]+'
    INTEGER : r'[0-9]+'
    IF : r'IF\b'
    ELIF : r'ELIF\b'
    ELSE : r'ELSE\b'
    WHILE : r'WHILE\b'
    FOR : r'FOR\b'
    NOT_IN : r'NOT IN\b'
    IN : r'IN\b'
    NOT : r'NOT\b'
    AND : r'AND\b'
    OR : r'OR\b'
    PVAR : r'PVAR\b'
    GVAR : r'GVAR\b'
    RULE : r'RULE\b'
    OWID : fr'({"|".join(OWID)})(?=[\b\s\n\(\),]+)'
    ANNOTATION : r'[_a-zA-Z0-9][_a-zA-Z0-9]*:(?!\n)'
    RULEBLOCK : r'(EVENT|CONDITIONS|ACTIONS)\b'
    NAME : r'[_a-zA-Z][_\-a-zA-Z0-9]*'
    WHITESPACE : r'[ \t]+'
    NEWLINE : r'[\r\n\f]+'
    SEMI : r';'
    COLON : r':'
    DOT : r'\.'