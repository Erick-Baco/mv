import tkinter as tk
from tkinter import scrolledtext, messagebox
from threading import Thread
import time
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar desde model/riscv_simulator
from model.riscv_simulator import RiscVSimulator


class RiscVGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RISC-V Simulator GUI")
        self.geometry("1200x900")

        self.sim = RiscVSimulator()

        # --- Widgets ---

        self.code_text = scrolledtext.ScrolledText(self, width=70, height=40)
        self.code_text.grid(row=0, column=0, rowspan=6, padx=5, pady=5)

        self.state_text = scrolledtext.ScrolledText(self, width=50, height=50, state='disabled')
        self.state_text.grid(row=0, column=1, rowspan=6, padx=5, pady=5)

        self.output_text = scrolledtext.ScrolledText(self, width=90, height=5, state='disabled', fg='green')
        self.output_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

        self.btn_load = tk.Button(self, text="Cargar Programa", command=self.load_program)
        self.btn_load.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.btn_run = tk.Button(self, text="Ejecutar Todo", command=self.run_program)
        self.btn_run.grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        self.btn_step = tk.Button(self, text="Paso a Paso", command=self.step_program)
        self.btn_step.grid(row=2, column=2, padx=5, pady=5, sticky="ew")

        self.btn_clear = tk.Button(self, text="Limpiar Consola", command=self.clear_output)
        self.btn_clear.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def print_output(self, msg):
        self.output_text.configure(state='normal')
        self.output_text.insert(tk.END, msg + "\n")
        self.output_text.see(tk.END)
        self.output_text.configure(state='disabled')

    def clear_output(self):
        self.output_text.configure(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state='disabled')

    def load_program(self):
        code = self.code_text.get(1.0, tk.END)
        try:
            self.sim.load_program(code)
            self.print_output("Programa cargado correctamente.")
            self.update_state()
        except Exception as e:
            messagebox.showerror("Error al cargar programa", str(e))

    def run_program(self):
        def run():
            self.sim.running = True
            while self.sim.running and self.sim.pc in self.sim.instructions:
                self.sim.executor.execute(self.sim.instructions[self.sim.pc])
                self.update_state()
                time.sleep(0.05)
            self.print_output("Ejecución finalizada.")

        Thread(target=run).start()

    def step_program(self):
        if not self.sim.running:
            self.sim.running = True
        if self.sim.pc not in self.sim.instructions:
            self.print_output("No hay más instrucciones para ejecutar.")
            self.sim.running = False
            return
        self.sim.executor.execute(self.sim.instructions[self.sim.pc])
        self.update_state()
        if not self.sim.running:
            self.print_output("Programa terminado.")

    def update_state(self):
        state_str = self.sim.get_state_text()
        self.state_text.configure(state='normal')
        self.state_text.delete(1.0, tk.END)
        self.state_text.insert(tk.END, state_str)
        self.state_text.configure(state='disabled')

    def on_close(self):
        self.destroy()


if __name__ == "__main__":
    app = RiscVGUI()
    # # Puede poner cualquier programa aqui, solo omita las primeras comillas y al final no olvide cerrar el parentesis profe
    app.code_text.insert(tk.END, """\
li f0, 1.5708         # 90 grados en radianes aprox (pi/2)
fsin.s f1, f0         # f1 = sin(f0) ≈ 1.0
fcos.s f2, f0         # f2 = cos(f0) ≈ 0.0
ftan.s f3, f0         # f3 = tan(f0) ≈ muy grande

fmv.s f10, f1         # mover f1 a fa0 para imprimir
li a7, 2
ecall                 # imprime sin(90°) ≈ 1.0000

fmv.s f10, f2
li a7, 2
ecall                 # imprime cos(90°) ≈ 0.0000

fmv.s f10, f3
li a7, 2
ecall                 # imprime tan(90°) ≈ valor grande

li a7, 10
ecall                 # termina

""")
    app.mainloop()
