'''
    Virtual Machine Class
    Single instance will be created each time the program is run
    since we have only one Python Interpreter
    It stores call stack, exception state, return values while they are being passed
    between frames
'''

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

