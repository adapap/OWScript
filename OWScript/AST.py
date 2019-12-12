class AST:
    children = []
    def __init__(self):
        self.children = []

    @property
    def format_children(self):
        return ', '.join(map(repr, self.children))

    @property
    def x(self):
        return 'X Component Of({})'

    @property
    def y(self):
        return 'Y Component Of({})'

    @property
    def z(self):
        return 'Z Component Of({})'

    @property
    def moving(self):
        return 'Compare(Speed Of({}), >, 0)'

    @property
    def facing(self):
        return 'Facing Direction Of({})'

    @property
    def pos(self):
        return 'Position Of({})'

    @property
    def eyepos(self):
        return 'Eye Position({})'

    @property
    def hero(self):
        return 'Hero Of({})'

    @property
    def team(self):
        return 'Team Of({})'

    @property
    def jumping(self):
        return 'Is Button Held({}, Jump)'

    @property
    def crouching(self):
        return 'Is Button Held({}, Crouch)'

    @property
    def interacting(self):
        return 'Is Button Held({}, Interact)'

    @property
    def lmb(self):
        return 'Is Button Held({}, Primary Fire)'

    @property
    def rmb(self):
        return 'Is Button Held({}, Secondary Fire)'

    def string(self, indent=0):
        string = ''
        if not self.__class__ == Block:
            string += ' ' * indent + '{}'.format(self.__class__.__name__) + '\n'
        else:
            indent -= 3
        for child in self.children:
            string += child.string(indent=indent + 3)
        return string

    def __repr__(self):
        if not self.children:
            return self.__class__.__name__
        return '{}({})'.format(self.__class__.__name__, self.format_children)

class Raw(AST):
    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return '<Raw {}>'.format(len(self.code))

class Import(AST):
    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return '#import {}'.format(self.path)

# Workshop Types
class WorkshopType(AST):
    @classmethod
    def get_values(cls):
        return cls._values + [x().get_values() for x in cls._extends]

    def __repr__(self):
        try:
            return self.__name__
        except AttributeError:
            return self.__class__.__name__

class Transformation(WorkshopType):
    _values = ['ROTATION', 'ROTATION AND TRANSLATION']
    _extends = []

class InvisibleTo(WorkshopType):
    _values = ['ALL', 'ENEMIES', 'NONE']
    _extends = []

class Color(WorkshopType):
    _values = ['BLUE', 'GREEN', 'PURPLE', 'RED', 'TEAM 1', 'TEAM 2', 'WHITE', 'YELLOW']
    _extends = []

class Button(WorkshopType):
    _values = ['ABILITY 1', 'ABILITY 2', 'CROUCH', 'INTERACT', 'JUMP', 'PRIMARY FIRE', 'SECONDARY FIRE', 'ULTIMATE']
    _extends = []

class Operation(WorkshopType):
    _values = ['ADD', 'APPEND TO ARRAY', 'DIVIDE', 'MAX', 'MIN', 'MODULO', 'MULTIPLY', 'RAISE TO POWER', 'REMOVE FROM ARRAY BY INDEX', 'REMOVE FROM ARRAY BY VALUE', 'SUBTRACT']
    _extends = []

class Event(WorkshopType):
    _values = ['ONGOING - EACH PLAYER', 'ONGOING - GLOBAL', 'PLAYER DEALT DAMAGE', 'PLAYER DEALT FINAL BLOW', 'PLAYER DIED', 'PLAYER EARNED ELIMINATION', 'PLAYER TOOK DAMAGE', 'PLAYER DEALT HEALING', 'PLAYER RECEIVED HEALING', 'PLAYER JOINED MATCH', 'PLAYER LEFT MATCH']
    _extends = []

class StringConstant(WorkshopType):
    _values = ['', '----------', '-> {0}', '!', '!!', '!!!', '#{0}', '({0})', '*', '...', '?', '??', '???', '{0} - {1}', '{0} - {1} - {2}', '{0} ->', '{0} -> {1}', '{0} != {1}', '{0} * {1}', '{0} / {1}', '{0} : {1} : {2}', '{0} {1}', '{0} {1} {2}', '{0} + {1}', '{0} <-', '{0} <- {1}', '{0} <->', '{0} <-> {1}', '{0} < {1}', '{0} <= {1}', '{0} = {1}', '{0} == {1}', '{0} > {1}', '{0} >= {1}', '{0} AND {1}', '{0} M', '{0} M/S', '{0} SEC', '{0} VS {1}', '{0}!', '{0}!!', '{0}!!!', '{0}%', '{0}, {1}', '{0}, {1}, AND {2}', '{0}:', '{0}: {1}', '{0}: {1} AND {2}', '{0}:{1}', '{0}?', '{0}??', '{0}???', '<- {0}', '<-> {0}', 'ABILITIES', 'ABILITY', 'ABILITY 1', 'ABILITY 2', 'ALERT', 'ALIVE', 'ALLIES', 'ALLY', 'ATTACK', 'ATTACKED', 'ATTACKING', 'ATTEMPT', 'ATTEMPTS', 'AVERAGE', 'AVOID', 'AVOIDED', 'AVOIDING', 'BACKWARD', 'BAD', 'BAN', 'BANNED', 'BANNING', 'BEST', 'BETTER', 'BOSS', 'BOSSES', 'BOUGHT', 'BUILD', 'BUILDING', 'BUILT', 'BURN', 'BURNING', 'BURNT', 'BUY', 'BUYING', 'CAPTURE', 'CAPTURED', 'CAPTURING', 'CAUTION', 'CENTER', 'CHALLENGE ACCEPTED', 'CHASE', 'CHASED', 'CHASING', 'CHECKPOINT', 'CHECKPOINTS', 'CLOUD', 'CLOUDS', 'COME HERE', 'CONDITION', 'CONGRATULATIONS', 'CONNECT', 'CONNECTED', 'CONNECTING', 'CONTROL POINT', 'CONTROL POINTS', 'COOLDOWN', 'COOLDOWNS', 'CORRUPT', 'CORRUPTED', 'CORRUPTING', 'CREDIT', 'CREDITS', 'CRITICAL', 'CROUCH', 'CROUCHED', 'CROUCHING', 'CURRENT', 'CURRENT ALLIES', 'CURRENT ALLY', 'CURRENT ATTEMPT', 'CURRENT CHECKPOINT', 'CURRENT ENEMIES', 'CURRENT ENEMY', 'CURRENT FORM', 'CURRENT GAME', 'CURRENT HERO', 'CURRENT HEROES', 'CURRENT HOSTAGE', 'CURRENT HOSTAGES', 'CURRENT LEVEL', 'CURRENT MISSION', 'CURRENT OBJECT', 'CURRENT OBJECTIVE', 'CURRENT OBJECTS', 'CURRENT PHASE', 'CURRENT PLAYER', 'CURRENT PLAYERS', 'CURRENT ROUND', 'CURRENT TARGET', 'CURRENT TARGETS', 'CURRENT UPGRADE', 'DAMAGE', 'DAMAGED', 'DAMAGING', 'DANGER', 'DEAD', 'DEFEAT', 'DEFEND', 'DEFENDED', 'DEFENDING', 'DELIVER', 'DELIVERED', 'DELIVERING', 'DESTABILIZE', 'DESTABILIZED', 'DESTABILIZING', 'DESTROY', 'DESTROYED', 'DESTROYING', 'DIE', 'DISCONNECT', 'DISCONNECTED', 'DISCONNECTING', 'DISTANCE', 'DISTANCES', 'DODGE', 'DODGED', 'DODGING', 'DOME', 'DOMES', 'DOWN', 'DOWNLOAD', 'DOWNLOADED', 'DOWNLOADING', 'DRAW', 'DROP', 'DROPPED', 'DROPPING', 'DYING', 'EAST', 'ELIMINATE', 'ELIMINATED', 'ELIMINATING', 'ELIMINATION', 'ELIMINATIONS', 'ENEMIES', 'ENEMY', 'ENTRANCE', 'ESCORT', 'ESCORTED', 'ESCORTING', 'EXCELLENT', 'EXIT', 'EXTREME', 'FAILED', 'FAILING', 'FAILURE', 'FALL', 'FALLEN', 'FALLING', 'FAR', 'FAST', 'FASTER', 'FASTEST', 'FAULT', 'FAULTS', 'FINAL', 'FINAL ALLIES', 'FINAL ALLY', 'FINAL ATTEMPT', 'FINAL CHECKPOINT', 'FINAL ENEMIES', 'FINAL ENEMY', 'FINAL FORM', 'FINAL GAME', 'FINAL HERO', 'FINAL HEROES', 'FINAL HOSTAGE', 'FINAL HOSTAGES', 'FINAL ITEM', 'FINAL LEVEL', 'FINAL MISSION', 'FINAL OBJECT', 'FINAL OBJECTIVE', 'FINAL OBJECTS', 'FINAL PHASE', 'FINAL PLAYER', 'FINAL PLAYERS', 'FINAL ROUND', 'FINAL TARGET', 'FINAL TARGETS', 'FINAL TIME', 'FINAL UPGRADE', 'FIND', 'FINDING', 'FINISH', 'FINISHED', 'FINISHING', 'FLOWN', 'FLY', 'FLYING', 'FORM', 'FORMS', 'FORWARD', 'FOUND', 'FREEZE', 'FREEZING', 'FROZEN', 'GAME', 'GAMES', 'GAMES LOST', 'GAMES WON', 'GG', 'GO', 'GOAL', 'GOALS', 'GOING', 'GOOD', 'GOOD LUCK', 'GOODBYE', 'GUILTY', 'HACK', 'HACKED', 'HACKING', 'HEAL', 'HEALED', 'HEALER', 'HEALERS', 'HEALING', 'HELLO', 'HELP', 'HERE', 'HERO', 'HEROES', 'HIDDEN', 'HIDE', 'HIDING', 'HIGH SCORE', 'HIGH SCORES', 'HMMM', 'HOSTAGE', 'HOSTAGES', 'HUH', 'HUNT', 'HUNTED', 'HUNTER', 'HUNTERS', 'HUNTING', 'I GIVE UP', 'I TRIED', 'IN VIEW', 'INCOMING', 'INITIAL', 'INITIAL ALLIES', 'INITIAL ALLY', 'INITIAL ATTEMPT', 'INITIAL CHECKPOINT', 'INITIAL ENEMIES', 'INITIAL ENEMY', 'INITIAL FORM', 'INITIAL GAME', 'INITIAL HERO', 'INITIAL HEROES', 'INITIAL HOSTAGE', 'INITIAL LEVEL', 'INITIAL MISSION', 'INITIAL OBJECT', 'INITIAL OBJECTIVE', 'INITIAL OBJECTS', 'INITIAL PHASE', 'INITIAL PLAYER', 'INITIAL PLAYERS', 'INITIAL ROUND', 'INITIAL TARGET', 'INITIAL TARGETS', 'INITIAL UPGRADE', 'INNOCENT', 'INSIDE', 'INVISIBLE', 'ITEM', 'ITEMS', 'JOIN', 'JOINED', 'JOINING', 'JUMP', 'JUMPING', 'KILL', 'KILLS', 'KILLSTREAK', 'KILLSTREAKS', 'LEADER', 'LEADERS', 'LEAST', 'LEFT', 'LESS', 'LEVEL', 'LEVELS', 'LIFE', 'LIMITED', 'LIVES', 'LOAD', 'LOADED', 'LOADING', 'LOCK', 'LOCKED', 'LOCKING', 'LOSER', 'LOSERS', 'LOSS', 'LOSSES', 'MAX', 'MILD', 'MIN', 'MISSION', 'MISSION', 'MISSION ABORTED', 'MISSION ACCOMPLISHED', 'MISSION FAILED', 'MISSIONS', 'MODERATE', 'MONEY', 'MORE', 'MOST', 'MY MISTAKE', 'NEAR', 'NEW HIGH SCORE', 'NEW RECORD', 'NEXT', 'NEXT ALLIES', 'NEXT ALLY', 'NEXT ATTEMPT', 'NEXT CHECKPOINT', 'NEXT ENEMIES', 'NEXT ENEMY', 'NEXT FORM', 'NEXT GAME', 'NEXT HERO', 'NEXT HEROES', 'NEXT HOSTAGE', 'NEXT HOSTAGES', 'NEXT LEVEL', 'NEXT MISSION', 'NEXT OBJECT', 'NEXT OBJECTIVE', 'NEXT OBJECTS', 'NEXT PHASE', 'NEXT PLAYER', 'NEXT PLAYERS', 'NEXT ROUND', 'NEXT TARGET', 'NEXT TARGETS', 'NEXT UPGRADE', 'NICE TRY', 'NO', 'NO THANKS', 'NONE', 'NORMAL', 'NORTH', 'NORTHEAST', 'NORTHWEST', 'NOT TODAY', 'OBJECT', 'OBJECTIVE', 'OBJECTIVES', 'OBJECTS', 'OBTAIN', 'OBTAINED', 'OBTAINING', 'OFF', 'ON', 'OOF', 'OOPS', 'OPTIMAL', 'OPTIMIZE', 'OPTIMIZED', 'OPTIMIZING', 'OUT OF VIEW', 'OUTGOING', 'OUTSIDE', 'OVER', 'OVERTIME', 'PAYLOAD', 'PAYLOADS', 'PHASE', 'PHASES', 'PICK', 'PICKED', 'PICKING', 'PLAYER', 'PLAYER', 'PLAYERS', 'PLAYERS', 'POINT', 'POINTS', 'POINTS EARNED', 'POINTS LOST', 'POWER-UP', 'POWER-UPS', 'PRICE', 'PROTECT', 'PROTECTED', 'PROTECTING', 'PURIFIED', 'PURIFY', 'PURIFYING', 'RAISE', 'RAISED', 'RAISING', 'RANK', 'RANK A', 'RANK B', 'RANK C', 'RANK D', 'RANK E', 'RANK F', 'RANK S', 'READY', 'RECORD', 'RECORDS', 'RECOVER', 'RECOVERED', 'RECOVERING', 'REMAIN', 'REMAINING', 'RESCUE', 'RESCUED', 'RESCUING', 'RESURRECT', 'RESURRECTED', 'RESURRECTING', 'REVEAL', 'REVEALED', 'REVEALING', 'RIGHT', 'ROUND', 'ROUND {0}', 'ROUNDS', 'ROUNDS LOST', 'ROUNDS WON', 'RUN', 'RUNNING', 'SAFE', 'SAVE', 'SAVED', 'SAVING', 'SCORE', 'SCORES', 'SECURE', 'SECURED', 'SECURING', 'SELL', 'SELLING', 'SEVER', 'SEVERE', 'SEVERED', 'SEVERING', 'SINK', 'SINKING', 'SLEEP', 'SLEEPING', 'SLEPT', 'SLOW', 'SLOWER', 'SLOWEST', 'SOLD', 'SORRY', 'SOUTH', 'SOUTHEAST', 'SOUTHWEST', 'SPARKLES', 'SPAWN', 'SPAWNED', 'SPAWNING', 'SPHERE', 'SPHERES', 'STABILIZE', 'STABILIZED', 'STABILIZING', 'STABLE', 'STAR', 'STARS', 'START', 'STARTED', 'STARTING', 'STATUS', 'STAY AWAY', 'STOP', 'STOPPED', 'STOPPING', 'STUN', 'STUNNED', 'STUNNING', 'SUBOPTIMAL', 'SUCCESS', 'SUDDEN DEATH', 'SUNK', 'SUPERB', 'SURVIVE', 'SURVIVED', 'SURVIVING', 'TARGET', 'TARGETS', 'TEAM', 'TEAMMATE', 'TEAMMATES', 'TEAMS', 'TERRIBLE', 'THANK YOU', 'THANKS', 'THAT WAS AWESOME', 'THREAT', 'THREAT LEVEL', 'THREAT LEVELS', 'THREATS', 'TIEBREAKER', 'TIME', 'TIMES', 'TOTAL', 'TRADE', 'TRADED', 'TRADING', 'TRAITOR', 'TRAITORS', 'TRANSFER', 'TRANSFERRED', 'TRANSFERRING', 'TRY AGAIN', 'TURRET', 'TURRETS', 'UGH', 'ULTIMATE ABILITY', 'UNDER', 'UNKNOWN', 'UNLIMITED', 'UNLOCK', 'UNLOCKED', 'UNLOCKING', 'UNSAFE', 'UNSTABLE', 'UP', 'UPGRADE', 'UPGRADES', 'UPLOAD', 'UPLOADED', 'UPLOADING', 'USE ABILITY 1', 'USE ABILITY 2', 'USE ULTIMATE ABILITY', 'VICTORY', 'VISIBLE', 'VORTEX', 'VORTICES', 'WAIT', 'WAITING', 'WALL', 'WALLS', 'WARNING', 'WELL PLAYED', 'WEST', 'WIN', 'WINNER', 'WINNERS', 'WINS', 'WORSE', 'WOW', 'YES', 'YOU', 'YOU LOSE', 'YOU WIN', 'ZONE', 'ZONES', '¡{0}!', '¿{0}?']
    _extends = []
    prefix = ["#{0}", "-> {0}", "<- {0}", "<-> {0}", "ROUND {0}"]
    surround = ["({0})", "¡{0}!", "¿{0}?"]
    postfix = ["{0} ->", "{0} <-", "{0} <->", "{0} M", "{0} M/S", "{0} SEC", "{0}!", "{0}!!", "{0}!!!", "{0}%", "{0}:", "{0}?", "{0}??", "{0}???"]
    binary = ["{0} - {1}", "{0} -> {1}", "{0} != {1}", "{0} * {1}", "{0} / {1}", "{0} {1}", "{0} + {1}", "{0} <- {1}", "{0} <-> {1}", "{0} < {1}", "{0} <= {1}", "{0} = {1}", "{0} == {1}", "{0} > {1}", "{0} >= {1}", "{0} AND {1}", "{0} VS {1}", "{0}, {1}", "{0}: {1}", "{0}:{1}"]
    ternary = ["{0} - {1} - {2}", "{0} {1} {2}", "{0} : {1} : {2}", "{0}, {1}, AND {2}", "{0}: {1} AND {2}"]
    normal = ["", "!", "!!", "!!!", "*", "----------", "...", "?", "??", "???", "ABILITIES", "ABILITY", "ABILITY 1", "ABILITY 2", "AGILITY", "ALERT", "ALIVE", "ALLIES", "ALLY", "AMMUNITION", "ANGLE", "ATTACK", "ATTACKED", "ATTACKING", "ATTEMPT", "ATTEMPTS", "AVERAGE", "AVOID", "AVOIDED", "AVOIDING", "BACKWARD", "BAD", "BAN", "BANNED", "BANNING", "BEST", "BETTER", "BID", "BIDS", "BLOCK", "BLOCKED", "BLOCKING", "BLUE", "BONUS", "BONUSES", "BOSS", "BOSSES", "BOUGHT", "BUILD", "BUILDING", "BUILT", "BURN", "BURNING", "BURNT", "BUY", "BUYING", "CAPTURE", "CAPTURED", "CAPTURING", "CAUTION", "CENTER", "CHALLENGE ACCEPTED", "CHARISMA", "CHASE", "CHASED", "CHASING", "CHECKPOINT", "CHECKPOINTS", "CLOUD", "CLOUDS", "CLUB", "CLUBS", "COMBO", "COME HERE", "CONDITION", "CONGRATULATIONS", "CONNECT", "CONNECTED", "CONNECTING", "CONSTITUTION", "CONTROL POINT", "CONTROL POINTS", "COOLDOWN", "COOLDOWNS", "CORRUPT", "CORRUPTED", "CORRUPTING", "CREDIT", "CREDITS", "CRITICAL", "CROUCH", "CROUCHED", "CROUCHING", "CURRENT", "CURRENT ALLIES", "CURRENT ALLY", "CURRENT ATTEMPT", "CURRENT CHECKPOINT", "CURRENT ENEMIES", "CURRENT ENEMY", "CURRENT FORM", "CURRENT GAME", "CURRENT HERO", "CURRENT HEROES", "CURRENT HOSTAGE", "CURRENT HOSTAGES", "CURRENT LEVEL", "CURRENT MISSION", "CURRENT OBJECT", "CURRENT OBJECTIVE", "CURRENT OBJECTS", "CURRENT PHASE", "CURRENT PLAYER", "CURRENT PLAYERS", "CURRENT ROUND", "CURRENT TARGET", "CURRENT TARGETS", "CURRENT UPGRADE", "DAMAGE", "DAMAGED", "DAMAGING", "DANGER", "DEAD", "DEAL", "DEALING", "DEALT", "DECK", "DECKS", "DEFEAT", "DEFEND", "DEFENDED", "DEFENDING", "DEFENSE", "DELIVER", "DELIVERED", "DELIVERING", "DEPTH", "DESTABILIZE", "DESTABILIZED", "DESTABILIZING", "DESTROY", "DESTROYED", "DESTROYING", "DETECT", "DETECTED", "DETECTING", "DEXTERITY", "DIAMOND", "DIAMONDS", "DIE", "DISCARD", "DISCARDED", "DISCARDING", "DISCONNECT", "DISCONNECTED", "DISCONNECTING", "DISTANCE", "DISTANCES", "DODGE", "DODGED", "DODGING", "DOME", "DOMES", "DOWN", "DOWNLOAD", "DOWNLOADED", "DOWNLOADING", "DRAW", "DRAWING", "DRAWN", "DROP", "DROPPED", "DROPPING", "DYING", "EAST", "ELIMINATE", "ELIMINATED", "ELIMINATING", "ELIMINATION", "ELIMINATIONS", "ENEMIES", "ENEMY", "ENTRANCE", "ESCORT", "ESCORTED", "ESCORTING", "EXCELLENT", "EXIT", "EXPERIENCE", "EXTREME", "FACE", "FACES", "FACING", "FAILED", "FAILING", "FAILURE", "FALL", "FALLEN", "FALLING", "FAR", "FAST", "FASTER", "FASTEST", "FAULT", "FAULTS", "FINAL", "FINAL ALLIES", "FINAL ALLY", "FINAL ATTEMPT", "FINAL CHECKPOINT", "FINAL ENEMIES", "FINAL ENEMY", "FINAL FORM", "FINAL GAME", "FINAL HERO", "FINAL HEROES", "FINAL HOSTAGE", "FINAL HOSTAGES", "FINAL ITEM", "FINAL LEVEL", "FINAL MISSION", "FINAL OBJECT", "FINAL OBJECTIVE", "FINAL OBJECTS", "FINAL PHASE", "FINAL PLAYER", "FINAL PLAYERS", "FINAL ROUND", "FINAL TARGET", "FINAL TARGETS", "FINAL TIME", "FINAL UPGRADE", "FIND", "FINDING", "FINISH", "FINISHED", "FINISHING", "FLOWN", "FLY", "FLYING", "FOLD", "FOLDED", "FOLDING", "FORM", "FORMS", "FORWARD", "FOUND", "FREEZE", "FREEZING", "FROZEN", "GAME", "GAMES", "GAMES LOST", "GAMES WON", "GG", "GO", "GOAL", "GOALS", "GOING", "GOOD", "GOOD LUCK", "GOODBYE", "GREEN", "GUILTY", "HACK", "HACKED", "HACKING", "HAND", "HANDS", "HEAL", "HEALED", "HEALER", "HEALERS", "HEALING", "HEART", "HEARTS", "HEIGHT", "HELLO", "HELP", "HERE", "HERO", "HEROES", "HIDDEN", "HIDE", "HIDING", "HIGH SCORE", "HIGH SCORES", "HIT", "HITTING", "HMMM", "HOSTAGE", "HOSTAGES", "HUH", "HUNT", "HUNTED", "HUNTER", "HUNTERS", "HUNTING", "I GIVE UP", "I TRIED", "IN VIEW", "INCOME", "INCOMING", "INITIAL", "INITIAL ALLIES", "INITIAL ALLY", "INITIAL ATTEMPT", "INITIAL CHECKPOINT", "INITIAL ENEMIES", "INITIAL ENEMY", "INITIAL FORM", "INITIAL GAME", "INITIAL HERO", "INITIAL HEROES", "INITIAL HOSTAGE", "INITIAL LEVEL", "INITIAL MISSION", "INITIAL OBJECT", "INITIAL OBJECTIVE", "INITIAL OBJECTS", "INITIAL PHASE", "INITIAL PLAYER", "INITIAL PLAYERS", "INITIAL ROUND", "INITIAL TARGET", "INITIAL TARGETS", "INITIAL UPGRADE", "INNOCENT", "INSIDE", "INTELLIGENCE", "INTERACT", "INVISIBLE", "ITEM", "ITEMS", "JOIN", "JOINED", "JOINING", "JUMP", "JUMPING", "KILL", "KILLS", "KILLSTREAK", "KILLSTREAK", "KILLSTREAKS", "LEADER", "LEADERS", "LEAST", "LEFT", "LESS", "LEVEL", "LEVEL DOWN", "LEVEL UP", "LEVELS", "LIFE", "LIMITED", "LIVES", "LOAD", "LOADED", "LOADING", "LOCK", "LOCKED", "LOCKING", "LOSER", "LOSERS", "LOSS", "LOSSES", "MAX", "MILD", "MIN", "MISSION", "MISSION", "MISSION ABORTED", "MISSION ACCOMPLISHED", "MISSION FAILED", "MISSIONS", "MODERATE", "MONEY", "MONSTER", "MONSTERS", "MORE", "MOST", "MY MISTAKE", "NEAR", "NEW HIGH SCORE", "NEW RECORD", "NEXT", "NEXT ALLIES", "NEXT ALLY", "NEXT ATTEMPT", "NEXT CHECKPOINT", "NEXT ENEMIES", "NEXT ENEMY", "NEXT FORM", "NEXT GAME", "NEXT HERO", "NEXT HEROES", "NEXT HOSTAGE", "NEXT HOSTAGES", "NEXT LEVEL", "NEXT MISSION", "NEXT OBJECT", "NEXT OBJECTIVE", "NEXT OBJECTS", "NEXT PHASE", "NEXT PLAYER", "NEXT PLAYERS", "NEXT ROUND", "NEXT TARGET", "NEXT TARGETS", "NEXT UPGRADE", "NICE TRY", "NO", "NO THANKS", "NONE", "NORMAL", "NORTH", "NORTHEAST", "NORTHWEST", "NOT TODAY", "OBJECT", "OBJECTIVE", "OBJECTIVES", "OBJECTS", "OBTAIN", "OBTAINED", "OBTAINING", "OFF", "ON", "OOF", "OOPS", "OPTIMAL", "OPTIMIZE", "OPTIMIZED", "OPTIMIZING", "OUT OF VIEW", "OUTGOING", "OUTSIDE", "OVER", "OVERTIME", "PARTICIPANT", "PARTICIPANTS", "PAYLOAD", "PAYLOADS", "PHASE", "PHASES", "PICK", "PICKED", "PICKING", "PILE", "PILES", "PLAY", "PLAYED", "PLAYER", "PLAYERS", "POINT", "POINTS", "POINTS EARNED", "POINTS LOST", "POWER", "POWER-UP", "POWER-UPS", "PRICE", "PRIMARY FIRE", "PROJECTILE", "PROJECTILE SPEED", "PROTECT", "PROTECTED", "PROTECTING", "PURIFIED", "PURIFY", "PURIFYING", "PURPLE", "RAISE", "RAISED", "RAISING", "RANK", "RANK A", "RANK B", "RANK C", "RANK D", "RANK E", "RANK F", "RANK S", "REACH", "REACHED", "REACHING", "READY", "RECORD", "RECORDS", "RECOVER", "RECOVERED", "RECOVERING", "RED", "REMAIN", "REMAINING", "RESCUE", "RESCUED", "RESCUING", "RESOURCE", "RESOURCES", "RESURRECT", "RESURRECTED", "RESURRECTING", "REVEAL", "REVEALED", "REVEALING", "REVERSE", "REVERSED", "REVERSING", "RIGHT", "ROUND", "ROUNDS", "ROUNDS LOST", "ROUNDS WON", "RUN", "RUNNING", "SAFE", "SAVE", "SAVED", "SAVING", "SCORE", "SCORES", "SECONDARY FIRE", "SECURE", "SECURED", "SECURING", "SELECT", "SELECTED", "SELECTING", "SELL", "SELLING", "SERVER LOAD", "SERVER LOAD AVERAGE", "SERVER LOAD PEAK", "SEVER", "SEVERE", "SEVERED", "SEVERING", "SINK", "SINKING", "SHOP", "SHOPS", "SHUFFLE", "SHUFFLED", "SHUFFLING", "SINK", "SINKING", "SKIP", "SKIPPED", "SKIPPING", "SLEEP", "SLEEPING", "SLEPT", "SLOW", "SLOWER", "SLOWEST", "SOLD", "SORRY", "SOUTH", "SOUTHEAST", "SOUTHWEST", "SPADE", "SPADES", "SPARKLES", "SPAWN", "SPAWNED", "SPAWNING", "SPEED", "SPEEDS", "SPHERE", "SPHERES", "STABILIZE", "STABILIZED", "STABILIZING", "STABLE", "STAR", "STARS", "START", "STARTED", "STARTING", "STATUS", "STAY", "STAY AWAY", "STAYED", "STAYING", "STOP", "STOPPED", "STOPPING", "STRENGTH", "STUN", "STUNNED", "STUNNING", "SUBOPTIMAL", "SUCCESS", "SUDDEN DEATH", "SUNK", "SUPERB", "SURVIVE", "SURVIVED", "SURVIVING", "TARGET", "TARGETS", "TEAM", "TEAMMATE", "TEAMMATES", "TEAMS", "TERRIBLE", "THANK YOU", "THANKS", "THAT WAS AWESOME", "THREAT", "THREAT LEVEL", "THREAT LEVELS", "THREATS", "TIEBREAKER", "TIME", "TIMES", "TOTAL", "TRADE", "TRADED", "TRADING", "TRAITOR", "TRAITORS", "TRANSFER", "TRANSFERRED", "TRANSFERRING", "TRY AGAIN", "TURRET", "TURRETS", "UGH", "ULTIMATE ABILITY", "UNDER", "UNKNOWN", "UNLIMITED", "UNLOCK", "UNLOCKED", "UNLOCKING", "UNSAFE", "UNSTABLE", "UP", "UPGRADE", "UPGRADES", "UPLOAD", "UPLOADED", "UPLOADING", "USE ABILITY 1", "USE ABILITY 2", "USE ULTIMATE ABILITY", "VICTORY", "VISIBLE", "VORTEX", "VORTICES", "WAIT", "WAITING", "WALL", "WALLS", "WARNING", "WELCOME", "WELL PLAYED", "WEST", "WHITE", "WILD", "WIN", "WINNER", "WINNERS", "WINS", "WISDOM", "WORSE", "WORST", "WOW", "YELLOW", "YES", "YOU", "YOU LOSE", "YOU WIN", "ZONE", "ZONES"]
    sorted_values = [sorted(x, key=len, reverse=True) for x in (prefix, surround, postfix, binary, ternary, normal)]

class TeamConstant(WorkshopType):
    _values = ['ALL', 'ALL TEAMS', 'TEAM 1', 'TEAM 2']
    _extends = []

class HeroConstant(WorkshopType):
    _values = ['SIGMA', 'ANA', 'ASHE', 'BAPTISTE', 'BASTION', 'BRIGITTE', 'D.VA', 'DOOMFIST', 'GENJI', 'HANZO', 'JUNKRAT', 'LÚCIO', 'MCCREE', 'MEI', 'MERCY', 'MOIRA', 'ORISA', 'PHARAH', 'REAPER', 'REINHARDT', 'ROADHOG', 'SOLDIER: 76', 'SOMBRA', 'SYMMETRA', 'TORBJÖRN', 'TRACER', 'WIDOWMAKER', 'WINSTON', 'WRECKING BALL', 'ZARYA', 'ZENYATTA']
    _extends = []

class EventPlayer(WorkshopType):
    _values = ['ALL', 'SIGMA', 'ANA', 'ASHE', 'BAPTISTE', 'BASTION', 'BRIGITTE', 'D.VA', 'DOOMFIST', 'GENJI', 'HANZO', 'JUNKRAT', 'LÚCIO', 'MCCREE', 'MEI', 'MERCY', 'MOIRA', 'ORISA', 'PHARAH', 'REAPER', 'REINHARDT', 'ROADHOG', 'SLOT 0', 'SLOT 1', 'SLOT 10', 'SLOT 11', 'SLOT 2', 'SLOT 3', 'SLOT 4', 'SLOT 5', 'SLOT 6', 'SLOT 7', 'SLOT 8', 'SLOT 9', 'SOLDIER: 76', 'SOMBRA', 'SYMMETRA', 'TORBJÖRN', 'TRACER', 'WIDOWMAKER', 'WINSTON', 'WRECKING BALL', 'ZARYA', 'ZENYATTA']
    _extends = []

class Variable(WorkshopType):
    _values = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    _extends = []

    def __init__(self, value, index):
        self.value = value
        self.index = index

class PlayEffect(WorkshopType):
    _values = ['BAD EXPLOSION', 'BAD PICKUP EFFECT', 'BUFF EXPLOSION SOUND', 'BUFF IMPACT SOUND', 'DEBUFF IMPACT SOUND', 'EXPLOSION SOUND', 'GOOD EXPLOSION', 'GOOD PICKUP EFFECT', 'RING EXPLOSION', 'RING EXPLOSION SOUND']
    _extends = []

class CreateEffect(WorkshopType):
    _values = ['BAD AURA', 'BAD AURA SOUND', 'BEACON SOUND', 'CLOUD', 'DECAL SOUND', 'ENERGY SOUND', 'GOOD AURA', 'GOOD AURA SOUND', 'LIGHT SHAFT', 'ORB', 'PICK-UP SOUND', 'RING', 'SMOKE SOUND', 'SPARKLES', 'SPARKLES SOUND', 'SPHERE']
    _extends = []

class Communicate(WorkshopType):
    _values = ['ACKNOWLEDGE', 'EMOTE DOWN', 'EMOTE LEFT', 'EMOTE RIGHT', 'EMOTE UP', 'GROUP UP', 'HELLO', 'NEED HEALING', 'THANKS', 'ULTIMATE STATUS', 'VOICE LINE DOWN', 'VOICE LINE LEFT', 'VOICE LINE RIGHT', 'VOICE LINE UP']
    _extends = []

class Icon(WorkshopType):
    _values = ['ARROW: DOWN', 'ARROW: LEFT', 'ARROW: RIGHT', 'ARROW: UP', 'ASTERISK', 'BOLT', 'CHECKMARK', 'CIRCLE', 'CLUB', 'DIAMOND', 'DIZZY', 'EXCLAMATION MARK', 'EYE', 'FIRE', 'FLAG', 'HALO', 'HAPPY', 'HEART', 'MOON', 'NO', 'PLUS', 'POISON', 'POISON 2', 'QUESTION MARK', 'RADIOACTIVE', 'RECYCLE', 'RING THICK', 'RING THIN', 'SAD', 'SKULL', 'SPADE', 'SPIRAL', 'STOP', 'TRASHCAN', 'WARNING', 'X']
    _extends = []

class Relative(WorkshopType):
    _values = ['TO PLAYER', 'TO WORLD']
    _extends = []

class Motion(WorkshopType):
    _values = ['CANCEL CONTRARY MOTION', 'INCORPORATE CONTRARY MOTION']
    _extends = []

class RoundingType(WorkshopType):
    _values = ['DOWN', 'TO NEAREST', 'UP']
    _extends = []

class LosCheck(WorkshopType):
    _values = ['OFF', 'SURFACES', 'SURFACES AND ALL BARRIERS', 'SURFACES AND ENEMY BARRIERS']
    _extends = []

class WorldTextClipping(WorkshopType):
    _values = ['CLIP AGAINST SURFACES', 'DO NOT CLIP']
    _extends = []

class HudLocation(WorkshopType):
    _values = ['LEFT', 'RIGHT', 'TOP']
    _extends = []

class IconReevaluation(WorkshopType):
    _values = ['NONE', 'POSITION', 'VISIBLE TO', 'VISIBLE TO AND POSITION']
    _extends = []

class EffectReevaluation(WorkshopType):
    _values = ['NONE', 'POSITION AND RADIUS', 'VISIBLE TO', 'VISIBLE TO, POSITION, AND RADIUS']
    _extends = []

class HudTextReevaluation(WorkshopType):
    _values = ['STRING', 'VISIBLE TO AND STRING']
    _extends = []

class WorldTextReevaluation(WorkshopType):
    _values = ['STRING', 'VISIBLE TO AND STRING', 'VISIBLE TO, POSITION, AND STRING']
    _extends = []

class ChaseRateReevaluation(WorkshopType):
    _values = ['DESTINATION AND RATE', 'NONE']
    _extends = []

class ChaseTimeReevaluation(WorkshopType):
    _values = ['DESTINATION AND DURATION', 'NONE']
    _extends = []

class ObjectiveDescriptionReevaluation(WorkshopType):
    _values = ['STRING', 'VISIBLE TO AND STRING']
    _extends = []

class DamageModificationReevaluation(WorkshopType):
    _values = ['NONE', 'RECEIVERS AND DAMAGERS', 'RECEIVERS, DAMAGERS, AND DAMAGE PERCENT']
    _extends = []

class FacingReevaluation(WorkshopType):
    _values = ['NONE', 'DIRECTION AND TURN RATE']
    _extends = []

class WaitBehavior(WorkshopType):
    _values = ['ABORT WHEN FALSE', 'IGNORE CONDITION', 'RESTART WHEN TRUE']
    _extends = []

class BarriersLos(WorkshopType):
    _values = ['ALL BARRIERS BLOCK LOS', 'BARRIERS DO NOT BLOCK LOS', 'ENEMY BARRIERS BLOCK LOS']
    _extends = []

class Status(WorkshopType):
    _values = ['ASLEEP', 'BURNING', 'FROZEN', 'HACKED', 'INVINCIBLE', 'KNOCKED DOWN', 'PHASED OUT', 'ROOTED', 'STUNNED', 'UNKILLABLE']
    _extends = []

class CompareOperator(WorkshopType):
    _values = ['==', '!=', '<', '<=', '>', '>=']
    _extends = []

class Any(WorkshopType):
    _values = ['ANY']
    _extends = []

class Boolean(WorkshopType):
    _values = ['AND', 'ARRAY CONTAINS', 'COMPARE', 'ENTITY EXISTS', 'EVENT WAS CRITICAL HIT', 'FALSE', 'HAS SPAWNED', 'HAS STATUS', 'IS ALIVE', 'IS TRUE FOR ALL', 'IS TRUE FOR ANY', 'IS USING ULTIMATE', 'IS ASSEMBLING HEROES', 'IS BETWEEN ROUNDS', 'IS BUTTON HELD', 'IS COMMUNICATING', 'IS COMMUNICATING ANY', 'IS COMMUNICATING ANY EMOTE', 'IS COMMUNICATING ANY VOICE LINE', 'IS CONTROL MODE POINT LOCKED', 'IS CROUCHING', 'IS CTF MODE IN SUDDEN DEATH', 'IS DEAD', 'IS FIRING PRIMARY', 'IS FIRING SECONDARY', 'IS FLAG AT BASE', 'IS FLAG BEING CARRIED', 'IS GAME IN PROGRESS', 'IS HERO BEING PLAYED', 'IS IN AIR', 'IS IN LINE OF SIGHT', 'IS IN SETUP', 'IS IN SPAWN ROOM', 'IS IN VIEW ANGLE', 'IS MATCH COMPLETE', 'IS MOVING', 'IS OBJECTIVE COMPLETE', 'IS ON GROUND', 'IS ON OBJECTIVE', 'IS ON WALL', 'IS PORTRAIT ON FIRE', 'IS STANDING', 'IS TEAM ON DEFENSE', 'IS TEAM ON OFFENSE', 'IS USING ABILITY 1', 'IS USING ABILITY 2', 'IS WAITING FOR PLAYERS', 'NOT', 'OR', 'TRUE']
    _extends = [Any]

class Hero(WorkshopType):
    _values = ['ALL HEROES', 'ALLOWED HEROES', 'HERO', 'HERO OF']
    _extends = [Any]

class Number(WorkshopType):
    _values = ['INDEX OF ARRAY VALUE', 'EVENT HEALING', 'ABSOLUTE VALUE', 'ALTITUDE OF', 'ANGLE DIFFERENCE', 'CONTROL MODE SCORING PERCENTAGE', 'COSINE FROM DEGREES', 'COSINE FROM RADIANS', 'COUNT OF', 'DISTANCE BETWEEN', 'DOT PRODUCT', 'EVENT DAMAGE', 'HEALTH', 'HEALTH PERCENT', 'HORIZONTAL ANGLE FROM DIRECTION', 'HORIZONTAL ANGLE TOWARDS', 'HORIZONTAL FACING ANGLE OF', 'HORIZONTAL SPEED OF', 'LAST DAMAGE MODIFICATION ID', 'LAST DAMAGE OVER TIME ID', 'LAST HEAL OVER TIME ID', 'LAST TEXT ID', 'MATCH ROUND', 'MATCH TIME', 'MAX', 'MAX HEALTH', 'MIN', 'MODULO', 'NUMBER', 'NUMBER OF DEAD PLAYERS', 'NUMBER OF DEATHS', 'NUMBER OF ELIMINATIONS', 'NUMBER OF FINAL BLOWS', 'NUMBER OF HEROES', 'NUMBER OF LIVING PLAYERS', 'NUMBER OF PLAYERS', 'NUMBER OF PLAYERS ON OBJECTIVE', 'OBJECTIVE INDEX', 'PAYLOAD PROGRESS PERCENTAGE', 'POINT CAPTURE PERCENTAGE', 'RAISE TO POWER', 'RANDOM INTEGER', 'RANDOM REAL', 'ROUND TO INTEGER', 'SCORE OF', 'SINE FROM DEGREES', 'SINE FROM RADIANS', 'SLOT OF', 'SPEED OF', 'SPEED OF IN DIRECTION', 'SQUARE ROOT', 'TEAM SCORE', 'TOTAL TIME ELAPSED', 'ULTIMATE CHARGE PERCENT', 'VERTICAL ANGLE FROM DIRECTION', 'VERTICAL ANGLE TOWARDS', 'VERTICAL FACING ANGLE OF', 'VERTICAL SPEED OF', 'X COMPONENT OF', 'Y COMPONENT OF', 'Z COMPONENT OF']
    _extends = [Any]

    def __init__(self, value):
        self.value = value

    def __int__(self):
        return int(self.value)

    def __add__(self, other):
        return float(self.value) + float(other.value)

    def __sub__(self, other):
        return float(self.value) - float(other.value)

    def __mul__(self, other):
        return float(self.value) * float(other.value)

    def __truediv__(self, other):
        return float(self.value) / float(other.value)

    def __pow__(self, other):
        return float(self.value) ** float(other.value)

    def __mod__(self, other):
        return float(self.value) % float(other.value)

    def __repr__(self):
        return '{}'.format(self.value)

class Vector(WorkshopType):
    _values = ['VELOCITY OF']
    _extends = [Any]


class Direction(WorkshopType):
    _values = ['DIRECTION TOWARDS', 'FACING DIRECTION OF', 'RAY CAST HIT NORMAL', 'VECTOR TOWARDS', 'LEFT', 'RIGHT', 'FORWARD', 'BACKWARD', 'UP', 'DOWN']
    _extends = [Vector]

class Position(WorkshopType):
    _values = ['EYE POSITION', 'FLAG POSITION', 'NEAREST WALKABLE POSITION', 'OBJECTIVE POSITION', 'PAYLOAD POSITION', 'POSITION OF', 'RAY CAST HIT POSITION']
    _extends = [Vector]

class BaseVector(WorkshopType):
    _values = ['CROSS PRODUCT', 'DIRECTION FROM ANGLES', 'LOCAL VECTOR OF', 'NORMALIZE', 'THROTTLE OF', 'VECTOR', 'WORLD VECTOR OF']
    _extends = [Direction, Position]

class Player(WorkshopType):
    _values = ['HEALER', 'HEALEE', 'HOST PLAYER', 'PLAYERS IN VIEW ANGLE', 'PLAYER CLOSEST TO RETICLE', 'ALL DEAD PLAYERS', 'ALL LIVING PLAYERS', 'ALL PLAYERS', 'ALL PLAYERS NOT ON OBJECTIVE', 'ALL PLAYERS ON OBJECTIVE', 'ATTACKER', 'CLOSEST PLAYER TO', 'EVENT PLAYER', 'FARTHEST PLAYER FROM', 'LAST CREATED ENTITY', 'NULL', 'PLAYER CARRYING FLAG', 'PLAYERS IN SLOT', 'PLAYERS ON HERO', 'PLAYERS WITHIN RADIUS', 'RAY CAST HIT PLAYER', 'VICTIM']
    _extends = [BaseVector]


class Team(WorkshopType):
    _values = ['CONTROL MODE SCORING TEAM', 'OPPOSITE TEAM OF', 'TEAM', 'TEAM OF']
    _extends = [Any]

class String(WorkshopType):
    _values = ['HERO ICON STRING', 'STRING']
    _extends = [Any]

    def __init__(self, value, length=None):
        super().__init__()
        self.value = value
        self.length = length

    def get_length(self):
        return self.length + sum(child.get_length for child in self.children)

    def __repr__(self):
        return '{}({}){}'.format(self.value, ', '.join(map(repr, self.children)), f'[{self.length}]' if self.length else '')

class CustomString(WorkshopType):
    _values = ['HERO ICON STRING', 'STRING']
    _extends = [Any]

    def __init__(self, value, length=None):
        super().__init__()
        self.value = value
        self.length = length

    def get_length(self):
        return self.length + sum(child.get_length for child in self.children)

    def __repr__(self):
        return '{}({}){}'.format(self.value, ', '.join(map(repr, self.children)), f'[{self.length}]' if self.length else '')
        
class Base(WorkshopType):
    _values = ['ADD', 'APPEND TO ARRAY', 'ARRAY SLICE', 'CURRENT ARRAY ELEMENT', 'DIVIDE', 'EMPTY ARRAY', 'FILTERED ARRAY', 'FIRST OF', 'GLOBAL VARIABLE', 'LAST OF', 'MULTIPLY', 'PLAYER VARIABLE', 'RANDOM VALUE IN ARRAY', 'RANDOMIZED ARRAY', 'REMOVE FROM ARRAY', 'SORTED ARRAY', 'SUBTRACT', 'VALUE IN ARRAY']
    _extends = [Any, Boolean, Hero, Number, Direction, Position, Player, Team]

class Terminal(AST):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self):
        return '{}'.format(self.value)

class Data(AST):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def __repr__(self):
        if not self.children:
            return self.name
        return '{}({})'.format(self.name, self.format_children)

class OWID(AST):
    def __init__(self, name, description='', args=[]):
        super().__init__()
        self.name = name
        self.description = description
        self.args = args

    def __repr__(self):
        return '{}({})'.format(self.name, ', '.join(map(repr, self.args)))

class Constant(AST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def halt(self, tp):
        return Raw(code='Apply Impulse({}, Down, Multiply(0.001, 0.001), To World, Cancel Contrary Motion)'.format(self.name.title()))

class BinaryOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return '{} {} {}'.format(self.left, self.op, self.right)

class UnaryOp(AST):
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return '{} {}'.format(self.op, self.right)

class Trailer(AST):
    def __init__(self, parent):
        self.parent = parent

class Script(AST):
    pass

class Rule(Data):
    def __init__(self, name, disabled):
        super().__init__(name)
        self.disabled = disabled

class Ruleblock(Data):
    pass

class Block(AST):
    def __repr__(self):
        return '{}'.format(self.format_children)

class Time(Terminal):
    pass

class Array(AST):
    def __init__(self, elements=None):
        self.elements = elements or []

    def append(self, tp, elem):
        elem = tp.visit(elem, tp.scope)
        if type(elem) != Object:
            elem = Raw(code=elem)
        self.elements.append(elem)

    def index(self, elem):
        return self.elements.index(elem)

    def __iter__(self):
        return iter(self.elements)

    def __len__(self):
        return len(self.elements)

    def __setitem__(self, index, item):
        while index > len(self) - 1:
            self.elements.append(Number(value='0'))
        self.elements.__setitem__(index, item)

    def __getitem__(self, index):
        return self.elements.__getitem__(index)

    def __repr__(self):
        return '{}'.format(self.elements)

class Compare(BinaryOp):
    pass

class Assign(BinaryOp):
    pass

class GlobalVar(AST):
    def __init__(self, letter, index=None):
        self.letter = letter
        self.index = index

    def __repr__(self):
        return 'Global.{}[{}]'.format(self.letter, self.index)

class PlayerVar(AST):
    def __init__(self, letter, index=None, player=None):
        self.letter = letter
        self.index = index
        self.player = player or Constant(name='Event Player')

    def __repr__(self):
        return 'Player@{}.{}[{}]'.format(self.player, self.letter, self.index)

class Var(AST):
    GLOBAL = 0
    PLAYER = 1
    INTERNAL = 2
    BUILTIN = 3
    CONST = 4
    STRING = 5
    CLASS = 6
    OBJECT = 7
    METHOD = 8

    def __init__(self, name, type_, value=None, data=None, player=None, chase=False):
        self.name = name
        self.type = type_
        self.value = value
        self.data = data
        self.player = player

    @property
    def _type(self):
        return {
            0: 'GLOBAL',
            1: 'PLAYER',
            2: 'INTERNAL',
            3: 'BUILTIN',
            4: 'CONST',
            5: 'STRING',
            6: 'CLASS',
            7: 'OBJECT',
            8: 'METHOD'
        }.get(self.type)

    def __repr__(self):
        if self.value or self.data:
            return '<{}: type={}, value={}, data={}>'.format(self.name, self._type, self.value, self.data)
        return '{}'.format(self.name)

class If(AST):
    def __init__(self, cond, true_block, false_block=None):
        self.cond = cond
        self.true_block = true_block
        self.false_block = false_block

    def __repr__(self):
        return 'if {}: {} | else: {}'.format(self.cond, self.true_block, self.false_block)

class While(AST):
    def __init__(self, cond, body):
        self.cond = cond
        self.body = body

    def __repr__(self):
        return 'while {}: {}'.format(self.cond, self.body)

class For(AST):
    def __init__(self, pointer, iterable, body):
        self.pointer = pointer
        self.iterable = iterable
        self.body = body

    def __repr__(self):
        return 'for {} in {}: {}'.format(self.pointer, self.iterable, self.body)

class Function(AST):
    def __init__(self, name, params):
        super().__init__()
        self.name = name
        self.params = params
        self.closure = None

    @property
    def arity(self):
        return len(self.params)

    @property
    def min_arity(self):
        return len([p for p in self.params if not p.optional])

    def __repr__(self):
        return '%{}({}): {}'.format(self.name, ', '.join(map(repr, self.params)), self.format_children)

class Parameter(AST):
    def __init__(self, name, optional=False, default=None):
        self.name = name
        self.optional = optional
        self.default = None or Constant(name='Null')

    def __repr__(self):
        return 'param {}{}'.format(self.name, '?=' + repr(self.default) if self.default else '')

class Class(AST):
    def __init__(self, name, body):
        self.name = name
        self.body = body
        self.closure = None

    def __repr__(self):
        return 'class {}'.format(self.name)

class Object():
    def __init__(self, type_):
        self.type = type_
        self.env = {}
    
    def __getattr__(self, attr):
        return self.env.get(attr)
    
    def __repr__(self):
        return '<obj {}>'.format(self.type.name)

class Return(AST):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'return {}'.format(self.value)

class Attribute(Trailer):
    def __init__(self, name, parent):
        super().__init__(parent)
        self.name = name

    def __repr__(self):
        return '{}.{}'.format(self.parent, self.name)

class Call(Trailer):
    def __init__(self, args, parent):
        super().__init__(parent)
        self.args = args

    def __repr__(self):
        return '{}({})'.format(self.parent, self.args)

class Item(Trailer):
    def __init__(self, index, parent):
        super().__init__(parent)
        self.index = index

    def __repr__(self):
        return '{}[{}]'.format(self.parent, self.index)
