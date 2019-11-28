"""
线程执行过程:
    1. __init__
    2. args | kwargs | task
    3. start
    4. run
    5. join
    6. result
"""
import logging
import threading
import time
from enum import Enum


class ThreadState(Enum):
    INIT = 1
    RUNNING = 2
    SUCCESS = 3
    FAILED = 4


class CustomThread(threading.Thread):
    def __init__(self, name=None, task=None, args=(), kwargs=None):
        super().__init__(name=name, target=self.run, args=args, kwargs=kwargs)
        self.state = ThreadState.INIT
        self._task = task
        self._result = None

    @property
    def args(self) -> tuple:
        return self._args

    @args.setter
    def args(self, args_):
        self._args = args_

    @property
    def kwargs(self) -> dict:
        return self._kwargs

    @kwargs.setter
    def kwargs(self, kwargs_):
        self._kwargs = kwargs_

    @property
    def task(self):
        if self._task is None:
            result = None
        elif self.args and self.kwargs:
            result = self._task(*self.args, **self.kwargs)
        elif self.args:
            result = self._task(*self.args)
        elif self.kwargs:
            result = self._task(**self.kwargs)
        elif self._task:
            result = self._task()
        return lambda: result

    @task.setter
    def task(self, object_, *args_, **kwargs_):
        self._task = object_
        if args_:
            self.args = args_
        if kwargs_:
            self.kwargs = kwargs_

    @property
    def result(self):
        return self._result

    def run(self) -> None:
        try:
            self.state = ThreadState.RUNNING

            logging.info(f"[{self.ident}] {self.name} start run")
            print(f"[{self.ident}] {self.name} start run")

            self._result = self.task()

            logging.info(f"[{self.ident}] {self.name} finish")
            print(f"[{self.ident}] {self.name} finish")

            self.state = ThreadState.SUCCESS
        except Exception as e:
            self.state = ThreadState.FAILED
            logging.exception(e)

    def is_finish(self):
        return self.state == ThreadState.SUCCESS

def task_mul(x, y):
    time.sleep(3)
    return x * y


def task_add(x, y):
    return x + y


if __name__ == '__main__':
    mul_ = CustomThread(name='mul_', task=task_mul, args=(1, 2))
    mul_.start()

    add_ = CustomThread(name='add_')
    add_.task = lambda x, y: x + y
    add_.args = 1, 2
    add_.start()

    mul_.join()
    add_.join()

    print(mul_.name)
    print(mul_.result)

    print(add_.name)
    print(add_.result)
