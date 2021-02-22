import common

def get_data(id):
    group, block, offset, length = _extract_from_id(id)
    with open('{}/{}/{}'.format(common.CERES_HOME + "/data", group, block), "rb") as f:
        f.seek(common.BLOCK_SIZE * block + offset)
        data = f.read(length)
    return data.decode(common.DATA_ENCODING)

def _extract_from_id(id):
    parts = id.split(':')
    return int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])