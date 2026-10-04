from solkraft.contracts import apply_contracts, contract_from_declaration, contract_from_node, excluded_effects


def test_quoted_exclusion_does_not_count():
    assert excluded_effects('Inspect the repo. The log says "do not deploy" as a quote.') == []
    assert excluded_effects("Inspect the repo. Do not deploy anything.") == ["deploy"]


def test_read_only_graph_node_is_a_declared_contract():
    contract = contract_from_node({
        "effect": False,
        "inputs": ["user objective"],
        "exit_evidence": "Observed behavior matches the request.",
    })
    assert contract["declared"] is True
    assert contract["side_effects"] == []
    assert contract["auth_scope"] == "none"
    assert contract["test_contract"] == "Observed behavior matches the request."


def test_frontmatter_must_state_all_four_fields():
    missing = contract_from_declaration({"inputs": ["repository"], "side_effects": []})
    assert missing["declared"] is False
    stated = contract_from_declaration({
        "inputs": ["repository"],
        "side_effects": [],
        "auth_scope": "read",
        "test_contract": "Cited files match the requested inspection.",
    })
    assert stated["declared"] is True


def test_undeclared_skill_is_not_an_automatic_pick():
    graph = {"nodes": {"mystery": {"description": "Does something."}}}
    result = apply_contracts({"selected": ["mystery"], "stages": [{"selected": ["mystery"]}]}, graph, "Inspect the repository.")
    assert result["selected"] == []
    assert "did not state" in result["contract_rejections"][0]["reasons"][0]


def test_explicit_name_can_still_select_an_undeclared_skill():
    graph = {"nodes": {"mystery": {"description": "Does something."}}}
    result = apply_contracts({"selected": ["mystery"], "stages": []}, graph, "Use mystery.", explicit=["mystery"])
    assert result["selected"] == ["mystery"]
    assert result["contracts"]["mystery"]["explicit_undeclared"] is True


def test_declared_side_effect_is_rejected_without_loading_a_body():
    graph = {"nodes": {
        "deployer": {
            "effect": True,
            "side_effects": ["deploy"],
            "auth_scope": "external-effect",
            "test_contract": "Deployment record matches the requested target.",
            "inputs": ["target"],
        },
        "reader": {
            "effect": False,
            "inputs": ["repository"],
            "exit_evidence": "Inspection cites files and revisions.",
        },
    }}
    result = apply_contracts(
        {"selected": ["reader", "deployer"], "stages": [{"selected": ["reader", "deployer"]}], "skills": [
            {"id": "reader"}, {"id": "deployer"}]},
        graph,
        "Inspect the repository. Do not deploy anything.",
    )
    assert result["selected"] == ["reader"]
    assert result["contract_rejections"][0]["id"] == "deployer"
    assert result["contracts"]["reader"]["test_contract"]
    assert result["execution_authorized"] is False
    assert result["stages"][0]["selected"] == ["reader"]


def test_auth_scope_is_a_selection_constraint():
    graph = {"nodes": {"writer": {
        "side_effects": [],
        "auth_scope": "write-local",
        "test_contract": "Diff matches the requested change.",
        "inputs": ["repository"],
    }}}
    result = apply_contracts({"selected": ["writer"], "stages": []}, graph,
                             "Implement the fix.", allowed_auth="read")
    assert result["selected"] == []
    assert result["selection_status"] == "abstained"
    assert "above read" in result["contract_rejections"][0]["reasons"][0]
