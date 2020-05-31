import time
# from termcolor import colored

class Node(object):
    """ The abstract AST node
    """


class Function(Node):
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence

        # self.sequence = [Print('start')] + sequence + [Print('end')]

        # self.sequence = [Print(colored('start', 'yellow'))] + sequence + [Print(colored('end', 'yellow'))]
    def _bytecode(self):
        _list = []
        for command in self.sequence:
            _list.append(command._bytecode())
        return _list

    def _print(self, indent=0):
        print(' '*indent + '| ' + str(self.name))
        for x in self.sequence:
            x._print(indent+1)

class ApplyFunc(Node):
    def __init__(self, func, loop):
        self.func = func
        self.loop = loop
    def _bytecode(self):
        return 'APPLY'
    def _print(self, indent=0):
        print(' '*indent + '| ' + str(self.func.name) + '('+str(self.loop)+')')

class AwaitSleep(Node):
    def __init__(self, target):
        self.target = target
    def _print(self, indent=0):
        print(' '*indent + '| await ' + str(self.target))

class AwaitAnother(Node):
    def __init__(self, target):
        self.target = target
    def _print(self, indent=0):
        print(' '*indent + '| await ' + str(self.target.func.name) + '('+str(self.target.loop)+')')

class Print(Node):
    def __init__(self, arg):
        self.arg = arg
    def _print(self, indent=0):
        print(' '*indent + '| print("'+str(self.arg)+'")')

class Compute(Node):
    def __init__(self, arg):
        self.arg = arg
    def _print(self, indent=0):
        print(' '*indent + '| compute("'+str(self.arg)+'")')

