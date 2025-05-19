#from service.executor import InstructionExecutor
#from service.parser import InstructionParser
from service.executor import InstructionExecutor
from service.parser import InstructionParser


class RiscVSimulator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RiscVSimulator, cls).__new__(cls)
            cls._instance._init_internal()
        return cls._instance

    def _init_internal(self):
        self.registers = [0] * 32
        self.fregisters = [0.0] * 32
        self.memory = {}
        self.pc = 0
        self.instructions = {}
        self.running = False
        self.parser = InstructionParser(self)
        self.executor = InstructionExecutor(self)

    def load_program(self, program):
        self.registers = [0] * 32
        self.memory = {}
        self.pc = 0
        self.instructions = {}

        address = 0
        for line in program.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if ':' in line:
                label, instruction = line.split(':', 1)
                self.memory[label.strip()] = address
                line = instruction.strip()
                if not line:
                    continue
            self.instructions[address] = line
            address += 4

    def get_state_text(self):
            lines = ["Registros enteros:"]
            for i in range(32):
                alias = ""
                if i == 0: alias = "zero"
                elif i == 1: alias = "ra"
                elif i == 2: alias = "sp"
                elif i == 10: alias = "a0"
                elif i == 17: alias = "a7"
                if alias:
                    lines.append(f"x{i} ({alias}): {self.registers[i]}")
                else:
                    lines.append(f"x{i}: {self.registers[i]}")

            lines.append("\nRegistros flotantes:")
            for i in range(32):
                lines.append(f"f{i}: {self.fregisters[i]:.4f}")

            return "\n".join(lines)
    
    def limpiar_comentarios(codigo_raw: str) -> str:
        """Devuelve el código sin todo lo que aparezca después de '#'."""
        lineas_limpias = []
        for linea in codigo_raw.split('\n'):
            sin_com = linea.split('#', 1)[0].rstrip()
            if sin_com:                       # descarta líneas vacías
                lineas_limpias.append(sin_com)
        return '\n'.join(lineas_limpias)


    def run(self):
        self.running = True
        self.pc = 0

        while self.running and self.pc in self.instructions:
            instruction = self.instructions[self.pc]
            self.executor.execute(instruction)

        return self.registers[10]
