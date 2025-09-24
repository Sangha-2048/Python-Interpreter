class Interpreter:
    def __init__(self):
        self.stack = []
        self.env = {}

    def STORE_NAME(self, name):
        val = self.stack.pop()
        self.env[name] = val

    def LOAD_NAME(self, name):
        val = self.env[name]
        self.stack.append(val)

    def LOAD_VALUE(self, number):
        self.stack.append(number)

    def PRINT_ANSWER(self):
        answer = self.stack.pop()
        print(answer)

    def ADD_TWO_VALUES(self):
        first_num = self.stack.pop()
        second_num = self.stack.pop()
        total = first_num + second_num
        self.stack.append(total)

    def parse_argument(self, instruction, argument, what_to_execute):
        '''
            Defining a function to clearly identify
            what the argument mean to the instruction
        '''

        numbers = ['LOAD_VALUE']
        names = ['LOAD_NAME', 'STORE_NAME']

        if instruction in numbers:
            return what_to_execute['numbers'][argument]

        elif instruction in names:
            return what_to_execute['names'][argument]

        return None

    def run_method(self, what_to_execute):

        instructions = what_to_execute['instructions']
        numbers = what_to_execute['numbers']

        for each_step in instructions:
            instruction, argument = each_step

            if instruction == 'LOAD_VALUE':
                number = numbers[argument]
                self.LOAD_VALUE(number)

            elif instruction == 'ADD_TWO_VALUES':
                self.ADD_TWO_VALUES()

            elif instruction == 'PRINT_ANSWER':
                self.PRINT_ANSWER()


    def execute(self, what_to_execute):
        instructions = what_to_execute['instructions']

        for each_step in instructions:
            instruction, argument = each_step

            argument = self.parse_argument(instruction, argument, what_to_execute)

            bytecode_method = getattr(self, instruction)

            if argument is None:
                bytecode_method()
            else:
                bytecode_method(argument)


# Adding two numbers
what_to_execute_addition_of_two_nums = {
    'instructions': [('LOAD_VALUE', 0), # First number
                     ('LOAD_VALUE', 1), # Second number
                     ('ADD_TWO_VALUES', None),
                     ('PRINT_ANSWER', None)
                     ],

    'numbers': [7, 5]
}

# Adding three numbers
what_to_execute_addition_of_three_nums = {
    "instructions": [("LOAD_VALUE", 0),
                     ("LOAD_VALUE", 1),
                     ("ADD_TWO_VALUES", None),
                     ("LOAD_VALUE", 2),
                     ("ADD_TWO_VALUES", None),
                     ("PRINT_ANSWER", None)],
    "numbers": [7, 5, 8]}



interpreter = Interpreter()
interpreter.run_method(what_to_execute_addition_of_three_nums)
