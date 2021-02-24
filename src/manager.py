import common
import utils

def delete_data(id, free_data):
    group, block, offset, length = utils.extract_from_id(id)
    with open('{}/{}/{}'.format(common.CERES_HOME + "/data", group, block), "r+b") as f:
        f.seek(common.BLOCK_SIZE * block + offset)
        f.write('\x00'.encode(common.DATA_ENCODING) * length)
    free_data[group][block].append({'start': offset, 'end': offset + length})
    return free_data

def merge_free(free_data):
    for group in range(0, len(free_data)):
        for block in range(0, len(free_data[group])):
            data = sorted(free_data[group][block], key = lambda x: x['start'])
            i = 1
            while i < len(data):
                if data[i - 1]['end'] == data[i]['start']:
                    data[i - 1]['end'] = data[i]['end']
                    del data[i]
                else:
                    i += 1
            free_data[group][block] = data
    return free_data
                