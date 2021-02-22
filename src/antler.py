import re
import os
import sys
import uuid
import utils
import common
import exporter
from collections import namedtuple

AST = namedtuple('AST', 'operation left right')
NON_LOGIC_OPERATIONS = ['LIMIT', 'ORDERBY', 'ORDERDESC']

def parse(query):
    # perform cleanup on parens
    # replace all 'open paren -> text' with 'open paren -> space -> text'
    query = re.sub(r'\((\S)', r'( \g<1>', query)
    # replace all 'text -> open paren' with 'text -> space -> open paren'
    query = re.sub(r'(\S)\(', r'\g<1> (', query)
    # replace all `text -> close paren` with 'text -> space -> close paren'
    query = re.sub(r'(\S)\)', r'\g<1> )', query)
    # replace all `close paren -> text` with 'close paren -> space -> text'
    query = re.sub(r'\)(\S)', r') \g<1>', query)

    # add beginning and end braces to query
    query = '( ' + query + ' )'

    # initialize variables for parsing
    RE_PATTERN = r'\(\s(\S*\s?(?:=|>|>=|<=|<|!=|IN)\s?\S*|\S*)\s(AND|OR|NOT|XOR|LIMIT|ORDERBY|ORDERDESC)\s(\S*\s?(?:=|>|>=|<=|<|!=|IN)\s?\S*|\S*)\s\)'
    top_ast = AST('', '', '')
    asts = {}
    did_match = False

    while True:
        print(query)
        m = re.search(RE_PATTERN, query)

        # if there are no more matches then we've done the whole query string
        if m == None:
            break

        groups = m.groups()
        did_match = True

        # create the AST for the match
        new_ast = AST(groups[1], groups[0], groups[2])

        # replace it in the query string and add it to the map
        ident = '%' + str(uuid.uuid4()) + '%'
        asts[ident] = new_ast
        query = query.replace('( {} {} {} )'.format(groups[0], groups[1], groups[2]), ident, 1)
        top_ast = new_ast
        
    print(asts)

    if not did_match:
        out = parse_query(query[2:len(query) - 2])
        return out
    # out = None
    out = operate(top_ast, asts)
    return out

def parse_query(query):
    RE_PATTERN = r'(\S*)\s+(=|>|>=|<=|<|!=|IN)\s+(\S*)'
    m = re.search(RE_PATTERN, query)

    # need to add some error handling here
    groups = m.groups()
    out = []
    if groups[1] == 'IN':
        for r in groups[2].split(','):
            with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], r)) as f:
                idents = f.read().split('\n')
            out = utils.merge_lists(out, idents)
        return out
    elif groups[1] == '=':
        with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], groups[2])) as f:
            out = f.read().split('\n')
            return out
    elif groups[1] == '>':
        minor_idx = [f for f in os.listdir(common.CERES_HOME + '/indices/{}'.format(groups[0]))]
        for i in minor_idx:
            if _do_comparison(i, groups[2], '>'):
                with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], i)) as f:
                    idents = f.read().split('\n')
                out = utils.merge_lists(out, idents)
        return out
    elif groups[1] == '>=':
        minor_idx = [f for f in os.listdir(common.CERES_HOME + '/indices/{}'.format(groups[0]))]
        for i in minor_idx:
            if _do_comparison(i, groups[2], '>='):
                with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], i)) as f:
                    idents = f.read().split('\n')
                out = utils.merge_lists(out, idents)
        return out
    elif groups[1] == '<=':
        minor_idx = [f for f in os.listdir(common.CERES_HOME + '/indices/{}'.format(groups[0]))]
        for i in minor_idx:
            if _do_comparison(i, groups[2], '<='):
                with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], i)) as f:
                    idents = f.read().split('\n')
                out = utils.merge_lists(out, idents)
        return out
    elif groups[1] == '<':
        minor_idx = [f for f in os.listdir(common.CERES_HOME + '/indices/{}'.format(groups[0]))]
        for i in minor_idx:
            if _do_comparison(i, groups[2], '<'):
                with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], i)) as f:
                    idents = f.read().split('\n')
                out = utils.merge_lists(out, idents)
        return out
    minor_idx = [f for f in os.listdir(common.CERES_HOME + '/indices/{}'.format(groups[0]))]
    for i in minor_idx:
        if i != groups[2]:
            with open(common.CERES_HOME + '/indices/{}/{}'.format(groups[0], i)) as f:
                idents = f.read().split('\n')
            out = utils.merge_lists(out, idents)
    return out

def operate(ast, asts):
    global NON_LOGIC_OPERATIONS

    m = re.search(r'%\S*%', ast.left)
    if m:
        l = operate(asts[ast.left], asts)
    else:
        l = parse_query(ast.left)

    if not ast.operation in NON_LOGIC_OPERATIONS:
        m = re.search(r'%\S*%', ast.right)
        if m:
            r = operate(asts[ast.right], asts)
        else:
            r = parse_query(ast.right)
        if ast.operation == "AND":
            return _do_and(l, r)
        if ast.operation == "OR":
            return _do_or(l, r)
        if ast.operation == "NOT":
            return _do_not(l, r)
        if ast.operation == "XOR":
            return _do_xor(l, r)
        return None
    else:
        if ast.operation == "LIMIT":
            return _do_limit(l, int(ast.right))
        if ast.operation == "ORDERBY":
            return _do_orderby(l, ast.right)
        if ast.operation == "ORDERDESC":
            return _do_desorderby(l, ast.right)
        return None

def _do_and(A, B):
    out = []
    for i in range(0, len(A)):
        if len(B) == 0:
            break
        while B[0] < A[i]:
            B.pop(0)
            if len(B) == 0:
                break
        if len(B) > 0:
            if B[0] == A[i]:
                out.append(A[i])
    return out

def _do_or(A, B):
    out = []
    for i in range(0, len(A)):
        if len(B) == 0:
            out += A[i:]
            break
        while B[0] < A[i]:
            out.append(B[0])
            B.pop(0)
            if len(B) == 0:
                out += A[i:]
                break
        if len(B) > 0:
            if B[0] != A[i]:
                out.append(A[i])
    out += B
    return out

def _do_not(A, B):
    out = []
    for i in range(0, len(A)):
        if len(B) == 0:
            out += A[i:]
            break
        while B[0] < A[i]:
            B.pop(0)
            if len(B) == 0:
                out += A[i:]
                break
        if len(B) > 0:
            if B[0] != A[i]:
                out.append(A[i])
    return out

def _do_xor(A, B):
    out = []
    for i in range(0, len(A)):
        if len(B) == 0:
            out += A[i:]
            break
        while B[0] < A[i]:
            out.append(B[0])
            B.pop(0)
            if len(B) == 0:
                out += A[i:]
                break
        if len(B) > 0:
            if B[0] == A[i]:
                B.pop(0)
            else:
                out.append(A[i])
        else:
            out.append(A[i])
    out += B
    return out

def _do_limit(A, n):
    print('limit')
    return A[:n]

def _do_orderby(A, field):
    data = []
    for ident in A:
        d = _map_dict(exporter.get_data(ident), ident)
        data.append(d)
    data = sorted(data, key = lambda x: x[field])
    print(data)
    out = [x['id'] for x in data]
    return out

def _do_desorderby(A, field):
    data = []
    for ident in A:
        d = _map_dict(exporter.get_data(ident), ident)
        data.append(d)
    data = sorted(data, key = lambda x: x[field], reverse=True)

    out = [x['id'] for x in data]
    return out

def _do_comparison(l, r, op):
    try:
        real_l = float(l)
        real_r = float(r)
    except:
        real_l = l
        real_r = r
    if op == '>':
        return real_l > real_r
    if op == '>=':
        return real_l >= real_r
    if op == '<':
        return real_l < real_r
    if op == '<=':
        return real_l <= real_r
        
def _map_dict(datum, ident):
    data = datum.split(',')
    out = {'id': ident}
    for i in range(0, len(common.SCHEMA['order'])):
        out[common.SCHEMA['order'][i]] = data[i]
    return out

if __name__ == '__main__':
    print(parse(sys.argv[1]))