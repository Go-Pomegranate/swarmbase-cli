import json
import subprocess
import os
import argparse

# Define your agents with their properties
swarms = [
    {
        'name': 'swarm-agency',
        'description': 'Swarm Agency is responsible for managing and coordinating swarms.',
        'parent_id': 'N/A'
    }
]

def load_configuration():
    if os.path.exists('configuration.json'):
        with open('configuration.json', 'r') as config_file:
            return json.load(config_file)
    return {}

def add_agents_to_swarms():
    config = load_configuration()
    agents = config.get('agents', [])
    swarms = config.get('swarms', [])

    for swarm in swarms:
        for agent in agents:
            # Logic to add agent to swarm
            print(f"Adding agent '{agent}' to swarm '{swarm}'")
            # Implement the actual logic here

def create_swarm(swarm):
    name = swarm['name']

    # Prepare the command to create the swarm
    cmd = [
        'swarm', 'swarm', 'create',
        '--name', name
    ]

    try:
        # Run the command and capture the output
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(f"Swarm '{name}' created successfully.")
        print(result.stdout)
        return result.stdout  # Return the result output
    except subprocess.CalledProcessError as e:
        print(f"Failed to create swarm '{name}'.")
        print(e.stderr)
        return None  # Return None if there's an error

def save_configuration(results):
    # Check if the configuration file exists
    if os.path.exists('configuration.json'):
        with open('configuration.json', 'r') as config_file:
            configuration = json.load(config_file)
    else:
        configuration = {}

    # Update the swarms section
    configuration['swarms'] = results

    # Write the updated configuration back to the JSON file
    with open('configuration.json', 'w') as config_file:
        json.dump(configuration, config_file, indent=4)
    print("Configuration updated in 'configuration.json'.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--add-agents', action='store_true', help='Add agents to swarms')
    args = parser.parse_args()

    if args.add_agents:
        add_agents_to_swarms()
    else:
        # Normal swarm creation logic
        config = load_configuration()
        swarms = config.get('swarms', [])
        results = []  # Initialize a list to store results
        for swarm in swarms:
            result = create_swarm(swarm)
            if result is not None:
                results.append(result)  # Append the result to the list

        save_configuration(results)  # Save the results to configuration.json

if __name__ == '__main__':
    main()
