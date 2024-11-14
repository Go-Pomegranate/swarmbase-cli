import json
import subprocess
import os

# Define your tools with their properties
tools = [
    {
        'name': 'ToolFactory',
        'description': 'Factory for creating tools.',
        'version': '1.0',
        'code': 'ToolFactory.from_langchain_tool(HumanInputRun)',
        'extra_attributes': '{}'
    },
    {
        'name': 'HumanInputRun',
        'description': 'Tool for human input.',
        'version': '1.0',
        'code': 'HumanInputRun()',
        'extra_attributes': '{}'
    },
    {
        'name': 'CopyFileTool',
        'description': 'Tool for copying files.',
        'version': '1.0',
        'code': 'CopyFileTool()',
        'extra_attributes': '{}'
    },
    {
        'name': 'DeleteFileTool',
        'description': 'Tool for deleting files.',
        'version': '1.0',
        'code': 'DeleteFileTool()',
        'extra_attributes': '{}'
    },
    {
        'name': 'FileSearchTool',
        'description': 'Tool for searching files.',
        'version': '1.0',
        'code': 'FileSearchTool()',
        'extra_attributes': '{}'
    },
    {
        'name': 'ListDirectoryTool',
        'description': 'Tool for listing directories.',
        'version': '1.0',
        'code': 'ListDirectoryTool()',
        'extra_attributes': '{}'
    },
    {
        'name': 'MoveFileTool',
        'description': 'Tool for moving files.',
        'version': '1.0',
        'code': 'MoveFileTool()',
        'extra_attributes': '{}'
    },
    {
        'name': 'ReadFileTool',
        'description': 'Tool for reading files.',
        'version': '1.0',
        'code': 'ReadFileTool()',
        'extra_attributes': '{}'
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
        return result.stdout  # Return the result output
    except subprocess.CalledProcessError as e:
        print(f"Failed to create tool '{name}'.")
        print(e.stderr)
        return None  # Return None if there's an error

def save_configuration(results):
    # Check if the configuration file exists
    if os.path.exists('configuration.json'):
        with open('configuration.json', 'r') as config_file:
            configuration = json.load(config_file)
    else:
        configuration = {}

    # Update the tools section
    configuration['tools'] = results

    # Write the updated configuration back to the JSON file
    with open('configuration.json', 'w') as config_file:
        json.dump(configuration, config_file, indent=4)
    print("Configuration updated in 'configuration.json'.")

def main():
    results = []  # Initialize a list to store results
    for tool in tools:
        result = create_tool(tool)
        if result is not None:
            results.append(result)  # Append the result to the list

    save_configuration(results)  # Save the results to configuration.json

if __name__ == '__main__':
    main()
