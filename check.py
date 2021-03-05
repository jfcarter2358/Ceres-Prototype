import sys
import re
import uuid

meta_keys = [
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second",
    "service",
    "level",
    "timestamp"
]

query = sys.argv[1]

def check_query(query, meta_keys):
    paren_match = r'\([^\(\)]*\)'
    logic_match = r'(AND|OR|NOT|XOR|LIMIT|ORDERBY|ORDERDESC)'
    group_match = r'(%\S+|\S+\s?(?:=|<|>|<=|>=|IN)\s?\S+|(?:[a-zA-Z]|[0-9])+)'
    expression_match = r'(\S*)\s?(=|<|>|<=|>=|IN)\s?(\S*)'
    limit_match = r'LIMIT\s(\S*)'
    order_match = r'(?:ORDERBY|ORDERDESC)\s(\S*)'
    logic = ['AND', 'OR', 'XOR', 'NOT', 'LIMIT', 'ORDERBY', 'ORDERDESC']

    query = query.strip()

    if not query.startswith('SELECTBY') and not query.startswith('DELETEBY'):
        return 'query must start with "SELECTBY" or "DELETEBY"'

    # cleanup and format query
    query = query.replace('SELECTBY', '').strip()
    query = query.replace('DELETEBY', '').strip()
    query = re.sub(r'\((\S)', r'( \g<1>', query)
    query = re.sub(r'(\S)\(', r'\g<1> (', query)
    query = re.sub(r'(\S)\)', r'\g<1> )', query)
    query = re.sub(r'\)(\S)', r') \g<1>', query)
    query = '( ' + query + ' )'

    if query.count('(') != query.count(')'):
        return 'Parenthesis mismatch'

    while True:
        m = re.search(paren_match, query)

        if m == None:
            break

        text = m.group(0)

        m2 = re.findall(group_match, text)
        m2_expressions = [x for x in m2 if not x in logic]
        m2_logic = [x for x in m2 if x in logic]

        if len(m2_expressions) > 2:
            return 'Too many expressions in the group "{}"'.format(text)

        m3 = re.findall(logic_match, text)
        if len(m2_expressions) == 2:
            if len(m3) > 1:
                return 'Too many logic operations in the group "{}"'.format(text)
            if len(m3) == 0:
                return 'Not enough logic operations in the group "{}"'.format(text)
        else:
            if len(m3) > 0:
                return 'Too many logic operations in the group "{}"'.format(text)

        m2_logic.append('')

        for match in m2_expressions:
            m4 = re.search(expression_match, match)
            if m2_logic[0] == 'LIMIT':
                try:
                    int(m2_expressions[1])
                except:
                    return 'LIMIT operation requires an integer for the right hand side'
            elif m2_logic[0] == 'ORDERBY' or m2_logic[0] == 'ORDERDESC':
                if not m2_expressions[1] in meta_keys:
                    return '{} operations requires a valid index for the right hand side, not {}. Valid indices are: {}'.format(m2_logic[0], m2_expressions[1], meta_keys)
            else:
                if m4 == None:
                    return 'Expresssion "{}" is not valid'.format(match)
                if not m4.groups()[0] in meta_keys:
                    return '"{}" is not a valid index, valid indices are: {}'.format(m4.groups()[0], meta_keys)

        ident = str(uuid.uuid4())
        query = query.replace(text, '%' + ident)

    return None

print(check_query(query, meta_keys))