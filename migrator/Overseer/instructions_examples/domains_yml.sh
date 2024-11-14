Domains:
    - tools
        - paths: [List of paths to where tools are stored]
        - entities: [List of tools]
        - tool_source:
            - type: [Type of source, can be "local" or "external".]
            - name: [Name of the source, can be "langchain", "local", "other"]
    - agents
        - paths: [List of paths to where agents are stored]
        - entities: [List of agents]
    - frameworks
        - paths: [List of paths to where frameworks are stored]
        - entities: [Pick only one from the list: "swarm-agency", "LangGraph", "autogen", "other"]
    - swarms
        - paths: [List of paths to where swarms are stored]
    Helper methods:
    - paths: [List of paths to where helper methods created my the user are stored]
    - entities: [List of helper methods names]