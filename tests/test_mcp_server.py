import asyncio
from pathlib import Path

from solkraft.catalog import SkillCatalog
from solkraft.mcp_server import build_mcp_server


def test_mcp_exposes_search_route_and_read_only_skill_tools(tmp_path):
    root = tmp_path / "skills"
    folder = root / "writing-review"
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text("---\nname: writing-review\ndescription: Review writing for accuracy and clarity.\n---\n\n# Review\n", encoding="utf-8")
    server = build_mcp_server(SkillCatalog([root]))

    tools = asyncio.run(server.list_tools())
    names = {tool.name for tool in tools}

    assert {"search_skills", "route_request", "get_skill", "get_skill_contract", "get_contract_index"} <= names
    assert not {"run_skill", "execute_skill", "shell"} & names



def test_mcp_tools_publish_read_only_annotations(tmp_path):
    root = tmp_path / "skills"
    folder = root / "demo"
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Inspect a demo.\n---\n",
        encoding="utf-8",
    )
    server = build_mcp_server(SkillCatalog([root]))
    tools = asyncio.run(server.list_tools())
    assert tools
    for tool in tools:
        data = tool.annotations.model_dump(by_alias=True) if tool.annotations else {}
        assert data.get("readOnlyHint") is True
        assert data.get("openWorldHint") is False
