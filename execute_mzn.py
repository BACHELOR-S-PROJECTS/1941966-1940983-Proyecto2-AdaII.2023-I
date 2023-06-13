import subprocess
import threading
result = None
def execute_mzn_file(mzn_file_path, dzn_file_path, timeout_seconds):
    try:
        # Función de ejecución del subproceso
        def run_solver():
            global result
            result = subprocess.run(['minizinc', mzn_file_path, '-d', dzn_file_path],
                                    capture_output=True, text=True)
        
        # Crear un hilo para ejecutar el solver
        solver_thread = threading.Thread(target=run_solver)
        
        # Iniciar el hilo del solver
        solver_thread.start()
        
        # Esperar un máximo de tiempo para que el hilo termine
        solver_thread.join(timeout_seconds)
        
        # Verificar si el solver terminó o aún está en ejecución
        if solver_thread.is_alive():
            # El solver aún está en ejecución, detener el subproceso
            
            print("La ejecución del solver excedió el límite de tiempo.")
            return "La ejecución del solver excedió el límite de tiempo."
        else:
            # El solver ha terminado, imprimir la salida
            if result.returncode == 0:
                print(result.stdout)
                return result.stdout
            else:
                print(result.stderr)
                return result.stderr
    except FileNotFoundError:
        print("MiniZinc solver no encontrado. Asegúrate de que MiniZinc esté instalado y agregado al PATH del sistema.")
        return "MiniZinc solver no encontrado. Asegúrate de que MiniZinc esté instalado y agregado al PATH del sistema."
