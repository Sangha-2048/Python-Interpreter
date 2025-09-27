'''
    Virtual Machine Class
    Single instance will be created each time the program is run
    since we have only one Python Interpreter
    It stores call stack, exception state, return values while they are being passed
    between frames
'''

from Frame import Frame
import dis

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


    """
    
    1. Adding another method that checks and parses the argument and updates last_instruction attribute in frame
    2. A instruction is 1 byte long if it doesn't have an argument, 3 bytes if does have an argument and last two bytes are argument for this( depending upon the opcode).
    3. Meaning of the argument depends upon which instruction it is.
    
    Example: POP_JUMP_IF_FALSE: Argument to the instruction is the jump target
    BUILD_LIST: Number of elements in the list
    LOAD_CONST: It is an index into list of constants
    
    4. The dis module in the standard library exposes a cheatsheet explaining what arguments have what meaning, which makes our code more compact. 
    For example, the list dis.hasname tells us that the arguments to LOAD_NAME, IMPORT_NAME, LOAD_GLOBAL, and nine other instructions have the same meaning: 
    for these instructions, the argument represents an index into the list of names on the code object.

    """

    def parse_byte_and_args(self):
        """
            Parses single instruction from the bytecode and extracts
            operation and its argument

            Context: In python, functions get compiled into code_objects that contain:
            1. co_code: a byte string of bytecode instructions
            2. co_consts: constants like ( numbers, strings)
            3. co_names: name of global variables
            4. co_varnames: local variables
        """

        f = self.frame # Taking current frame
        op_offset = f.last_instruction # where we are in bytecode (like an instruction pointer)
        byte_code = f.code_obj.co_code[op_offset] # numeric opcode (eg: 100 for LOAD_CONST)
        f.last_instruction += 1 # Moving instruction pointer by 1
        byte_name = dis.opname[byte_code] # This will give the intelligible name for the instruction

        if byte_code >= dis.HAVE_ARGUMENT: # Some opcode has arguments
            # If byte_code >= 90 then it means that instruction takes an argument
            # index into the bytecode
            arg = f.code_obj.co_code[f.last_instruction: f.last_instruction + 2]

            f.last_instruction += 2 # advance the instruction pointer

            arg_val = arg[0] + (arg[1] * 256)

            if byte_code in dis.hasconst: # Look up a constant
                arg = f.code_obj.co_const[arg_val]

            elif byte_code in dis.hasname: # Look up a name
                arg = f.code_obj.co_names[arg_val]

            elif byte_code in dis.haslocal: # Look up a local name
                arg = f.code_obj.co_varnames[arg_val]

            elif byte_code in dis.hasjrel: # Calculate a relative jump
                arg = f.last_instruction + arg_val

            else:
                arg = arg_val

            argument = [arg]

        else:
            # For instructions with no arguments, return empty list
            argument = []

        return byte_name, argument






    def run_frame(self):
        pass