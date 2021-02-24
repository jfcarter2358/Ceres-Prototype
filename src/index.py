import common
import os

def handle_index_add(ident, index_keys):
    _check_dirs(index_keys)
    for k in index_keys:
        insert_ident(ident, k)
    insert_ident(ident, 'all')

def insert_ident(ident, index):
    with open(common.CERES_HOME + '/indices/' + index) as f:
        ident_list = f.read().split('\n')
    ident_list = add_ident(ident, ident_list)
    if ident_list[0] == '':
        del ident_list[0]
    with open(common.CERES_HOME + '/indices/' + index, 'w') as f:
        f.write('\n'.join(ident_list))

def add_ident(ident, idents):
    if len(idents) == 0:
        return []
    pivot = int(len(idents) / 2)
    if pivot == 0:
        if idents[pivot] == ident:
            return idents
        if idents[pivot] < ident:
            return idents + [ident]
        return [ident] + idents
    
    if idents[pivot - 1] <= ident:
        if idents[pivot] > ident:
            return idents[:pivot] + [ident] + idents[pivot:]
        return idents[:pivot] + add_ident(ident, idents[pivot:])
    return add_ident(ident, idents[:pivot]) + idents[pivot:]

def _check_dirs(indices):
    if not os.path.exists('{}/indices'.format(common.CERES_HOME)):
        os.mkdir('{}/indices'.format(common.CERES_HOME))
    if not os.path.exists('{}/indices/all'.format(common.CERES_HOME)):
        with open('{}/indices/all'.format(common.CERES_HOME), 'w') as f:
            f.write('')
    for idx in indices:
        parts = idx.split('/')
        if not os.path.exists('{}/indices/{}'.format(common.CERES_HOME, parts[0])):
            os.mkdir('{}/indices/{}'.format(common.CERES_HOME, parts[0]))
        if not os.path.exists('{}/indices/{}/{}'.format(common.CERES_HOME, parts[0], parts[1])):
            with open('{}/indices/{}'.format(common.CERES_HOME, idx), 'w') as f:
                f.write('')