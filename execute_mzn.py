import subprocess
import tkinter as tk

def execute_mzn_file(comando,label):
    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

    # Lee la salida línea por línea mientras se ejecuta el comando
    while True:
        salida = proceso.stdout.readline()
        if salida == b'' and proceso.poll() is not None:
            break
        if salida:
            print(salida.strip().decode())  # Muestra la salida
            #for i in salida.strip().decode():
             #yield "a"
            label.config(state='normal')
            label.delete("1.0", tk.END)
            label.insert(tk.END,"a")
            label.update()
            #inputtxt.insert(tk.END, solucion)
            label.config(state='disabled')
            
            
    # Espera a que el comando termine y obtén el código de salida
    codigo_salida = proceso.poll()
    return codigo_salida