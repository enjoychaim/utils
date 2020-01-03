"""
基于c的deque实现的queue
    1. not_empty, not_full, all_task_done三个共享锁
    2. PriorityQueue和LifoQueue均基于queue实现
"""

import queue

if __name__ == '__main__':
    q = queue.Queue()

    for i in range(5):
        q.put(i)

    while not q.empty():
        print(q.get(), end=' ')

    print()
