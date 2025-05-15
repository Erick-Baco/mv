from model.riscv_simulator import RiscVSimulator

# Programa de ejemplo: suma del 1 al 10
example_program = """
# Ejemplo 3: Mayor de tres números
# Este programa encuentra el mayor de tres números
#
# Registros utilizados:
# a0 (x10): Primer número y resultado final
# a1 (x11): Segundo número
# a2 (x12): Tercer número
# a3 (x13): Mayor temporal

mayor_de_tres:
    li a0, 15      # Primer número
    li a1, 7       # Segundo número
    li a2, 42      # Tercer número
    
    mv a3, a0      # Inicializa mayor con el primer número
    
    bge a3, a1, check_third  # Si mayor >= segundo, salta
    mv a3, a1      # Si no, actualiza mayor con segundo
    
check_third:
    bge a3, a2, fin  # Si mayor >= tercero, salta
    mv a3, a2      # Si no, actualiza mayor con tercero
    
fin:
    mv a0, a3      # Mueve el resultado a a0 para retornar
    
    li a7, 1       # Código para imprimir entero
    ecall          # Llamada al sistema para imprimir
    
    li a7, 10      # Código para terminar programa
    ecall          # Llamada al sistema para terminar


"""

def main():
    simulator = RiscVSimulator()
    simulator.load_program(example_program)
    result = simulator.run()
    print(f"\nResultado final en a0 (x10): {result}")

if __name__ == "__main__":
    main()
