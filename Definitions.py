from typing import Tuple, Union
class Syntax:
    definitions = {}
    aliases = {}

class Player(Syntax):
    def __init__(self):
        self.definitions = {
            'Event Player': None
        }

class Team(Syntax):
    def __init__(self):
        self.definitions = {
            'All': None,
            'Team 1': None,
            'Team 2': None
        }

class Hero(Syntax):
    def __init__(self):
        self.definitions = {
            'Ana': None,
            'Soldier: 76': None
        }

class Players(Syntax):
    def __init__(self):
        self.definitions = {
            'All': None,
            'Slot 0': None,
            'Slot 1': None,
            'Slot 2': None,
            'Slot 3': None,
            'Slot 4': None,
            'Slot 5': None,
            'Slot 6': None,
            'Slot 7': None,
            'Slot 8': None,
            'Slot 9': None,
            'Slot 10': None,
            'Slot 11': None,
            'Hero': Hero
        }

class Button(Syntax):
    def __init__(self):
        self.definitions = {}

class Event(Syntax):
    def __init__(self):
        self.definitions = {
            'Ongoing - Global': None,
            'Ongoing - Each Player': Tuple[Team, Players],
            'Player Earned Elimination': Tuple[Team, Players],
            'Player Dealt Final Blow': Tuple[Team, Players],
            'Player Dealt Damage': Tuple[Team, Players],
            'Player Took Damage': Tuple[Team, Players],
            'Player Died': Tuple[Team, Players]
        }
        self.aliases = {
            'Global': 'Ongoing - Global',
            'Each Player': 'Ongoing - Each Player',
            'On Kill': 'Player Earned Elimination',
            'On Final Blow': 'Player Dealt Final Blow',
            'On Damage': 'Player Dealt Damage',
            'On Damaged': 'Player Took Damage',
            'On Death': 'Player Died'
        }

class Array(Syntax):
    def __init__(self):
        self.definitions = {
            'All Players': Team
        }

class Value(Syntax):
    def __init__(self):
        self.definitions = {
            'Current Array Element': None,
            'Has Spawned': Entity,
            'Is True For All': Tuple[Array, Condition]
        }
        self.aliases = {
            'All True': 'Is True For All'
        }

class Action(Syntax):
    def __init__(self):
        self.definitions = {
            'Abort': None,
            'Abort If': Condition,
            'Abort If Condition Is False': None,
            'Abort If Condition Is True': None,
            'Allow Button': Tuple[Player, Button]
        }

Entity = Union[Value, Player] #Icon, Effect
Condition = Value
types = [Player, Team, Hero, Players, Event, Array, Value, Action]
type_names = [x.__name__.upper() for x in types]