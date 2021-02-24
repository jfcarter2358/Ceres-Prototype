import common
import index
import os

import time

def get_writable(data, free_data, meta):
    encoded_data = data.encode(common.DATA_ENCODING)
    length = len(encoded_data)
    if common.INSERT_STRATEGY == 'first':
        for g in free_data:
            for b in free_data[g]:
                for i in range(0, len(free_data[g][b])):
                    if free_data[g][b][i]['end'] - free_data[g][b][i]['start'] < length:
                        continue
                    if free_data[g][b][i]['end'] - free_data[g][b][i]['start'] > length:
                        ident = _do_write(encoded_data, g, b, free_data[g][b][i]['start'], length)
                        index.handle_index_add(ident, meta)
                        free_data[g][b][i]['start'] += length
                        return free_data, ident
                    ident = _do_write(encoded_data, g, b, free_data[g][b][i]['start'], length)
                    index.handle_index_add(ident, meta)
                    del free_data[g][b][i]
                    return free_data, ident
    raise ValueError("No space left in database")

def _do_write(data, group, block, offset, length):
    _check_dirs(group, block)
    with open('{}/{}/{}'.format(common.CERES_HOME + "/data", group, block), "r+b") as f:
        f.seek(int(common.BLOCK_SIZE) * int(block) + int(offset))
        f.write(data)

    pad_len = len(str(common.BLOCK_SIZE))
    group_pad_len = len(str(common.MAX_GROUPS))
    block_pad_len = len(str(common.MAX_BLOCKS))
    return str(group).zfill(group_pad_len) + ":" + str(block).zfill(block_pad_len) + ":" + str(offset).zfill(pad_len) + ":" + str(length).zfill(pad_len)

def _check_dirs(group, block):
    if not os.path.exists('{}/{}'.format(common.CERES_HOME + "/data", group)):
        os.mkdir('{}/{}'.format(common.CERES_HOME + "/data", group))
    if not os.path.exists('{}/{}/{}'.format(common.CERES_HOME + "/data", group, block)):
        with open('{}/{}/{}'.format(common.CERES_HOME + "/data", group, block), 'w') as f:
            f.write('')