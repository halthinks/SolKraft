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

    assert {"search_skills", "route_request", "get_skill"} <= names
    assert not {"run_skill", "execute_skill", "shell"} & names
