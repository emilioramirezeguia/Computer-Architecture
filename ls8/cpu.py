"""CPU functionality."""

import sys

HLT = 0b00000001  # 1
LDI = 0b10000010  # 130
PRN = 0b01000111  # 71
MUL = 0b10100010  # 162
PUSH = 0b01000101  # 69
POP = 0b01000110  # 70


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.program_counter = 0
        self.stack_pointer = 7
        self.register[self.stack_pointer] = 0xf4
        self.running = False
        self.dispatch_table = {}
        self.dispatch_table[HLT] = self.handle_hlt
        self.dispatch_table[LDI] = self.handle_ldi
        self.dispatch_table[PRN] = self.handle_prn
        self.dispatch_table[MUL] = self.handle_mul
        self.dispatch_table[PUSH] = self.handle_push
        self.dispatch_table[POP] = self.handle_pop

    def ram_read(self, memory_address_register):
        memory_data_register = self.ram[memory_address_register]
        return memory_data_register

    def ram_write(self, memory_address_register, memory_data_register):
        self.ram[memory_address_register] = memory_data_register

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Usage: compy.py <program_name>")
            sys.exit(1)

        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()

                    if line == "" or line[0] == "#":
                        continue

                    try:
                        string_value = line.split("#")[0]
                        value = int(string_value, 2)

                    except ValueError:
                        print(f"Invalid number: {string_value}")
                        sys.exit(1)

                    self.ram[address] = value
                    address += 1

        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "SUB":
            self.register[reg_a] -= self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            # self.fl,
            # self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    # HLT (halt the CPU and exit the emulator)
    def handle_hlt(self, a, b):
        self.running = False

    # LDI (set the value of a register to an integer)
    def handle_ldi(self, a, b):
        self.register[a] = b

    # PRN (print numeric value stored in the given register)
    def handle_prn(self, a, b):
        print(self.register[a])

    # MUL (multiply the values in two registers together and store the result in registerA)
    def handle_mul(self, a, b):
        self.alu("MUL", a, b)

    # PUSH (push the value in the given register on the stack.)
    def handle_push(self, a, b):
        # decrement the stack pointer
        self.register[self.stack_pointer] -= 1

        # grab the value out of the given register
        value = self.register[a]  # => this is the value we want to push

        # copy the value onto the stack
        top_of_the_stack_address = self.register[self.stack_pointer]
        self.ram[top_of_the_stack_address] = value

    # POP (pop the value at the top of the stack into the given register)
    def handle_pop(self, a, b):
        # grab the value from the top of the stack
        top_of_the_stack_address = self.register[self.stack_pointer]

        # store the value in the register
        self.register[a] = top_of_the_stack_address

        # increment the stack pointer
        self.register[self.stack_pointer] += 1

    def run(self):
        """Run the CPU."""

        self.running = True

        while self.running:
            instruction_register = self.ram_read(self.program_counter)
            operand_a = self.ram_read(self.program_counter + 1)
            operand_b = self.ram_read(self.program_counter + 2)

            if instruction_register in self.dispatch_table:
                self.dispatch_table[instruction_register](operand_a, operand_b)
            else:
                print(f"Unkown instruction: {instruction_register}")
                sys.exit(1)

            instruction_length = ((instruction_register & 0b11000000) >> 6) + 1
            # this also works => instruction_length = (instruction_register >> 6) + 1
            self.program_counter += instruction_length
