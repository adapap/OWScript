import json

try:
    from .AST import *
except ImportError:
    from AST import *

class WorkshopData:
    """Manager for workshop type data."""
    def __init__(self):
        try:
            with open('Workshop.json') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            with open('OWScript/Workshop.json') as f:
                self.data = json.load(f)

    def _gettype(self, type_):
        """Returns a WorkshopType object containing data about the argument."""
        if type_ == 'ANY':
            return Any
        for key in self.data.get('types'):
            if key.get('name') == type_:
                name = type_.title().replace(' ', '')
                return globals().get(name)

    def __getitem__(self, item):
        """Returns the instance of the class from the specified Event/Action/Value."""
        for data_type, data_list in self.data.items():
            if data_type in ('events', 'types'):
                continue
            for key in data_list:
                if key.get('name') == item:
                    name = item
                    description = key.get('description')
                    _args = key.get('args', [])
                    if not _args:
                        return Constant(name=item)
                    args = [self._gettype(arg.get('type')) for arg in key.get('args', [])]
                    node = OWID(name=name, description=description, args=args)
                    return node
        return Constant(name=item)
Workshop = WorkshopData()
# types_ = Workshop.data.get('types')
# print([x.get('name') for x in types_])
# for type_ in types_:
#     extends = ', '.join(map(lambda x: ''.join(x.title().split()), type_.get('extends', [])))
#     values = '_values = {}'.format(type_.get('values', []))
#     name = ''.join(type_.get('name').title().split())
#     string = f"""class {name}(WorkshopType):
#     {values}
#     _extends = [{extends}]
# """
#     print(string)