"""
线程执行过程:
    1. __init__
    2. args | kwargs | task
    3. start
    4. run
    5. join
    6. result
线程池执行过程:
    1. add_task, 添加任务(线程对应: args | kwargs | task)
    2. run_task, 执行任务(线程对应: start)
    3. get_result, 获取结果(线程对应: result)
"""
import time
from queue import Queue

from thread_ import CustomThread


class ThreadPool:
    def __init__(self, pool_size=100):
        self.pool = []
        self.pool_size = pool_size
        self.queue = Queue()

    def add_task(self, task, *args, **kwargs):
        """添加任务"""
        if len(self.pool) < self.pool_size:
            self.pool.append(self._init_thread(task, *args, **kwargs))
        else:
            self.queue.put_nowait({'task': task, 'args': args, 'kwargs': kwargs})

    def _init_thread(self, task, *args, **kwargs):
        return CustomThread(name=task.__name__, task=task, args=args, kwargs=kwargs)

    def run_task(self):
        """执行任务"""
        # TODO: 可考虑使用contextlib.contextmanager实现上个线程结束之后立即从队列中获取新任务
        while self.pool:
            self._start_task()
            self._wait_task_finish()
            if not self.queue.empty():
                item = self.queue.get_nowait()
                task = item['task']
                args = item['args']
                kwargs = item['kwargs']
                self.add_task(task, *args, **kwargs)

    def _start_task(self):
        for thread_ in self.pool:
            thread_.start()

    def _wait_task_finish(self):
        for thread_ in self.pool:
            thread_.join()
        self.pool_finish = self.pool
        self.pool = []

    def get_result(self):
        """获取任务执行结果"""
        return [thread_.result for thread_ in self.pool_finish]


def task_mul(x, y):
    time.sleep(3)
    return x * y


def task_add(x, y):
    return x + y


if __name__ == '__main__':
    thread_pool = ThreadPool(2)
    thread_pool.add_task(task_mul, 1, 2)
    thread_pool.add_task(task_add, 1, 2)
    thread_pool.add_task(task_add, 3, 4)
    thread_pool.run_task()
    result = thread_pool.get_result()
    print(result)
