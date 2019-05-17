import logging
import pandas as pd
from tqdm import tqdm
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.sql.expression import ClauseElement


def sql2df(dsn_or_engin: [str, Engine],
           sql: [ClauseElement, str],
           debug: bool = False,
           chunksize: int = None,
           **kwargs):
  """Generate DataFrame from sql result"""
  if isinstance(dsn_or_engin, str):
    # Use server side cursors  by passing server_side_cursors=True
    engine = create_engine(dsn_or_engin, server_side_cursors=True)
  else:
    engine = dsn_or_engin
  if debug:
    logging.info(sql.compile(engine, compile_kwargs={'literal_binds': True}))
  with engine.connect() as conn:
    if chunksize:
      frames = pd.read_sql(sql, conn, chunksize=chunksize, **kwargs)
      data = [i for i in frames]
      if data:
        return pd.concat(data)
    return pd.read_sql(sql, conn, **kwargs)


def iter_2_df(iterator,
              chunk_size: int = 0,
              func=None,
              **kwargs) -> pd.DataFrame:
  """Turn an Mongo iterator into multiple small pandas.DataFrame

  This is a balance between memory and efficiency
  If no result, return empty pandas.DataFrame

  Args:
    iterator: an iterator
    chunk_size: the row size of each small pandas.DataFrame, 0 means no chunk
    func: generator to transform each record
    kwargs: extra parameters passed to tqdm.tqdm
  Returns:
    pandas.DataFrame
  """
  records = []
  frames = []
  for i, record in enumerate(tqdm(iterator, **kwargs)):
    if func:
      for new_record in func(record):
        records.append(new_record)
    else:
      records.append(record)
    if chunk_size and (i % chunk_size == chunk_size - 1):
      frames.append(pd.DataFrame(records))
      records = []
  if records:
    frames.append(pd.DataFrame(records))
  frames = pd.concat(frames) if frames else pd.DataFrame()
  return frames
