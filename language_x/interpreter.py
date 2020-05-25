import heapq
# from termcolor import colored
from AST import *
import monotonic; 
mtime = monotonic.time.time

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
    callback = None
    def __init__(self, func, callback):
        self.func = func
        self.callback = callback
    def is_finished(self):
        return self._pc >= len(self.func.sequence)
    def run(self, stack, queue):
        while not self.is_finished():
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
                # f()
                stack.extend([Frame(command.func, None) for x in range(command.loop)])
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
        
def run_event_loop(main_function):
    print('>>>>>>>>>>>>>>>Running')
    start_time = mtime()

    # call stack: Frame
    stack = []
    # event queue: SleepTask
    queue = []
    stack.append(Frame(main_function, None))
    running_time = 0
    sleep_time = 0
    while stack or queue:
        while not stack:
            current_time = mtime()
            if queue[0].when <= current_time:
                sleep_task = queue.pop(0)
                # heapq.heappop(queue)
                stack.append(sleep_task.callback)
            else:
                # print('going to sleep for ' + str(queue[0].when - current_time))
                time.sleep(queue[0].when - current_time)
                sleep_time += queue[0].when - current_time

        while stack:
            frame = stack[-1]
            start = mtime()
            # print('run stack:', frame)
            frame.run(stack, queue)
            running_time += (mtime() - start)

    print('<<<<<<<<<<Program finished, duration: ' + str(mtime() - start_time))
    print('<<<<<<<<<<Acutal running time: ' + str(running_time))
    print('<<<<<<<<<<Acutal sleep time: ' + str(sleep_time))



        

