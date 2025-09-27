'''
    Virtual Machine Class
    Single instance will be created each time the program is run
    since we have only one Python Interpreter
    It stores call stack, exception state, return values while they are being passed
    between frames
'''

from Frame import Frame

class VirtualMachineError(Exception):
    pass

class VirtualMachine(object):
    '''
        Here class VirtualMachine(object): is
        equivalent to class VirtualMachine:
        as all classes in Python are inherited from object
        for Python 3+

        In Python 2 versions you need to explicitly specify the above object definition
        to use some of the built-in methods of object class like super()
    '''
    def __init__(self):
        self.frames = []
        self.frame = None # Current frame
        self.return_value = None
        self.last_exception = None

    def run_code(self, code, global_names = None, local_names = None):
        '''
            Entry point to execute code using virtual machine
            Starts by setting up and running a frame
            This frame can create more frames in the future
            The call stack may grow and shrink as program executes
            When first frame eventually returns then the execution of program completes
        '''

        frame = self.make_frame(code, global_names = global_names, local_names = local_names)
        return self.run_frame(frame)

    '''
        Adding frame manipulation in virtual machine
        3 helper functions in the frame
        1. Create a new frame (responsible for sorting out namespaces in new frame)
        2. Other two to push and pop frame from the frame stack
    '''

    def make_frame(self, code, call_args=None, global_names = None, local_names = None):
        '''
            code: code object to run
            call_args: function arguments passed in
            global_names: dictionary of global variables
            local_names: dictionary of local variables
        '''

        if call_args is None:
            call_args = {}
        if global_names is not None and local_names is not None:
            local_names = global_names

        # Case already inside another frame
        # mimicking function call where global remains the same and start with new local variables
        elif self.frames:
            global_names = self.frame.global_names
            local_names = {}

        # Case when no frame exists,
        # Creating new python env of global and local like python does when running a script
        # Keys like __builtins__ come from python global namespaces
        else:
            global_names = local_names = {
                '__builtins__' : __builtins__,
                '__name__': '__main__',
                '__doc__': None,
                '__package__': None
            }

        local_names.update(call_args)
        frame = Frame(code, global_names, local_names, self.frame)

        return frame


    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()

        if self.frames:
            self.frame = self.frames[-1] # Updating the current frame with the prev one

        else:
            self.frame = None

    # Adding some helper methods for data stack manipulation
    def top(self):
        return self.frame.stack[-1]

    def pop(self):
        return self.frame.stack.pop()

    # *val means that function can take any number of arguments
    # extend() method adds all the elements of iterable to the list
    def push(self, *vals):
        self.frame.stack.extend(vals)

    def popn(self, n):
        '''
            Pop a number of n values from the stack
            Ordered by deepest value first
        '''

        if n:
            res = self.frame.stack[-n:]
            self.frame.stack[-n:] = []
            return res
        else:
            return []


    # Adding another method that checks and parses the argument and updates last_instruction attribute in frame

    def run_frame(self):
        pass