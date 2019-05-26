import json
with open('workshop.json') as f:
    data = json.load(f)

actions = {
    x.get('name'): {
        'description': x.get('description'),
        'args': x.get('args')
    } for x in data.get('actions')
}
values = {
    x.get('name'): {
        'description': x.get('description'),
        'args': x.get('args')
    } for x in data.get('values')
}
types = {}
for type_ in data.get('types'):
    key = type_.pop('name')
    value = {k: type_.get(k) for k in type_.keys()}
    types.update({key: value})