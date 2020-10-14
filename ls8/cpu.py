"""CPU functionality."""

import sys

HLT = 0b00000001  # 1
LDI = 0b10000010  # 130
PRN = 0b01000111  # 71
MUL = 0b10100010  # 162


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.program_counter = 0
        self.running = False
        self.dispatch_table = {}
        self.dispatch_table[HLT] = self.handle_hlt
        self.dispatch_table[LDI] = self.handle_ldi
        self.dispatch_table[PRN] = self.handle_prn
        self.dispatch_table[MUL] = self.handle_mul

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
        # elif op == "SUB": etc
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

    def handle_hlt(self, a, b):
        self.running = False

    def handle_ldi(self, a, b):
        self.register[a] = b

    def handle_prn(self, a, b):
        print(self.register[a])

    def handle_mul(self, a, b):
        self.alu("MUL", a, b)

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

            # # HLT (halt the CPU and exit the emulator)
            # if instruction_register == HLT:
            #     running = False

            # # LDI (set the value of a register to an integer)
            # if instruction_register == LDI:
            #     self.dispatch_table[LDI](operand_a, operand_b)

            # # PRN (print numeric value stored in the given register)
            # if instruction_register == PRN:
            #     self.dispatch_table[PRN](operand_a)

            # # MUL (multiply the values in two registers together and store the result in registerA)
            # if instruction_register == MUL:
            #     self.dispatch_table[MUL](operand_a, operand_b)

            # print(f"Unkown instruction: {instruction_register}")
            # sys.exit(1)
