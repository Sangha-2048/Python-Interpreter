'''
    Frame Class
    Collection of attributes with no methods
    Attributes include: code object created by the complier (containing instructions and
    constants + variables) + reference to prev. frame + data stack + block stack +
    local, global, built-in namespaces and the last instruction executed
'''

class Frame:

    def __init__(self, code_object, global_names, local_names, prev_frame):
        self.code_object = code_object
        self.global_names = global_names
        self.local_names = local_names
        self.prev_frame = prev_frame
        self.stack = []

        if prev_frame is not None:
            self.builtin_names = prev_frame.builtin_names
        else:
            self.builtin_names = local_names['__builtins__']

            if hasattr(self.builtin_names, '__dict__'):
                self.builtin_names = self.builtin_names.__dict__

        self.last_instruction = 0

        self.block_stack = []








