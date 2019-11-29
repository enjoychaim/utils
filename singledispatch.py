"""
单分派泛函数使用
"""
from functools import singledispatch, wraps


def dispatcher(func):
    __dispatcher = singledispatch(func)

    @wraps(func)
    def wrapper(*args, **kw):
        return __dispatcher.dispatch(args[1].__class__)(*args, **kw)

    wrapper.register = __dispatcher.register
    return wrapper


class TradeOrderForCreateOrderCmd:

    def execute(self, *args, **kwargs):
        print('TradeOrderForCreateOrder >>> execute ->', args, kwargs)


class TradeOrderFactory:

    @dispatcher
    def dispatch(self, class_, *args, **kwargs):
        print('dispatcher --->', class_, args, kwargs)

    @dispatch.register(TradeOrderForCreateOrderCmd)
    def create_order(self, class_, *args, **kwargs):
        class_.execute(*args, **kwargs)


if __name__ == '__main__':
    trade_order_factory = TradeOrderFactory()
    trade_order_factory.dispatch('default')
    trade_order_factory.dispatch(TradeOrderForCreateOrderCmd(), 1, 2, 3)
