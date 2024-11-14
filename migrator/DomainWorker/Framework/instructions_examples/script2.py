import subprocess

frameworks = [
    {
        'name': 'langchain',
        'description': 'LangChain is a framework for building language model applications.'
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

    except subprocess.CalledProcessError as e:
        print(f"Failed to create framework '{name}'.")
        print(e.stderr)

def main():
    for framework in frameworks:
        create_framework(framework)

if __name__ == '__main__':
    main()
