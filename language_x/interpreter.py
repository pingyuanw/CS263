import heapq
# from termcolor import colored
from AST import *
import monotonic; 
mtime = monotonic.time.time
from multiprocessing import Process, Queue
from Queue import Empty



# from rpython.rlib import jit

# def printable_loc(pc, frame):
#     return str(pc)

# driver = jit.JitDriver(greens = ['pc', 'frame'],
#                        reds = ['stack', 'queue'],
#                        get_printable_location=printable_loc)

class Counter:
    count = 0
    def __init__(self, count):
        self.count = count
    def decrease(self):
        self.count -= 1
    def is_done(self):
        return self.count == 0
class SleepTask:
    def __init__(self, duration, callback):
        self.when = mtime() + duration
        self.callback = callback
        # print('new SleepTask:' + str(duration))
    def __lt__(self, other):
        return self.when < other.when
class Frame:
    _pc = 0

    func = None
    callback_hash = None
    def __init__(self, func, callback_hash):
        self.func = func
        self.callback_hash = callback_hash
    def is_finished(self):
        return self._pc >= len(self.func.sequence)
    def run(self, loop):
        while not self.is_finished():
            # required hint indicating this is the top of the opcode dispatch
            # driver.jit_merge_point(pc=self._pc, frame=self, stack=stack, queue=queue)

            command = self.func.sequence[self._pc]
            self._pc += 1

            # await 1
            if isinstance(command, AwaitSleep):
                loop.stack.pop(0)

                newtask = SleepTask(command.target, self)
                loop.add_sleep_task(newtask)
                return
            # await f():5
            elif isinstance(command, AwaitAnother):
                loop.stack.pop(0)
                apply_node = command.target
                loop.add_counter(self, apply_node.loop)
                loop.stack.extend([Frame(apply_node.func, hash(self)) for x in range(apply_node.loop)])
                return
            elif isinstance(command, ApplyFunc):
                # f():5
                loop.stack.extend([Frame(command.func, None) for x in range(command.loop)])

                # required hint indicating this is the end of a loop
                # driver.can_enter_jit(pc=self._pc, frame=self, stack=stack, queue=queue)
                return
            elif isinstance(command, Print):
                # print('xxx')
                # print(colored(self.func.name + ':', 'blue') + command.arg)
                print(self.func.name + ':' + command.arg)
            elif isinstance(command, Compute):
                x = 1
                for i in range(command.arg):
                    x = x*i
            else:
                print('wrong command in function:', self.func.name)
                raise NotImplementedError

        # frame finish funning
        loop.stack.pop(0)
        # schedule callback waiting on it
        if self.callback_hash:
            loop.receive_hash(self.callback_hash)
   
def run(main_function):
    start_time = mtime()

    run_event_loop([Frame(main_function, None)], None, 0)

    # print('<<<<<<<<<<Program finished, duration: ' + str(mtime() - start_time))
    print(mtime() - start_time)

def run_event_loop(stack, pipe, id):
    event_loop = EventLoop(stack, pipe, id)
    event_loop.run()

class EventLoop:
    id = 0
    # call stack: Frame
    stack = []
    # event queue: SleepTask
    queue = []
    # await counters: {hash: (frame, count)}
    counters = {}
    pipe = None
    # child process: (process, pipe_queue)
    children = []
    def __init__(self, stack, pipe, id):
        self.stack = stack
        self.pipe = pipe
        self.queue = []
        self.counters = {}
        self.children = []
        self.id = id
    def add_sleep_task(self, newtask):
        # print('add sleep task')
        i = 0
        for task in self.queue:
            if newtask.when < task.when:
                break
            i += 1
        self.queue.insert(i, newtask)

    def add_counter(self, callback, count):
        if hash(callback) in self.counters:
            raise Exception("!!!!!!")
        self.counters[hash(callback)] = (callback, count)
        # print('add counter:', self.id, hash(callback))

    def receive_hash(self, v):
        # print('receive_hash', self.id, v)
        if v in self.counters:
            frame, count = self.counters[v]
            count -= 1
            if count == 0:
                self.stack.append(frame)
                del self.counters[v]
            else:
                self.counters[v] = (frame, count)
            # print(count)
        else:
            self.pipe.put_nowait(v)
    def run(self):
        # flag = len(stack)
        # print('>>>>>>>>>>>>>>>New Event Loop Running:', self.id, len(self.stack))
        start_time = mtime()
        # running_time = 0
        # sleep_time = 0
        # queue_time = 0

        while self.stack or self.queue or self.counters:
            # start = mtime()
            while self.stack:
                # print(len(self.stack))
                if len(self.stack) > 15:
                    pivot = len(self.stack)/2
                    another_stack = self.stack[pivot:]
                    self.stack = self.stack[0:pivot]

                    q = Queue()
                    p = Process(target=run_event_loop, args=(another_stack, q, self.id+1))
                    self.children.append((p, q))
                    p.start()

                frame = self.stack[0]
                # print('run stack:', frame)
                frame.run(self)
            # running_time += (mtime() - start)

            # check await callback
            # print(v for v in self.counters)
            # start = mtime()
            for p, q in self.children:
                while not q.empty():
                    hash_v = q.get_nowait()
                    self.receive_hash(hash_v)
            # print('read pipe time:' + str(mtime() - start))
                # try:
                #     hash_v = q.get_nowait()
                #     self.receive_hash(hash_v)
                # except Empty:
                #     pass
            # check event queue
            if self.queue:
                current_time = mtime()
                if self.queue[0].when <= current_time:
                    i = 0
                    for task in self.queue:
                        if task.when > current_time:
                            break
                        self.stack.append(task.callback)
                        i += 1

                    self.queue = self.queue[i:]
                    # queue_time += (mtime() - current_time)
                # else:
                #     print('going to sleep for ' + str(self.queue[0].when - current_time))
                #     time.sleep(self.queue[0].when - current_time)
                    # sleep_time += self.queue[0].when - current_time

        # print('wait for children')
        while self.children:
            for p, q in self.children:
                if not q.empty():
                    hash_v = q.get_nowait()
                    self.receive_hash(hash_v)
                else:
                    p.join(timeout=0)
                    if not p.is_alive():
                        self.children.remove((p,q))

        # print('<<<<<<<<<<<:'+str(flag))
        # print('<<<<<<<<<<Event Loop End', self.id, ' duration: ' + str(mtime() - start_time))
        # print('<<<<<<<<<<Acutal running time: ' + str(running_time))
        # print('<<<<<<<<<<Acutal sleep time: ' + str(sleep_time))
        # print('<<<<<<<<<<Queue time: ' + str(queue_time))




        

