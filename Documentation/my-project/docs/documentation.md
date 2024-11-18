Here's the uniform and consistent version of your documentation, with examples presented clearly alongside each command:

````markdown
# Welcome to Swarmbase.ai Documentation

Swarmbase.ai is a powerful tool for managing multi-agents with various frameworks in one place. This documentation provides an overview of the `swarm` CLI tool, including installation, configuration, and usage.

## Installation

To get started with Swarmbase.ai, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Go-Pomegranate/Swarmbase.ai
   cd Swarmbase.ai
   ```
````

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before using the CLI, set the base URL for the `swarm` API:

```bash
swarm --base-url http://127.0.0.1:5000
```

## Debugging

Most commands support a `--debug` option that enables detailed logging, useful for troubleshooting.

Example:

```bash
swarm agent create --name "AgentName" --description "Description of the agent" --debug
```

## Usage

### Agents

- **Create a new agent:**

  ```bash
  swarm agent create --name <AgentName> --description <Description>
  ```

  Example:

  ```bash
  swarm agent create --name "CEO" --description "Chief Executive Officer responsible for strategic decisions and overall direction"
  ```

- **List all agents:**

  ```bash
  swarm agent list
  ```

- **Get an agent by ID:**

  ```bash
  swarm agent get <agent_id>
  ```

  Example:

  ```bash
  swarm agent get "1235-asd2-3-3"
  ```

- **Update an agent:**

  ```bash
  swarm agent update <agent_id> --name <NewName> --description <NewDescription>
  ```

  Example:

  ```bash
  swarm agent update "1235-asd2-3-3" --name "Better CEO" --description "New Chief Executive Officer overseeing the organization"
  ```

- **Delete an agent:**

  ```bash
  swarm agent delete <agent_id>
  ```

  Example:

  ```bash
  swarm agent delete "1235-asd2-3-3"
  ```

- **Link two agents:**

  ```bash
  swarm agent link --agent1 <agent1_id> --agent2 <agent2_id> --relationship <relationship_type>
  ```

  Where `<relationship_type>` can be one of the following:

  - `"collaborates"`: Both agents can initiate conversations with each other.
  - `"supervises"`: `agent1` can initiate conversations with `agent2`, but `agent2` cannot initiate conversations with `agent1`.

  Example:

  ```bash
  swarm agent link --agent1 "1234-asd-3" --agent2 "1234-asd-4" --relationship "supervises"
  ```

- **Unlink two agents:**

  ```bash
  swarm agent unlink --agent1 <agent1_id> --agent2 <agent2_id>
  ```

  Example:

  ```bash
  swarm agent unlink --agent1 "1234-asd-3" --agent2 "1234-asd-4"
  ```

- **Get agent relationships:**

  ```bash
  swarm agent get_relationships <agent_id>
  ```

  Example:

  ```bash
  swarm agent get_relationships "1234-asd-3"
  ```

### Frameworks

- **Create a new framework:**

  ```bash
  swarm framework create --name <FrameworkName> --description <Description>
  ```

  Example:

  ```bash
  swarm framework create --name "SwarmBase" --description "Framework for AI-based agents"
  ```

- **List all frameworks:**

  ```bash
  swarm framework list
  ```

  Example:

  ```bash
  swarm framework list
  ```

- **Get a framework by ID:**

  ```bash
  swarm framework get <framework_id>
  ```

  Example:

  ```bash
  swarm framework get "5678-defg-3-3"
  ```

- **Update a framework:**

  ```bash
  swarm framework update <framework_id> --name <NewName> --description <NewDescription>
  ```

  Example:

  ```bash
  swarm framework update "5678-defg-3-3" --name "Better Framework" --description "Updated AI framework"
  ```

- **Delete a framework:**

  ```bash
  swarm framework delete <framework_id>
  ```

  Example:

  ```bash
  swarm framework delete "5678-defg-3-3"
  ```

### Swarms

- **Create a new swarm:**

  ```bash
  swarm swarm create --name <SwarmName> --description <Description>
  ```

  Example:

  ```bash
  swarm swarm create --name "ResearchSwarm" --description "Swarm focused on AI research"
  ```

- **List all swarms:**

  ```bash
  swarm swarm list
  ```

  Example:

  ```bash
  swarm swarm list
  ```

- **Get a swarm by ID:**

  ```bash
  swarm swarm get <swarm_id>
  ```

  Example:

  ```bash
  swarm swarm get "9101-ghij-4-4"
  ```

- **Update a swarm:**

  ```bash
  swarm swarm update <swarm_id> --name <NewName> --description <NewDescription>
  ```

  Example:

  ```bash
  swarm swarm update "9101-ghij-4-4" --name "Advanced Research Swarm" --description "Updated swarm for AI research"
  ```

- **Delete a swarm:**

  ```bash
  swarm swarm delete <swarm_id>
  ```

  Example:

  ```bash
  swarm swarm delete "9101-ghij-4-4"
  ```

### Tools

- **Create a new tool:**

  ```bash
  swarm tool create --name <ToolName> --description <Description> --version <Version> --code <Code> --inputs <Inputs> --outputs <Outputs> --extra_attributes <ExtraAttributes>
  ```

  Example:

  ```bash
  swarm tool create --name "DataAnalyzer" --description "Tool for analyzing data" --version "1.0" --code "print(f'I need answer for this question: {question}')" --inputs "{'name': 'question', 'type':'str', 'description': 'Question to be answered.'}" --outputs "{'name': 'result', 'type':'str', 'description': 'Analysis result'}" --extra_attributes "{'author': 'John Doe'}"
  ```

- **List all tools:**

  ```bash
  swarm tool list
  ```

  Example:

  ```bash
  swarm tool list
  ```

- **Get a tool by ID:**

  ```bash
  swarm tool get <tool_id>
  ```

  Example:

  ```bash
  swarm tool get "1213-ijkl-5-5"
  ```

- **Update a tool:**

  ```bash
  swarm tool update <tool_id> --name <NewName> --description <NewDescription> --version <NewVersion> --code <NewCode> --inputs <NewInputs> --outputs <NewOutputs> --extra_attributes <NewExtraAttributes>
  ```

  Example:

  ```bash
  swarm tool update "1213-ijkl-5-5" --name "Enhanced DataAnalyzer" --description "Updated tool for advanced data analysis" --version "2.0" --code "print(f'I need answer for this question: {question}. But this time the code is better')" --inputs "{'name': 'question', 'type':'str', 'description': 'Question to be answered.'}" --outputs "{'name': 'result', 'type':'str', 'description': 'Analysis result'}" --extra_attributes "{'author': 'Jane Doe'}"
  ```

  Example:

  ```bash
  swarm tool update "1213-ijkl-5-5" --name "Enhanced DataAnalyzer" --description "Updated tool for advanced data analysis"
  ```

- **Delete a tool:**

  ```bash
  swarm tool delete <tool_id>
  ```

  Example:

  ```bash
  swarm tool delete "1213-ijkl-5-5"
  ```
