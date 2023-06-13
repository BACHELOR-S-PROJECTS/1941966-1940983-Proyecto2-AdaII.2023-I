import tkinter as tk
from tkinter import scrolledtext
from execute_mzn import execute_mzn_file

# Create a new Tkinter window
window = tk.Tk()
window.title("PROYECTO 2 DE ADA - CALENDARIOS DEPORTIVOS")

# Obtener las dimensiones de la pantalla
screen_width = window.winfo_screenwidth() // 2
screen_height = window.winfo_screenheight() // 2

# Establecer las dimensiones de la ventana
window.geometry(f"{screen_width}x{screen_height}")

# Crear un contenedor para los componentes horizontales
frame = tk.Frame(window)
frame.pack()

PAD_X = 15

def hallarSol():
    entradaUsuario = text_area.get("1.0", tk.END)

    f = open("params.dzn", "w")
    f.write(entradaUsuario)
    f.close()

    execute_mzn_file("model.mzn","params.dzn")
    solucion = ""

    inputtxt.config(state='normal')
    inputtxt.delete("1.0", tk.END)
    inputtxt.insert(tk.END, entradaUsuario)
    inputtxt.config(state='disabled')

text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=screen_width // 20, height=screen_height // 50, font=("Times New Roman", 15))
text_area.pack(side=tk.LEFT, padx=PAD_X, ipadx=screen_width // 15, ipady=10)

# Crear un botón para obtener el texto
button = tk.Button(frame, text="HALLAR SOLUCION", command=hallarSol)
button.pack(side=tk.LEFT, padx=PAD_X, ipadx=screen_width // 15, ipady=10)

# Create a label widget
label = tk.Label(window, text="SOLUCION ENCONTRADA:", bg="grey", fg="white")
label.pack(side=tk.TOP, padx=PAD_X, ipadx=11, ipady=11)

inputtxt = tk.Text(window, height=10, width=25, bg="light yellow", state='disabled')
inputtxt.pack(side=tk.TOP, padx=PAD_X, ipadx=screen_width, ipady=10)

window.mainloop()
