def display_rmb(fen: int):
    """把 分 为单位的金额显示为 元, 并保留2位小数

    Args:
      fen: 单位为分的整数
    """
    return round(float(fen) / 100, 2)
