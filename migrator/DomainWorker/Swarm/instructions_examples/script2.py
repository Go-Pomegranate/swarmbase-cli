import subprocess

# Define your agents with their properties
swarms = [
    {
        'name': 'swarm-agency',
        'description': 'Swarm Agency is responsible for managing and coordinating swarms.',
        'parent_id': 'N/A'
    }
]

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
    except subprocess.CalledProcessError as e:
        print(f"Failed to create swarm '{name}'.")
        print(e.stderr)

def main():
    for swarm in swarms:
        create_swarm(swarm)

if __name__ == '__main__':
    main()
