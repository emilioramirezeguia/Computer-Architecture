"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.program_counter = 0

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

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""

        running = True

        while running:
            instruction_register = self.ram_read(self.program_counter)
            operand_a = self.ram_read(self.program_counter + 1)
            operand_b = self.ram_read(self.program_counter + 2)

            # HLT (halt the CPU and exit the emulator)
            if instruction_register == HLT:
                running = False
                self.program_counter += 1
            # LDI (set the value of a register to an integer)
            elif instruction_register == LDI:
                self.register[operand_a] = operand_b
                self.program_counter += 3
            # PRN (print numeric value stored in the given register)
            elif instruction_register == PRN:
                print(self.register[operand_a])
                self.program_counter += 2
            else:
                print(f"Unkown instruction: {instruction_register}")
                sys.exit(1)
