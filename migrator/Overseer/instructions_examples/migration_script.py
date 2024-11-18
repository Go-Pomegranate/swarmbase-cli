import subprocess
import os

def run_script(script_name):
    try:
        # Construct the full path to the script
        script_path = os.path.join(os.getcwd(), script_name)

        # Check if the script exists
        if not os.path.isfile(script_path):
            print(f"Script '{script_name}' not found.")
            return

        # Run the script
        print(f"Running '{script_name}'...")
        result = subprocess.run(['python', script_path], check=True, text=True, capture_output=True)
        print(f"Finished running '{script_name}'.")
        print("Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running '{script_name}'.")
        print(e.stderr)

def main():
    scripts = ['[path_to_project]/swarms.py', '[path_to_project]/agents.py', '[path_to_project]/frameworks.py', '[path_to_project]/tools.py']

    for script in scripts:
        run_script(script)

if __name__ == '__main__':
    main()