class Interpreter:
    def __init__(self):
        self.stack = []

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


what_to_execute = {
    'instructions': [('LOAD_VALUE', 0), # First number
                     ('LOAD_VALUE', 1), # Second number
                     ('ADD_TWO_VALUES', None),
                     ('PRINT_ANSWER', None)
                     ],

    'numbers': [7, 5]
}

interpreter = Interpreter()
interpreter.run_method(what_to_execute)
