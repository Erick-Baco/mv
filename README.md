
# 🧠 RISC-V Virtual Machine

Este proyecto es un **simulador de una máquina virtual RISC-V**, diseñado para ejecutar instrucciones en ensamblador RISC-V línea por línea. 

---

## 🚀 Objetivo

Simular el comportamiento de una arquitectura RISC-V de 32 bits (RV32I), permitiendo:

* Cargar programas escritos en ensamblador.
* Ejecutarlos instrucción por instrucción.
* Manipular registros, memoria, saltos y llamadas al sistema (`ecall`).
* Mostrar resultados en vista gráfica.

---

## 🧱 Arquitectura basada en SRP + MVC

El proyecto sigue el **principio de responsabilidad única (SRP)**, **el patron singleton** y está organizado en una arquitectura **MVC**, facilitando mantenimiento, escalabilidad y pruebas unitarias.

```
src/
├── model/           # Lógica del simulador (Singleton)
│   └── riscv_simulator.py
├── service/         # Clases especializadas
│   ├── executor.py      # Ejecuta instrucciones
│   └── parser.py        # Parsea argumentos y etiquetas
├── controller/
│   └── simulator.py     # Controlador general (opcional)
└── view/
    └── main.py          # Punto de entrada
```

---

## 🛠️ Tecnologías

* Python 3.11+
* Compatible con interfaz gráfica (`tkinter`) 

---

## 🧪 Instrucciones soportadas (subset RV32I)

* **Aritmética**: `add`, `sub`, `addi`, `mul`
* **Lógica**: `and`, `or`, `xor`
* **Memoria**: `lw`, `sw`
* **Saltos condicionales**: `beq`, `bne`, `blt`, `bge`, `ble`
* **Saltos incondicionales**: `j`, `jal`, `jalr`
* **Asignaciones**: `li`, `mv`
* **Syscalls**: `ecall` (print y exit)

---

## 📦 Cómo ejecutar

```bash
# Estando en la raíz del proyecto (donde está src/)
python src/view/virtual_machine.py
```


---

## 👨‍💻 Autor

* [ ] Eder Alvarez
* [ ] Erick Baco
* [ ] Humberto Trujillo

FES Aragón – UNAM
6º semestre | Compiladores 2025
