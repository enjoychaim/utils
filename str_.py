def str_bool(input_str: str) -> bool:
    """Return True if the string representation indicates true values"""
    return input_str.lower() in ['true', 't', 'yes', 'y']


def float_comma(input_str: str) -> list:
    """Return comma separated string as list of float"""
    return [float(i) for i in input_str.split(',')]


def int_comma(input_str: str) -> list:
    """Return comma separated string as list of int"""
    return [int(i) for i in input_str.split(',')]
