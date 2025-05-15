import tkinter as tk
from tkinter import ttk

def iniciar_maquina_virtual():
    salida_texto.insert(tk.END, "🔧 Máquina virtual iniciada...\n")

ventana = tk.Tk()
ventana.title("Máquina Virtual")
ventana.geometry("400x300")
ventana.configure(bg="black")

# Usar un estilo ttk para el botón
style = ttk.Style()
style.theme_use('alt')  # Cambiar tema para que acepte colores
style.configure("Custom.TButton", background="gray20", foreground="white")

boton_inicio = ttk.Button(
    ventana,
    text="Iniciar",
    command=iniciar_maquina_virtual,
    style="Custom.TButton"
)
boton_inicio.pack(pady=20)

salida_texto = tk.Text(
    ventana,
    height=10,
    width=45,
    font=("Courier", 10),
    bg="black",
    fg="white",
    insertbackground="white"
)
salida_texto.pack(pady=10)

ventana.mainloop()
