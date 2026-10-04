"""Typed input/output compatibility used to augment semantic routing."""
from __future__ import annotations


EXTERNAL_SOURCES = {"user", "context", "artifact", "host"}


def normalize_binding(binding, *, direction: str) -> dict:
    if isinstance(binding, str):
        return {
            "name": binding,
            "required": False,
            "source": "legacy",
            "schema": {},
            "legacy": True,
        }
    if not isinstance(binding, dict):
        return {
            "name": "",
            "required": True,
            "source": None,
            "schema": {},
            "invalid": True,
        }
    return {
        "name": binding.get("name", ""),
        "required": binding.get("required", True),
        "source": binding.get("source"),
        "sensitive": binding.get("sensitive", False),
        "description": binding.get("description"),
        "schema": dict(binding.get("schema") or {}),
        "legacy": False,
    }


def schema_compatible(output_schema: dict, input_schema: dict) -> bool:
    """Conservative JSON-Schema compatibility for routing metadata."""
    if not input_schema:
        return True
    if not output_schema:
        return False

    input_type = input_schema.get("type")
    output_type = output_schema.get("type")
    if input_type and output_type and input_type != output_type:
        return False

    input_format = input_schema.get("format")
    output_format = output_schema.get("format")
    if input_format and output_format and input_format != output_format:
        return False

    input_enum = input_schema.get("enum")
    output_enum = output_schema.get("enum")
    if input_enum is not None and output_enum is not None:
        if not set(output_enum).issubset(set(input_enum)):
            return False

    return True


def output_satisfies_input(output_binding: dict, input_binding: dict) -> bool:
    output_binding = normalize_binding(output_binding, direction="output")
    input_binding = normalize_binding(input_binding, direction="input")
    if input_binding["name"] and output_binding["name"]:
        if input_binding["name"] != output_binding["name"]:
            return False
    return schema_compatible(output_binding["schema"], input_binding["schema"])


def contract_bindings(node: dict, field: str) -> list[dict]:
    direction = "input" if field == "inputs" else "output"
    return [normalize_binding(item, direction=direction) for item in node.get(field, [])]


def candidate_producers(graph: dict, consumer_id: str, input_binding: dict) -> list[dict]:
    """Return compatible producer candidates without inventing dependencies."""
    candidates = []
    for skill, node in graph.get("nodes", {}).items():
        if skill == consumer_id:
            continue
        for output in contract_bindings(node, "outputs"):
            if output_satisfies_input(output, input_binding):
                edge = next(
                    (
                        item for item in graph.get("edges", [])
                        if {item.get("from"), item.get("to")} == {skill, consumer_id}
                    ),
                    None,
                )
                candidates.append({
                    "skill": skill,
                    "output": output,
                    "edge": edge,
                    "contract_status": node.get("contract_status"),
                })
                break
    candidates.sort(key=lambda item: (0 if item["edge"] else 1, item["skill"]))
    return candidates


def resolve_required_inputs(
    graph: dict,
    selected: list[str],
    *,
    available_inputs=None,
    allowed_skills=None,
) -> dict:
    """Resolve required inputs and propose unique typed producer additions."""
    available_inputs = set(available_inputs or ())
    allowed_skills = set(allowed_skills) if allowed_skills is not None else None
    selected_set = set(selected)
    additions = []
    input_status = {}
    explanations = []

    for consumer in list(selected):
        node = graph.get("nodes", {}).get(consumer, {})
        for binding in contract_bindings(node, "inputs"):
            if not binding.get("required", True):
                continue
            name = binding.get("name") or "<unnamed>"
            key = f"{consumer}:{name}"

            if name in available_inputs:
                input_status[key] = {
                    "status": "available",
                    "source": "request-context",
                }
                continue

            source = binding.get("source")
            if source in EXTERNAL_SOURCES:
                input_status[key] = {
                    "status": "elicitable",
                    "source": source,
                }
                continue

            producers = [
                item for item in candidate_producers(graph, consumer, binding)
                if item["skill"] not in selected_set
                and (allowed_skills is None or item["skill"] in allowed_skills)
            ]
            selected_producers = [
                item for item in candidate_producers(graph, consumer, binding)
                if item["skill"] in selected_set
                and (allowed_skills is None or item["skill"] in allowed_skills)
            ]
            if selected_producers:
                producer = selected_producers[0]
                input_status[key] = {
                    "status": "available",
                    "source": "skill-output",
                    "producer": producer["skill"],
                    "output": producer["output"].get("name"),
                }
                explanations.append({
                    "consumer": consumer,
                    "input": name,
                    "producer": producer["skill"],
                    "output": producer["output"].get("name"),
                    "relationship": "typed-dataflow",
                })
                continue

            if len(producers) == 1:
                producer = producers[0]
                additions.append({
                    "producer": producer["skill"],
                    "consumer": consumer,
                    "input": name,
                    "output": producer["output"].get("name"),
                    "edge": producer["edge"],
                })
                selected_set.add(producer["skill"])
                input_status[key] = {
                    "status": "available",
                    "source": "skill-output",
                    "producer": producer["skill"],
                    "output": producer["output"].get("name"),
                }
                explanations.append({
                    "consumer": consumer,
                    "input": name,
                    "producer": producer["skill"],
                    "output": producer["output"].get("name"),
                    "relationship": "typed-dataflow",
                })
            elif len(producers) > 1:
                input_status[key] = {
                    "status": "elicitable",
                    "source": "ambiguous-producer",
                    "candidates": [item["skill"] for item in producers],
                }
            else:
                input_status[key] = {
                    "status": "unavailable",
                    "source": source or "skill-output",
                }

    return {
        "additions": additions,
        "inputs": input_status,
        "explanations": explanations,
    }
