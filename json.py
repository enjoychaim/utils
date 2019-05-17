import enum
import zlib
from datetime import datetime

import numpy as np
import simplejson as json
from aiomysql.sa.result import RowProxy

from const import datetime as datetime_cosnt


def parse(x):
  """Overwrite json parser to support extra value types"""
  if isinstance(x, np.integer):
    return int(x)
  if isinstance(x, RowProxy):
    return dict(x)
  if isinstance(x, datetime):
    return x.strftime(datetime_cosnt.PYTHON_DATETIME_FORMAT)
  if isinstance(x, enum.Enum):
    return x.value
  raise TypeError('Unsupported type {}, value {}'.format(type(x), x))


def dumps(obj, *args, **kwargs):
  """Extend json.dumps to use customized parser by default"""
  kwargs.pop('default', None)
  kwargs.pop('ignore_nan', None)
  kwargs.pop('separators', None)
  return json.dumps(obj,
                    *args,
                    default=parse,
                    ignore_nan=True,
                    separators=(',', ':'),
                    **kwargs)


def encode(obj, *args, compress: bool = False, separators=(',', ':'), **kwargs):
  """Support compression on json string"""
  json_str = (json
              .dumps(obj, *args, ignore_nan=True, default=parse,
                     separators=separators, **kwargs)
              .replace('</', '<\\/'))
  if compress:
    return zlib.compress(json_str.encode())
  return json_str


def decode(json_str, compress: bool = False):
  """Support decompression from json string"""
  if compress:
    json_str = zlib.decompress(json_str).decode()
  return json.loads(json_str)


decoder = json.decoder
loads = json.loads
JSONDecodeError = json.JSONDecodeError
