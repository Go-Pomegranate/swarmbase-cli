# Welcome to Swarmbase.ai Documentation

Swarmbase.ai is a powerful tool for managing multi-agents with various frameworks in one place. This documentation provides an overview of the `swarm` CLI tool, including installation, configuration, and usage.

## Installation

To get started with **Swarmbase.ai**, follow these steps:**Install the PyPi package with swarmbase-cli**

1. ```bash
   pip install swarmbase-cli
   ```
2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

## Configuration

Before using the CLI, set the base URL for the `swarm` API:

```bash
swarm --base-url http://127.0.0.1:5000
```

## Debug

Most commands support a `--debug` option that enables detailed logging, which can be very useful for troubleshooting:

```
swarm agent create --name "AgentName" --description "Description of the agent" --debug

```

## Usage

### Agents

- **Create a new agent:**

  ```bash
  swarm agent create --name "AgentName" --description "Description of the agent"
  ```
- **List all agents:**

  ```bash
  swarm agent list
  ```
- **Get an agent by ID:**

  ```bash
  swarm agent get <agent_id>
  ```
- **Update an agent:**

  ```bash
  swarm agent update <agent_id> --name "NewName" --description "New description"
  ```
- **Delete an agent:**

  ```bash
  swarm agent delete <agent_id>
  ```

* **Link two agents:**

  ```
  swarm agent link --agent1 <agent1_id> --agent2 <agent2_id> --relationship <relationship_type>

  ```
* **Unlink two agents:**

  ```
  swarm agent unlink --agent1 <agent1_id> --agent2 <agent2_id>
  ```
* **Get agent relationships:**

  ```
  swarm agent get_relationships <agent_id>

  ```

### Frameworks

- **Create a new framework:**

  ```bash
  swarm framework create --name "FrameworkName" --description "Description of the framework"
  ```
- **List all frameworks:**

  ```bash
  swarm framework list
  ```
- **Get a framework by ID:**

  ```bash
  swarm framework get <framework_id>
  ```
- **Update a framework:**

  ```bash
  swarm framework update <framework_id> --name "NewName" --description "New description"
  ```
- **Delete a framework:**

  ```bash
  swarm framework delete <framework_id>
  ```

### Swarms

- **Create a new swarm:**

  ```bash
  swarm swarm create --name "SwarmName" --description "Description of the swarm"
  ```
- **List all swarms:**

  ```bash
  swarm swarm list
  ```
- **Get a swarm by ID:**

  ```bash
  swarm swarm get <swarm_id>
  ```
- **Update a swarm:**

  ```bash
  swarm swarm update <swarm_id> --name "NewName" --description "New description"
  ```
- **Delete a swarm:**

  ```bash
  swarm swarm delete <swarm_id>
  ```

### Tools

- **Create a new tool:**

  ```bash
  swarm tool create --name "ToolName" --description "Description of the tool"
  ```
- **List all tools:**

  ```bash
  swarm tool list
  ```
- **Get a tool by ID:**

  ```bash
  swarm tool get <tool_id>
  ```
- **Update a tool:**

  ```bash
  swarm tool update <tool_id> --name "NewName" --description "New description"
  ```
- **Delete a tool:**

  ```bash
  swarm tool delete <tool_id>
  ```
