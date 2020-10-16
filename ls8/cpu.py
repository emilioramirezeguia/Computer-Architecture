"""CPU functionality."""

import sys

HLT = 0b00000001  # 1
LDI = 0b10000010  # 130
PRN = 0b01000111  # 71
ADD = 0b10100000  # 160
SUB = 0b10100001  # 161
MUL = 0b10100010  # 162
CMP = 0b10100111  # 167
PUSH = 0b01000101  # 69
POP = 0b01000110  # 70
CALL = 0b01010000  # 80
RET = 0b00010001  # 17
JMP = 0b01010100  # 84
JEQ = 0b01010101  # 85
JNE = 0b01010110  # 86
AND = 0b10101000  # 168
OR = 0b10101010  # 170
XOR = 0b10101011  # 171
NOT = 0b01101001  # 105


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.program_counter = 0
        self.stack_pointer = 7
        self.flag = 0b00000000
        self.register[self.stack_pointer] = 0xf4
        self.running = False
        self.dispatch_table = {}
        self.dispatch_table[HLT] = self.handle_hlt
        self.dispatch_table[LDI] = self.handle_ldi
        self.dispatch_table[PRN] = self.handle_prn
        self.dispatch_table[ADD] = self.handle_add
        self.dispatch_table[SUB] = self.handle_sub
        self.dispatch_table[MUL] = self.handle_mul
        self.dispatch_table[CMP] = self.handle_cmp
        self.dispatch_table[PUSH] = self.handle_push
        self.dispatch_table[POP] = self.handle_pop
        self.dispatch_table[CALL] = self.handle_call
        self.dispatch_table[RET] = self.handle_ret
        self.dispatch_table[JMP] = self.handle_jmp
        self.dispatch_table[JEQ] = self.handle_jeq
        self.dispatch_table[JNE] = self.handle_jne
        self.dispatch_table[AND] = self.handle_and
        self.dispatch_table[OR] = self.handle_or
        self.dispatch_table[XOR] = self.handle_xor
        self.dispatch_table[NOT] = self.handle_not

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
        elif op == "CMP":
            if self.register[reg_a] == self.register[reg_b]:
                self.flag = 0b00000001
            else:
                self.flag = 0b00000000
            # print("Flag BEFORE: ", self.flag)
            # if self.register[reg_a] < self.register[reg_b]:
            #     self.flag = 0b00000100
            # elif self.register[reg_a] > self.register[reg_b]:
            #     self.flag = 0b00000010
            # else:
            #     self.flag = 0b00000001
            # print("Flag AFTER: ", self.flag)
        elif op == "AND":
            self.register[reg_a] = self.register[reg_a] & self.register[reg_b]
        elif op == "OR":
            self.register[reg_a] = self.register[reg_a] | self.register[reg_b]
        elif op == "XOR":
            self.register[reg_a] = self.register[reg_a] ^ self.register[reg_b]
        elif op == "NOT":
            self.register[reg_a] = ~self.register[reg_a]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            self.flag,
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

    # ADD (add the value in two registers and store the result in registerA)
    def handle_add(self, a, b):
        self.alu("ADD", a, b)

    # SUB (subtract the value in the second register from the first, storing the result in registerA)
    def handle_sub(self, a, b):
        self.alu("SUB", a, b)

    # MUL (multiply the values in two registers together and store the result in registerA)
    def handle_mul(self, a, b):
        self.alu("MUL", a, b)

    # CMP (compare the values in two registers)
    def handle_cmp(self, a, b):
        self.alu("CMP", a, b)

    # PUSH (push the value in the given register on the stack)
    def handle_push(self, a, b):
        # decrement the stack pointer
        self.register[self.stack_pointer] -= 1

        # grab the value out of the given register
        value = self.register[a]

        # copy the value onto the stack
        top_of_the_stack_address = self.register[self.stack_pointer]
        self.ram[top_of_the_stack_address] = value

    # POP (pop the value at the top of the stack into the given register)
    def handle_pop(self, a, b):
        # grab the value from the top of the stack
        top_of_the_stack_address = self.register[self.stack_pointer]
        value = self.ram[top_of_the_stack_address]

        # store the value in the register
        self.register[a] = value

        # increment the stack pointer
        self.register[self.stack_pointer] += 1

    def handle_call(self, a, b):
        # get the address of the next instruction after the call
        return_address = self.program_counter + 2

        # push the address onto the stack
        self.push_value(return_address)

        # get subroutine address from register
        subroutine_address = self.register[a]

        # jump to it
        self.program_counter = subroutine_address

    # RET (return from subroutine)
    def handle_ret(self, a, b):
        # get return address from the top of the stack
        return_address = self.pop_value()

        # store it in the program counter
        self.program_counter = return_address

    # JMP (jump to the address stored in the given register)
    def handle_jmp(self, a, b):
        # get jump address from the given register
        jump_address = self.register[a]

        # set it to the program counter and jump to it
        self.program_counter = jump_address

    # JEQ (if equal flag is true, jump to the address in the register)
    def handle_jeq(self, a, b):
        # get jump address from the given register
        jump_address = self.register[a]

        # if the equal flag is set to true, jump to that address
        if self.flag == 1:
            self.program_counter = jump_address
        else:
            self.program_counter += 2

    # JNE (if equal flag is false, jump to the address in the register)
    def handle_jne(self, a, b):
        # get jump address from the given register
        jump_address = self.register[a]

        # if the equal flag is set to false, jump to that address
        if self.flag == 0:
            self.program_counter = jump_address
        else:
            self.program_counter += 2

    # AND (Bitwise-AND the values in registerA and registerB, then store the result in registerA)
    def handle_and(self, a, b):
        self.alu("AND", a, b)

    # OR (perform a bitwise-OR between the values in registerA and registerB, storing the result in registerA)
    def handle_or(self, a, b):
        self.alu("OR", a, b)

    # XOR (perform a bitwise-XOR between the values in registerA and registerB, storing the result in registerA)
    def handle_xor(self, a, b):
        self.alu("XOR", a, b)

    # NOT (perform a bitwise-NOT on the value in a register, storing the result in the register)
    def handle_not(self, a, b):
        self.alu("NOT", a, b)

    def push_value(self, value):
        # decrement the stack pointer
        self.register[self.stack_pointer] -= 1

        # copy the value onto the stack
        top_of_the_stack_address = self.register[self.stack_pointer]
        self.ram[top_of_the_stack_address] = value

    def pop_value(self):
        # grab the value from the top of the stack
        top_of_the_stack_address = self.register[self.stack_pointer]
        value = self.ram[top_of_the_stack_address]

        # increment the stack pointer
        self.register[self.stack_pointer] += 1

        return value

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
                print(
                    f"Unkown instruction: {instruction_register} at address {self.program_counter}")
                sys.exit(1)

            # declare a variable and check if that bit is equal to 1 (true/false value)
            set_instruction = ((instruction_register & 0b00010000))
            if set_instruction != 0:
                pass
            # if instruction_register == CALL or instruction_register == RET:
            #     pass
            else:
                # if it's not true, increment as normal
                instruction_length = (
                    (instruction_register & 0b11000000) >> 6) + 1
                # this also works => instruction_length = (instruction_register >> 6) + 1
                self.program_counter += instruction_length
