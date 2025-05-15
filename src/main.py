from model.riscv_simulator import RiscVSimulator

# Programa de ejemplo: suma del 1 al 10
example_program = """
# Inicialización
li a0, 0       # acumulador
li a1, 1       # contador
li a2, 10      # límite

loop:
add a0, a0, a1
addi a1, a1, 1
ble a1, a2, loop

# Imprimir resultado
li a7, 1
ecall

# Finalizar
li a7, 10
ecall
"""

def main():
    simulator = RiscVSimulator()
    simulator.load_program(example_program)
    result = simulator.run()
    print(f"\nResultado final en a0 (x10): {result}")

if __name__ == "__main__":
    main()
