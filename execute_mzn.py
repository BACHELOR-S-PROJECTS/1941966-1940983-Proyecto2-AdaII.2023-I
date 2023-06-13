import subprocess
def execute_mzn_file(mzn_file_path, dzn_file_path):
    try:
        # Run the MiniZinc solver as a subprocess
        #result = subprocess.run(['minizinc', mzn_file_path, '-d', dzn_file_path], capture_output=True, text=True)
        result = subprocess.run(['minizinc', mzn_file_path], capture_output=True, text=True)
        # Check if the solver executed successfully
        if result.returncode == 0:
            # Print the output
            print(result.stdout)
        else:
            # Print the error message
            print(result.stderr)
    except FileNotFoundError:
        print("MiniZinc solver not found. Make sure MiniZinc is installed and added to the system's PATH.")
