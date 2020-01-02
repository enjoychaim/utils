def encode(str_):
    """编码"""
    return ' '.join([bin(ord(c)).replace('0b', '') for c in str_])


def decode(str_):
    """解码"""
    return ''.join([chr(i) for i in [int(b, 2) for b in str_.split(' ')]])
