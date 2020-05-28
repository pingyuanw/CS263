import heapq
# from termcolor import colored
from AST import *
import monotonic; 
mtime = monotonic.time.time
from multiprocessing import Process



# from rpython.rlib import jit

# def printable_loc(pc, frame):
#     return str(pc)

# driver = jit.JitDriver(greens = ['pc', 'frame'],
#                        reds = ['stack', 'queue'],
#                        get_printable_location=printable_loc)

class SleepTask:
    def __init__(self, duration, callback):
        self.when = mtime() + duration
        self.callback = callback
        # print('new SleepTask:' + str(duration))
    def __lt__(self, other):
        return self.when < other.when
class Frame:
    _pc = 0
    _loop = 0
    func = None
    callback = None
    def __init__(self, func, callback):
        self.func = func
        self.callback = callback
    def is_finished(self):
        return self._pc >= len(self.func.sequence)
    def run(self, stack, queue):
        while not self.is_finished():
            # required hint indicating this is the top of the opcode dispatch
            # driver.jit_merge_point(pc=self._pc, frame=self, stack=stack, queue=queue)

            command = self.func.sequence[self._pc]
            self._pc += 1

            # await 1
            if isinstance(command, AwaitSleep):
                stack.pop()
                i = 0
                newtask = SleepTask(command.target, self)
                for task in queue:
                    if newtask.when < task.when:
                        break
                    i += 1
                queue.insert(i, newtask)
                # heapq.heappush(queue, SleepTask(command.target, self))
                return
            # await f()
            elif isinstance(command, AwaitAnother):
                stack.pop()
                stack.append(Frame(command.target.func, self))
                return
            elif isinstance(command, ApplyFunc):
                # f():5
                stack.extend([Frame(command.func, None) for x in range(command.loop)])

                # required hint indicating this is the end of a loop
                # driver.can_enter_jit(pc=self._pc, frame=self, stack=stack, queue=queue)
                return
            elif isinstance(command, Print):
                # print('xxx')
                # print(colored(self.func.name + ':', 'blue') + command.arg)
                print(self.func.name + ':' + command.arg)

            else:
                print('wrong command in function:', self.func.name)
                raise NotImplementedError

        # frame finish funning
        stack.pop()
        # schedule callback waiting on it
        if self.callback:
            stack.append(self.callback)
   
def run(main_function):
    # call stack: Frame
    stack = []
    # event queue: SleepTask
    queue = []
    stack.append(Frame(main_function, None))

    start_time = mtime()

    run_event_loop(stack, queue)

    print('<<<<<<<<<<Program finished, duration: ' + str(mtime() - start_time))

def run_event_loop(stack, queue):

    # flag = len(stack)
    # print('>>>>>>>>>>>>>>>New Event Loop Running:', len(stack))
    # start_time = mtime()
    # running_time = 0
    # sleep_time = 0
    # queue_time = 0

    children = []
    while stack or queue:
        while not stack:
            current_time = mtime()
            if queue[0].when <= current_time:
                i = 0
                for task in queue:
                    if task.when > current_time:
                        break
                    stack.append(task.callback)
                    i += 1

                queue = queue[i:]
                # queue_time += (mtime() - current_time)
            else:
                # print('going to sleep for ' + str(queue[0].when - current_time))
                time.sleep(queue[0].when - current_time)
                # sleep_time += queue[0].when - current_time
        
        start = mtime()
        while stack:
            if len(stack) > 5000:
                pivot = len(stack)/2
                another_stack = stack[pivot:]
                stack = stack[0:pivot]
                p = Process(target=run_event_loop, args=(another_stack,[]))
                children.append(p)
                p.start()

            frame = stack[-1]
            # print('run stack:', frame)
            frame.run(stack, queue)
        # running_time += (mtime() - start)

    for p in children:
        p.join()

    # print('<<<<<<<<<<<:'+str(flag))
    # print('<<<<<<<<<<Program finished, duration: ' + str(mtime() - start_time))
    # print('<<<<<<<<<<Acutal running time: ' + str(running_time))
    # print('<<<<<<<<<<Acutal sleep time: ' + str(sleep_time))
    # print('<<<<<<<<<<Queue time: ' + str(queue_time))




        

