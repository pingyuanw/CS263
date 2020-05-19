import heapq
import time
from termcolor import colored

class Function:
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = [Print(colored('start', 'yellow'))] + sequence + [Print(colored('end', 'yellow'))]
class ApplyFunc:
    def __init__(self, func, version):
        self.func = func
        self.version = version
class Await:
    def __init__(self, target):
        self.target = target
class Print:
    def __init__(self, arg):
        self.arg = arg
class SleepTask:
    def __init__(self, duration, callback):
        self.when = time.monotonic() + duration
        self.callback = callback
        print('new SleepTask:', duration)
    def __lt__(self, other):
        return self.when < other.when
class Frame:
    _pc = 0
    _func = None
    _version = None
    callback = None
    def __init__(self, func, version, callback):
        self._func = func
        self._version = str(version)
        self.callback = callback
    def is_finished(self):
        return self._pc >= len(self._func.sequence)
    def run(self, stack, queue):
        while not self.is_finished():
            command = self._func.sequence[self._pc]
            self._pc += 1

            command_type = type(command)
            if command_type == Await:
                stack.pop()
                # await f()
                if type(command.target) == ApplyFunc:
                    stack.append(Frame(command.target.func, command.target.version, self))
                # await 1
                else:
                    heapq.heappush(queue, SleepTask(command.target, self))
                return
            elif command_type == ApplyFunc:
                # f()
                stack.append(Frame(command.func, command.version, None))
                return
            elif command_type == Print:
                # print('xxx')
                print(colored(self._func.name + self._version, 'blue'), command.arg)
            else:
                print('wrong command in function:', self._func.name)
        stack.pop()
        if self.callback:
            stack.append(self.callback)
        
def run_event_loop(main_function):
    # call stack: Frame
    stack = []
    # event queue: SleepTask
    queue = []
    stack.append(Frame(main_function, '', None))
    while stack or queue:
        while not stack:
            current_time = time.monotonic()
            if queue[0].when <= current_time:
                sleep_task = heapq.heappop(queue)
                stack.append(sleep_task.callback)
            else:
                time.sleep(queue[0].when - current_time)

        while stack:
            frame = stack[-1]
            print('run stack:', frame)
            frame.run(stack, queue)

    print('program finished')
 
g = Function('g', [Await(2)])

f = Function('f', [Await(ApplyFunc(g, 2)), Await(1)])

main_node = Function('main', [Await(ApplyFunc(g, 1)), ApplyFunc(f, 1)])

run_event_loop(main_node)

        

