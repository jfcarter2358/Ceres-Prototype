import common
import utils

def get_data(id):
    group, block, offset, length = utils.extract_from_id(id)
    with open('{}/{}/{}'.format(common.CERES_HOME + "/data", group, block), "rb") as f:
        f.seek(common.BLOCK_SIZE * block + offset)
        data = f.read(length)
    return data.decode(common.DATA_ENCODING)