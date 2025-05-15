

class InstructionParser:
    def __init__(self, simulator):
        self.sim = simulator

    def parse_register(self, reg_str):
        reg_str = reg_str.strip(',')
        if reg_str == 'zero':
            return 0
        elif reg_str == 'ra':
            return 1
        elif reg_str == 'sp':
            return 2
        elif reg_str == 'gp':
            return 3
        elif reg_str == 'tp':
            return 4
        elif reg_str.startswith('t') and '0' <= reg_str[1] <= '6':
            return 5 + int(reg_str[1])
        elif reg_str == 'fp' or reg_str == 's0':
            return 8
        elif reg_str.startswith('s') and '1' <= reg_str[1] <= '11':
            return 8 + int(reg_str[1])
        elif reg_str.startswith('a') and '0' <= reg_str[1] <= '7':
            return 10 + int(reg_str[1])
        elif reg_str.startswith('x'):
            return int(reg_str[1:])
        else:
            raise ValueError(f"Registro no reconocido: {reg_str}")

    def parse_r_type(self, args):
        rd = self.parse_register(args[0])
        rs1 = self.parse_register(args[1])
        rs2 = self.parse_register(args[2])
        return rd, rs1, rs2

    def parse_i_type(self, args):
        rd = self.parse_register(args[0])
        rs1 = self.parse_register(args[1])
        imm = int(args[2])
        return rd, rs1, imm

    def parse_load(self, args):
        rd = self.parse_register(args[0])
        offset_base = args[1].split('(')
        offset = int(offset_base[0])
        rs1 = self.parse_register(offset_base[1].strip(')'))
        return rd, offset, rs1

    def parse_store(self, args):
        rs2 = self.parse_register(args[0])
        offset_base = args[1].split('(')
        offset = int(offset_base[0])
        rs1 = self.parse_register(offset_base[1].strip(')'))
        return rs2, offset, rs1

    def parse_branch(self, args):
        rs1 = self.parse_register(args[0])
        rs2 = self.parse_register(args[1])
        label = args[2]
        return rs1, rs2, label

    def parse_bucle(self, args):
        spc = self.parse_register(args[0])
        rs1 = self.parse_register(args[1])
        limit = self.sim.registers[rs1]
        rs2 = self.resolve_label(args[2])
        return spc, limit, rs2

    def resolve_label(self, label):
        if label in self.sim.memory:
            return self.sim.memory[label]
        try:
            return int(label)
        except ValueError:
            raise ValueError(f"Etiqueta no encontrada: {label}")
