# Patryk Wegrzyn
# Kompilatory - laboratorium - poniedziałek 11:15

class Memory:

    def __init__(self, name):  # memory name
        self.name = name
        self.table = {}

    def has_key(self, name):  # variable name
        return name in self.table

    def get(self, name):         # gets from memory current value of variable <name>
        return self.table[name]

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.table[name] = value


class MemoryStack:

    def __init__(self, memory=None):  # initialize memory stack with memory <memory>
        self.stack = list()
        self.global_scope_skipped = False
        if memory is None:
            self.stack.append(Memory("globalMemory"))
        else:
            self.stack.append(memory)

    def get(self, name):   # gets from memory stack current value of variable <name>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                return memory.get(name)
        return None

    def insert(self, name, value):  # inserts into memory stack variable <name> with value <value>
        self.stack[-1].put(name, value)

    def set(self, name, value):  # sets variable <name> to value <value>
        for memory in reversed(self.stack):
            if memory.has_key(name):
                memory.put(name, value)
                return

    def push(self, memory):  # pushes memory <memory> onto the stack
        if self.global_scope_skipped:
            self.stack.append(memory)
        else:
            self.global_scope_skipped = True

    def pop(self):    # pops the top memory from the stack
        self.stack.pop()
