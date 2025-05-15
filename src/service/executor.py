class InstructionExecutor:
    def __init__(self, simulator):
        self.sim = simulator
        self.parser = simulator.parser

    def execute(self, instruction):
        parts = instruction.split()
        opcode = parts[0].lower()
        next_pc = self.sim.pc + 4

        # Aritmética
        if opcode == 'add':
            rd, rs1, rs2 = self.parser.parse_r_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] + self.sim.registers[rs2]

        elif opcode == 'sub':
            rd, rs1, rs2 = self.parser.parse_r_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] - self.sim.registers[rs2]

        elif opcode == 'addi':
            rd, rs1, imm = self.parser.parse_i_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] + imm

        elif opcode == 'mul':
            rd, rs1, rs2 = self.parser.parse_r_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] * self.sim.registers[rs2]

        # Lógicos
        elif opcode == 'and':
            rd, rs1, rs2 = self.parser.parse_r_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] & self.sim.registers[rs2]

        elif opcode == 'or':
            rd, rs1, rs2 = self.parser.parse_r_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] | self.sim.registers[rs2]

        elif opcode == 'xor':
            rd, rs1, rs2 = self.parser.parse_r_type(parts[1:])
            self.sim.registers[rd] = self.sim.registers[rs1] ^ self.sim.registers[rs2]

        # Memoria
        elif opcode == 'lw':
            rd, offset, rs1 = self.parser.parse_load(parts[1:])
            address = self.sim.registers[rs1] + offset
            self.sim.registers[rd] = self.sim.memory.get(address, 0)

        elif opcode == 'sw':
            rs2, offset, rs1 = self.parser.parse_store(parts[1:])
            address = self.sim.registers[rs1] + offset
            self.sim.memory[address] = self.sim.registers[rs2]

        # Control de flujo
        elif opcode == 'beq':
            rs1, rs2, label = self.parser.parse_branch(parts[1:])
            if self.sim.registers[rs1] == self.sim.registers[rs2]:
                next_pc = self.parser.resolve_label(label)

        elif opcode == 'bne':
            rs1, rs2, label = self.parser.parse_branch(parts[1:])
            if self.sim.registers[rs1] != self.sim.registers[rs2]:
                next_pc = self.parser.resolve_label(label)

        elif opcode == 'blt':
            rs1, rs2, label = self.parser.parse_branch(parts[1:])
            if self.sim.registers[rs1] < self.sim.registers[rs2]:
                next_pc = self.parser.resolve_label(label)

        elif opcode in ('j', 'jal'):
            label = parts[1]
            next_pc = self.parser.resolve_label(label)
            if opcode == 'jal':
                self.sim.registers[1] = self.sim.pc + 4

        elif opcode == 'jalr':
            rd, offset, rs1 = self.parser.parse_load(parts[1:])
            self.sim.registers[rd] = self.sim.pc + 4
            next_pc = self.sim.registers[rs1] + offset

        # Asignación y syscall
        elif opcode == 'li':
            rd = self.parser.parse_register(parts[1])
            imm = int(parts[2])
            self.sim.registers[rd] = imm

        elif opcode == 'mv':
            rd = self.parser.parse_register(parts[1])
            rs = self.parser.parse_register(parts[2])
            self.sim.registers[rd] = self.sim.registers[rs]

        elif opcode == 'ecall':
            if self.sim.registers[17] == 1:
                print(f"Output: {self.sim.registers[10]}")
            elif self.sim.registers[17] == 10:
                self.sim.running = False

        elif opcode == 'ble':
            spc, limit, rs2 = self.parser.parse_bucle(parts[1:])
            if self.sim.registers[spc] <= limit:
                next_pc = rs2
                self.sim.pc = next_pc

        elif opcode == 'bge':
            spc, limit, rs2 = self.parser.parse_bucle(parts[1:])
            if self.sim.registers[spc] >= limit:
                next_pc = rs2
                self.sim.pc = next_pc

        else:
            print(f"Instrucción no soportada: {instruction}")

        self.sim.registers[0] = 0
        self.sim.pc = next_pc
