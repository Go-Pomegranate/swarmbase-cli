import subprocess

# Define your tools with their properties
tools = [
    {
        'name': 'ToolName',
        'description': 'Description of the tool.',
        'version': '1.0',
        'code': 'print("Hello, World!")',
        'extra_attributes': '{"attribute1": "value1", "attribute2": "value2"}'
    }
]

def create_tool(tool):
    name = tool['name']
    description = tool['description']
    version = tool['version']
    code = tool['code']
    extra_attributes = tool['extra_attributes']

    # Prepare the command to create the tool
    cmd = [
        'swarm', 'tool', 'create',
        '--name', name,
        '--description', description,
        '--version', version,
        '--code', code,
        '--extra_attributes', extra_attributes
    ]

    try:
        # Run the command and capture the output
        result = subprocess.run(cmd, check=True, text=True, capture_output=True)
        print(f"Tool '{name}' created successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create tool '{name}'.")
        print(e.stderr)

def main():
    for tool in tools:
        create_tool(tool)

if __name__ == '__main__':
    main()