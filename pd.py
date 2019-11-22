def iter_dataframe_by_chunk(df, chunk=1):
    """Iterate DataFrame as DataFrame"""
    for i in range(0, df.shape[0], chunk):
        yield df[i:i + chunk]
