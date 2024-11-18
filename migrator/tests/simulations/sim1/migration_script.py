import subprocess
import os

def run_script(script_name, args=None):
    try:
        # Construct the full path to the script
        script_path = os.path.join(os.getcwd(), script_name)

        # Check if the script exists
        if not os.path.isfile(script_path):
            print(f"Script '{script_name}' not found.")
            return

        # Prepare the command
        command = ['python', script_path]
        if args:
            command.extend(args)

        # Run the script
        print(f"Running '{script_name}' with args {args}...")
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(f"Finished running '{script_name}'.")
        print("Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running '{script_name}'.")
        print(e.stderr)

def main():
    # Define the scripts and their order
    scripts = [
        ('frameworks.py', None),
        ('swarms.py', None),
        ('agents.py', None),
        ('swarms.py', ['--add-agents']),  # Assuming '--add-agents' is a flag to add agents
        ('tools.py', None),
        ('agents.py', ['--assign-tools'])  # Assuming '--assign-tools' is a flag to assign tools
    ]

    for script, args in scripts:
        run_script(script, args)

if __name__ == '__main__':
    main()
