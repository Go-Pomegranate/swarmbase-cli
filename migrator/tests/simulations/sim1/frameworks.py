import json
import subprocess
import os

frameworks = [
    {
        'name': 'swarm-agency',
        'description': 'Swarm Agency is a framework for managing multi-agent systems.'
    }
]

def create_framework(framework):
    name = framework['name']
    description = framework['description']

    # Prepare the command to create the framework
    cmd = [
        'swarm', 'framework', 'create',
        '--name', name,
        '--description', description
    ]

    try:
        # Run the command and capture the output
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(f"Framework '{name}' created successfully.")
        print(result.stdout)
        return result.stdout  # Return the result output
    except subprocess.CalledProcessError as e:
        print(f"Failed to create framework '{name}'.")
        print(e.stderr)
        return None  # Return None if there's an error

def save_configuration(results):
    # Check if the configuration file exists
    if os.path.exists('configuration.json'):
        with open('configuration.json', 'r') as config_file:
            configuration = json.load(config_file)
    else:
        configuration = {}

    # Update the frameworks section
    configuration['frameworks'] = results

    # Write the updated configuration back to the JSON file
    with open('configuration.json', 'w') as config_file:
        json.dump(configuration, config_file, indent=4)
    print("Configuration updated in 'configuration.json'.")

def main():
    results = []  # Initialize a list to store results
    for framework in frameworks:
        result = create_framework(framework)
        if result is not None:
            results.append(result)  # Append the result to the list

    save_configuration(results)  # Save the results to configuration.json

if __name__ == '__main__':
    main()
