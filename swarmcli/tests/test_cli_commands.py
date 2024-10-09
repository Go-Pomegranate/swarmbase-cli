import pytest
import requests
from click.testing import CliRunner
from swarmcli import cli_commands  # noqa: F401
from swarmcli.utils import cli


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def base_url():
    return "http://127.0.0.1:5000"


@pytest.fixture(scope="module")
def agent_data():
    return {
        "name": "CreatedTestAgent",
        "description": "CreatedTestAgent Description",
    }


@pytest.fixture(scope="module")
def agent_data2():
    return {
        "name": "CreatedTestAgent2",
        "description": "CreatedTestAgent2 Description",
    }


def create_agent(base_url, name, description):
    response = requests.post(
        f"{base_url}/api/agents",
        json={"name": name, "description": description},
    )
    print(
        f"Create Agent: Status Code: {response.status_code}, Response Content: {response.text}",
    )
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print(
            f"Create Agent: Response content is not valid JSON: {response.text}",
        )
        return None
    return response_json


@pytest.fixture()
def create_test_agent(live_server, agent_data):
    agent = create_agent(
        live_server,
        agent_data["name"],
        agent_data["description"],
    )
    assert agent is not None
    assert "agent" in agent
    assert agent["agent"]["name"] == agent_data["name"]
    return agent["agent"]["id"]


@pytest.fixture()
def create_test_agent2(live_server, agent_data2):
    agent = create_agent(
        live_server,
        agent_data2["name"],
        agent_data2["description"],
    )
    assert agent is not None
    assert "agent" in agent
    assert agent["agent"]["name"] == agent_data2["name"]
    return agent["agent"]["id"]


@pytest.fixture(scope="module")
def framework_data():
    return {
        "name": "CreatedTestSwarm",
        "description": "CreatedTestSwarm Description",
    }


def create_framework(base_url, name, description):
    response = requests.post(
        f"{base_url}/api/frameworks",
        json={"name": name, "description": description},
    )
    print(
        f"Create Framework: Status Code: {response.status_code}, Response Content: {response.text}",
    )
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print(
            f"Create Framework: Response content is not valid JSON: {response.text}",
        )
        return None
    return response_json


@pytest.fixture()
def create_test_framework(live_server, framework_data):
    framework = create_framework(
        live_server,
        framework_data["name"],
        framework_data["description"],
    )
    assert framework is not None
    assert "framework" in framework
    assert framework["framework"]["name"] == framework_data["name"]
    return framework["framework"]["id"]


@pytest.fixture(scope="module")
def swarm_data():
    return {
        "name": "CreatedTestSwarm",
        "description": "CreatedTestSwarm Description",
    }


def create_swarm(base_url, name, description):
    response = requests.post(
        f"{base_url}/api/swarms",
        json={"name": name, "description": description},
    )
    print(
        f"Create Swarm: Status Code: {response.status_code}, Response Content: {response.text}",
    )
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print(
            f"Create Swarm: Response content is not valid JSON: {response.text}",
        )
        return None
    return response_json


@pytest.fixture()
def create_test_swarm(live_server, swarm_data):
    swarm = create_swarm(
        live_server,
        swarm_data["name"],
        swarm_data["description"],
    )
    assert swarm is not None
    assert "swarm" in swarm
    assert swarm["swarm"]["name"] == swarm_data["name"]
    return swarm["swarm"]["id"]


@pytest.fixture(scope="module")
def tool_data():
    return {
        "name": "CreatedTestTool",
        "description": "CreatedTestTool Description",
        "version": "0.0.1",
        "code": "print('tool')",
        "extra_attributes": None,
    }


def create_tool(base_url, name, description, version, code, extra_attributes):
    response = requests.post(
        f"{base_url}/api/tools",
        json={
            "name": name,
            "description": description,
            "version": version,
            "code": code,
            "extra_attributes": extra_attributes,
        },
    )
    print(
        f"Create tool: Status Code: {response.status_code}, Response Content: {response.text}",
    )
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print(
            f"Create tool: Response content is not valid JSON: {response.text}",
        )
        return None
    return response_json


@pytest.fixture()
def create_test_tool(live_server, tool_data):
    tool = create_tool(
        live_server,
        tool_data["name"],
        tool_data["description"],
        tool_data["version"],
        tool_data["code"],
        tool_data["extra_attributes"],
    )
    assert tool is not None
    assert "tool" in tool
    assert tool["tool"]["name"] == tool_data["name"]
    return tool["tool"]["id"]


def test_agent_create(live_server, runner):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "agent",
            "create",
            "--name",
            "test_agent",
            "--description",
            "A test agent",
        ],
    )
    assert result.exit_code == 0
    assert "test_agent" in result.output


def test_agent_list(runner, live_server):
    result = runner.invoke(cli, ["--base-url", live_server, "agent", "list"])
    assert result.exit_code == 0
    assert "test_agent" in result.output


def test_agent_get(runner, live_server, create_test_agent):
    result = runner.invoke(
        cli,
        ["--base-url", live_server, "agent", "get", create_test_agent],
    )
    assert result.exit_code == 0
    assert "CreatedTestAgent" in result.output


def test_agent_update(runner, live_server, create_test_agent):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "agent",
            "update",
            create_test_agent,
            "--name",
            "updated_agent",
            "--description",
            "Updated description",
        ],
    )
    assert result.exit_code == 0
    assert "updated_agent" in result.output


def test_agent_delete(runner, live_server, create_test_agent):
    result = runner.invoke(
        cli,
        ["--base-url", live_server, "agent", "delete", create_test_agent],
    )
    assert result.exit_code == 0
    assert result.output == "\n"


def test_agent_link(
    runner,
    live_server,
    create_test_agent,
    create_test_agent2,
):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "agent",
            "link",
            "--agent1",
            create_test_agent,
            "--agent2",
            create_test_agent2,
            "--relationship",
            "supervises",
        ],
    )
    print(f"Link Agent Response: {result.output}")
    assert result.exit_code == 0
    assert create_test_agent in result.output
    assert create_test_agent2 in result.output


def test_agent_get_relationships(
    runner,
    live_server,
    create_test_agent,
    create_test_agent2,
):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "agent",
            "get-relationships",
            create_test_agent,
        ],
    )
    assert result.exit_code == 0
    assert create_test_agent2 in result.output


def test_agent_unlink(
    runner,
    live_server,
    create_test_agent,
    create_test_agent2,
):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "agent",
            "unlink",
            "--agent1",
            create_test_agent,
            "--agent2",
            create_test_agent2,
        ],
    )
    assert result.exit_code == 0
    assert result.output == "\n"


def test_framework_create(runner, live_server):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "framework",
            "create",
            "--name",
            "test_framework",
            "--description",
            "A test framework",
        ],
    )
    assert result.exit_code == 0
    assert "test_framework" in result.output


def test_framework_list(runner, base_url):
    result = runner.invoke(cli, ["--base-url", base_url, "framework", "list"])
    assert result.exit_code == 0
    assert "test_framework" in result.output


def test_framework_get(runner, base_url, create_test_framework):
    result = runner.invoke(
        cli,
        ["--base-url", base_url, "framework", "get", create_test_framework],
    )
    assert result.exit_code == 0
    assert "CreatedTestSwarm" in result.output


def test_framework_update(runner, base_url, create_test_framework):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            base_url,
            "framework",
            "update",
            create_test_framework,
            "--name",
            "updated_framework",
            "--description",
            "Updated description",
        ],
    )
    assert result.exit_code == 0
    assert "updated_framework" in result.output


def test_framework_delete(runner, live_server, create_test_framework):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "framework",
            "delete",
            create_test_framework,
        ],
    )
    assert result.exit_code == 0
    assert "\n" in result.output


def test_swarm_create(runner, live_server):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "swarm",
            "create",
            "--name",
            "test_swarm",
            "--extra_attributes",
            "{'version': 1.0.1}",
        ],
    )
    assert result.exit_code == 0
    assert "test_swarm" in result.output


def test_swarm_list(runner, live_server):
    result = runner.invoke(cli, ["--base-url", live_server, "swarm", "list"])
    assert result.exit_code == 0
    assert "test_swarm" in result.output


def test_swarm_get(runner, live_server, create_test_swarm):
    result = runner.invoke(
        cli,
        ["--base-url", live_server, "swarm", "get", create_test_swarm],
    )
    assert result.exit_code == 0
    assert "CreatedTestSwarm" in result.output


def test_swarm_update(runner, live_server, create_test_swarm):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "swarm",
            "update",
            create_test_swarm,
            "--name",
            "updated_swarm",
            "--description",
            "Updated description",
        ],
    )
    assert result.exit_code == 0
    assert "updated_swarm" in result.output


def test_swarm_delete(runner, live_server, create_test_swarm):
    result = runner.invoke(
        cli,
        ["--base-url", live_server, "swarm", "delete", create_test_swarm],
    )
    assert result.exit_code == 0
    assert "\n" in result.output


def test_tool_create(runner, live_server):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "tool",
            "create",
            "--name",
            "test_tool",
            "--description",
            "A test tool",
        ],
    )
    assert result.exit_code == 0
    assert "test_tool" in result.output


def test_tool_list(runner, live_server):
    result = runner.invoke(cli, ["--base-url", live_server, "tool", "list"])
    assert result.exit_code == 0
    assert "test_tool" in result.output


def test_tool_get(runner, live_server, create_test_tool):
    result = runner.invoke(
        cli,
        ["--base-url", live_server, "tool", "get", create_test_tool],
    )
    assert result.exit_code == 0
    assert "CreatedTestTool" in result.output


def test_tool_update(runner, live_server, create_test_tool):
    result = runner.invoke(
        cli,
        [
            "--base-url",
            live_server,
            "tool",
            "update",
            create_test_tool,
            "--name",
            "updated_tool",
            "--description",
            "Updated description",
        ],
    )
    assert result.exit_code == 0
    assert "CreatedTestTool" in result.output


def test_tool_delete(runner, live_server, create_test_tool):
    result = runner.invoke(
        cli,
        ["--base-url", live_server, "tool", "delete", create_test_tool],
    )
    assert result.exit_code == 0
    assert "\n" in result.output
