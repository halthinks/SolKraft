"""Exercise the distributable client's real stdio contract, outside the checkout."""
import asyncio
import json
import os
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]


def test_plugin_routes_and_retrieves_over_real_stdio(tmp_path):
    plugin = Path(os.environ.get("SOLKRAFT_TEST_PLUGIN_ROOT", ROOT / "plugins" / "solkraft"))
    manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text())
    config = json.loads((plugin / manifest["mcpServers"]).read_text())["mcpServers"]["solkraft"]
    assert (plugin / manifest["skills"] / "solkraft/SKILL.md").is_file()

    async def exercise():
        params = StdioServerParameters(command=config["command"], args=config["args"], cwd=str(tmp_path))
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                assert {t.name for t in tools.tools} == {
                    "search_skills", "route_request", "get_skill", "get_skill_resource", "get_selection_graph"
                }
                async def call(name, arguments):
                    result = await session.call_tool(name, arguments)
                    assert not result.isError, result
                    return result.structuredContent or json.loads(result.content[0].text)
                found = await call("search_skills", {"query": "software test", "limit": 5})
                assert found["items"]
                route = await call("route_request", {
                    "objective": "Draft PR", "context": {"stage": "repository-release-gate"}
                })
                assert route["execution_authorized"] is False
                assert "solforge-workflow-software-test" in str(route["selected"])
                skill = await call("get_skill", {"skill_id": "solforge-workflow-software-test"})
                assert "content" in skill
                resource = await call("get_skill_resource", {
                    "skill_id": "solforge", "resource": "references/native-execution.md"
                })
                assert "content" in resource
                graph = await call("get_selection_graph", {})
                assert len(graph["nodes"]) >= 173
    asyncio.run(exercise())
