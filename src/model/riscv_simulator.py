#from service.executor import InstructionExecutor
#from service.parser import InstructionParser
from src.service.executor import InstructionExecutor
from src.service.parser import InstructionParser


class RiscVSimulator:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RiscVSimulator, cls).__new__(cls)
            cls._instance._init_internal()
        return cls._instance

    def _init_internal(self):
        self.registers = [0] * 32
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

    def run(self):
        self.running = True
        self.pc = 0

        while self.running and self.pc in self.instructions:
            instruction = self.instructions[self.pc]
            self.executor.execute(instruction)

        return self.registers[10]
