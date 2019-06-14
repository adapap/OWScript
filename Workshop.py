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
    reserved_list.extend([(x, 'VALUE') for x in types.get('NUMBER').get('values')])
    const_types = ['EVENT', 'EFFECT REEVALUATION', 'HUD TEXT REEVALUATION', 'WORLD TEXT REEVALUATION',
    'CHASE RATE REEVALUATION', 'CHASE TIME REEVALUATION', 'OBJECTIVE DESCRIPTION REEVALUATION', 'DAMAGE MODIFICATION REEVALUATION',
    'WAIT BEHAVIOR', 'LOS CHECK', 'COLOR', 'HERO CONSTANT', 'CREATE EFFECT']
    for const_type in const_types:
        reserved_list.extend([(x, 'CONST') for x in types.get(const_type).get('values')])
    reserved = dict(reserved_list)
    reserved['ALL'] = 'CONST'
    del reserved['AND']
    del reserved['OR']
    del reserved['NOT']
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
    items = sorted(sorted([k for k, v in reserved.items() if v == 'ACTION']), key=len, reverse=True)
    print("|".join(items))