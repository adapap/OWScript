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

if __name__ == '__main__':
    reserved_list = []
    reserved_list.extend([(x, 'ACTION') for x in actions])
    reserved_list.extend([(x, 'VALUE') if values.get(x).get('args') else (x, 'CONST') for x in values])
    reserved_list.extend([(x, 'CONST') for x in types.get('EVENT').get('values')])
    reserved_list.extend([(x, 'VALUE') for x in types.get('NUMBER').get('values')])
    reserved_list.extend([(x, 'CONST') for x in types.get('EFFECT REEVALUATION').get('values')])
    reserved_list.extend([(x, 'CONST') for x in types.get('LOS CHECK').get('values')])
    reserved_list.extend([(x, 'CONST') for x in types.get('COLOR').get('values')])
    reserved_list.extend([(x, 'CONST') for x in types.get('CREATE EFFECT').get('values')])
    reserved = dict(reserved_list)
    aliases = {
        'ALL TRUE': 'IS TRUE FOR ALL',
        'ON GLOBAL': 'ONGOING - GLOBAL',
        'ON EACH PLAYER': 'ONGOING - EACH PLAYER',
        'PLAYERS IN RADIUS': 'PLAYERS WITHIN RADIUS',
        'ROUND': 'ROUND TO INTEGER',
        'SIN': 'SINE FROM DEGREES',
        'SINR': 'SINE FROM RADIANS',
        'COS': 'COSINE FROM DEGREES',
        'COSR': 'COSINE FROM RADIANS'
    }

    # for k, v in sorted(reserved.items(), key=lambda x: (x[1], x[0])):
    #     print(f"('{k}', '{v}'),")
    for x in sorted([k for k, v in reserved.items() if v == 'ACTION'], key=lambda x: x):
        print(f"| '{x}',")