"""
列表操作相关
"""
import itertools


def chunk(iterable, iter_size, is_fill=False, filler=None):
    """
    迭代块访问
    :param iterable: 可迭代对象
    :param iter_size: 每次迭代大小
    :param is_fill: 切块不够, 是否填充
    :param filler: 填充对象
    """
    fill_size = iter_size - 1 if is_fill else 0
    it = itertools.chain(iterable, itertools.repeat(filler, fill_size))
    chunk = tuple(itertools.islice(it, iter_size))
    while 0 < len(chunk) <= iter_size:
        yield chunk
        chunk = tuple(itertools.islice(it, iter_size))


def grouped(iterable, n):
    """s -> (s0,s1,s2,...sn-1),
            (sn,sn+1,sn+2,...s2n-1),
            (s2n,s2n+1,s2n+2,...s3n-1),
            ...
    """
    return zip(*[iter(iterable)] * n)
