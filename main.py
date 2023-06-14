import tkinter as tk
from tkinter import scrolledtext
import subprocess
import tkinter as tk
import re

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



text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=screen_width // 20, height=screen_height // 50, font=("Times New Roman", 15))
text_area.pack(side=tk.LEFT, padx=PAD_X, ipadx=screen_width // 15, ipady=10)
def execute_mzn_file():
    proceso = subprocess.Popen("minizinc -a CalDep.mzn -d DatosCalDep.dzn", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # Lee la salida línea por línea mientras se ejecuta el comando
    salida = None
    todoDeConsola = ""
    i = 0
    while True:
        i = i + 10#10
        salida = proceso.stdout.readline()
        if (i == 1000):
            codigo_salida = proceso.poll()
            break
            

        if salida == b'' and proceso.poll() is not None:
            break
        if salida:
            try:
                print(salida)  # Muestra la salida
                todoDeConsola = todoDeConsola + salida.strip().decode() +"\n"
            except:
                pass
                       
    #for i in salida.strip().decode():
    #yield "a"
    global inputtxt
    inputtxt.config(state='normal')
    inputtxt.delete("1.0", tk.END)
    inputtxt.insert(tk.END,todoDeConsola+"\n")
    inputtxt.update()
    #inputtxt.insert(tk.END, solucion)
    inputtxt.config(state='disabled')               
    # Espera a que el comando termine y obtén el código de salida
    codigo_salida = proceso.poll()
    return codigo_salida


def hallarSol():
    global inputtxt
    inputtxt.config(state='normal')
    inputtxt.delete("1.0", tk.END)
    inputtxt.insert(tk.END,"PROCESANDO...")
    inputtxt.update()
    entradaUsuario = text_area.get("1.0", tk.END)

    list_of_strings = entradaUsuario.split("\n")
    file_dzn = "n = " + list_of_strings[0] + ";\n" + "Min = " + list_of_strings[1] + ";\n" + "Max = " + list_of_strings[2] + ";\nD = \n["
    for i in range(3,3+int(list_of_strings[0])+1):
        file_dzn = file_dzn + "|" + str(list_of_strings[i].replace(" ",", ")) + "\n"
    file_dzn = file_dzn[0:len(file_dzn)-1] + "];"

    def reemplazar_espacios(string):
        # Utilizamos expresiones regulares para encontrar los espacios entre números
        patron = r'(\d+)\s+(\d+)'
        reemplazo = r'\1,\2'
    
        while re.search(patron, string):
            string = re.sub(patron, reemplazo, string)

        return string

    f = open("DatosCalDep.dzn", "w")
    print("Esto:",reemplazar_espacios(file_dzn))
    f.write(reemplazar_espacios(file_dzn))
    f.close()

    #sol = execute_mzn_file("model.mzn","params.dzn",10)

    solucion = execute_mzn_file()

    # inputtxt.config(state='normal')
    # inputtxt.delete("1.0", tk.END)
    # inputtxt.insert(tk.END, solucion)
    # inputtxt.config(state='disabled')

# Crear un botón para obtener el texto
button = tk.Button(frame, text="HALLAR SOLUCION", command=hallarSol)
button.pack(side=tk.LEFT, padx=PAD_X, ipadx=screen_width // 15, ipady=10)

# Create a label widget
label = tk.Label(window, text="SOLUCION ENCONTRADA:", bg="grey", fg="white")
label.pack(side=tk.TOP, padx=PAD_X, ipadx=11, ipady=11)

inputtxt = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=screen_width // 20, height=screen_height // 50, font=("Times New Roman", 15))
inputtxt.pack(side=tk.TOP, padx=PAD_X, ipadx=screen_width, ipady=10)



    
window.mainloop()



