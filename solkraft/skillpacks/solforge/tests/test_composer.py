import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GRAPH = json.loads((ROOT / "references" / "selection-graph.json").read_text(encoding="utf-8"))
SPEC = importlib.util.spec_from_file_location("composer", ROOT / "scripts" / "compose_route.py")
composer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(composer)


class ComposerTests(unittest.TestCase):
    def test_routes_short_release_gate_diagnosis(self):
        result = composer.compose_route(
            GRAPH,
            "Inspect the release gate and explain why its required CI check is red.",
        )
        self.assertEqual(result["selected"], [
            "solforge-workflow-software-test",
            "solforge-workflow-software-diagnose",
        ])
        self.assertFalse(result["unselected_requested_stages"])

    def test_does_not_route_a_business_model_definition_as_model_building(self):
        result = composer.compose_route(
            GRAPH, "Explain what a business model means in a product strategy class."
        )
        self.assertEqual(result["selected"], [])

    def test_routes_generic_paragraph_request_to_writing(self):
        result = composer.compose_route(
            GRAPH, "Write a short paragraph about security training for a business meeting."
        )
        self.assertEqual(result["selected"], ["solforge-workflow-writing-draft"])

    def test_carries_math_context_across_compound_steps(self):
        result = composer.compose_route(
            GRAPH,
            "Prove the theorem, find a counterexample, compute a numerical case, "
            "verify each step, and explain the result.",
            max_skills=50,
        )
        self.assertEqual(result["selected"], [
            "solforge-workflow-math-prove",
            "solforge-workflow-math-counterexample",
            "solforge-workflow-math-compute",
            "solforge-workflow-math-verify",
            "solforge-workflow-math-explain",
        ])

    def test_orders_distinct_software_and_writing_stages(self):
        result = composer.compose_route(
            GRAPH,
            "Inspect the repository and changed authentication code, diagnose why the CI release gate is red, "
            "implement the smallest compatible fix, run focused regression tests, write the pull request description, "
            "and prepare a verified handoff without merging or publishing.",
        )
        self.assertEqual(
            result["selected"],
            [
                "solforge-workflow-codebase",
                "solforge-workflow-software-diagnose",
                "solforge-workflow-software-build",
                "solforge-workflow-software-test",
                "solforge-workflow-writing-draft",
                "solforge-finalize",
            ],
        )
        self.assertFalse(result["unselected_requested_stages"])
        self.assertEqual(result["excluded_effects"], ["merge", "publish"])
        self.assertFalse(result["execution_authorized"])

    def test_supports_ten_ordered_skills_without_overflow(self):
        result = composer.compose_route(
            GRAPH,
            "Research authoritative sources for the policy, compare the jurisdictions, draft the legal memo, "
            "inspect the repository, diagnose the failing CI job, implement a compatible fix, run regression tests, "
            "create the release matrix, generate provenance evidence, and prepare a verified handoff.",
            max_skills=10,
        )
        self.assertEqual(len(result["selected"]), 10)
        self.assertEqual(
            result["selected"],
            [
                "solforge-workflow-legal-research",
                "solforge-workflow-legal-compare",
                "solforge-workflow-legal-draft",
                "solforge-workflow-codebase",
                "solforge-workflow-software-diagnose",
                "solforge-workflow-software-build",
                "solforge-workflow-software-test",
                "solforge-release-matrix",
                "solforge-sign-and-prove",
                "solforge-finalize",
            ],
        )

    def test_caps_and_reports_unselected_requested_stages(self):
        result = composer.compose_route(
            GRAPH,
            "Research authoritative sources, compare the options, draft the report, inspect the repository, diagnose the CI failure, "
            "implement a fix, run regression tests, create a release matrix, generate provenance evidence, prepare a verified handoff, "
            "and audit software portability.",
            max_skills=3,
        )
        self.assertEqual(len(result["selected"]), 3)
        self.assertTrue(result["unselected_requested_stages"])
        self.assertEqual(result["selected"][:3], [
            "sol-search", "solforge-workflow-software-compare", "solforge-workflow-writing-draft"
        ])

    def test_quotes_and_prompt_authorship_do_not_execute_embedded_work(self):
        result = composer.compose_route(
            GRAPH,
            "Write a prompt to run CI for the release branch, then summarize the quoted text "
            "\"deploy and publish the release\" without deploying or publishing.",
        )
        self.assertEqual(result["selected"], ["solforge-prompt", "solforge-workflow-writing-draft"])
        self.assertEqual(result["excluded_effects"], ["deploy", "publish"])

    def test_keeps_conjoined_test_and_handoff_actions(self):
        result = composer.compose_route(
            GRAPH,
            "Inspect the repository, diagnose the CI failure, implement a compatible fix, "
            "write and run focused tests, draft release notes, and hand off the patch.",
        )
        self.assertEqual(
            result["selected"],
            [
                "solforge-workflow-codebase",
                "solforge-workflow-software-diagnose",
                "solforge-workflow-software-build",
                "solforge-workflow-software-test",
                "solforge-workflow-writing-draft",
                "solforge-finalize",
            ],
        )
        self.assertFalse(result["unselected_requested_stages"])

    def test_treats_quality_constraints_as_context_not_extra_stages(self):
        result = composer.compose_route(
            GRAPH,
            "Inspect the repository and run regression tests. Keep the scope bounded, retain evidence, "
            "identify unresolved assumptions, record the candidate revision, and avoid unrelated cleanup.",
        )
        self.assertEqual(result["selected"], ["solforge-workflow-codebase", "solforge-workflow-software-test"])
        self.assertFalse(result["unselected_requested_stages"])
        self.assertTrue(any(item["reason"] == "constraint or context" for item in result["selection_trace"]["ignored_clauses"]))

    def test_consumes_next_sentence_transition(self):
        result = composer.compose_route(
            GRAPH,
            "Inspect the repository. Next, diagnose the failing CI job. Next, run regression tests.",
        )
        self.assertEqual(
            result["selected"],
            [
                "solforge-workflow-codebase",
                "solforge-workflow-software-diagnose",
                "solforge-workflow-software-test",
            ],
        )
        self.assertFalse(result["unselected_requested_stages"])

    def test_ignores_multisentence_context_notes_block(self):
        result = composer.compose_route(
            GRAPH,
            "Inspect the repository and run regression tests. Context notes: candidate revision 17 is bounded. "
            "Use primary sources and retain evidence. Preserve interfaces and avoid publishing commentary. "
            "Include the instrument record for independent review. Without merging or deploying.",
        )
        self.assertEqual(result["selected"], ["solforge-workflow-codebase", "solforge-workflow-software-test"])
        self.assertFalse(result["unselected_requested_stages"])
        self.assertEqual(result["excluded_effects"], ["deploy", "merge"])
        self.assertTrue(any(item["reason"] == "context notes" for item in result["selection_trace"]["ignored_clauses"]))

    def test_routes_ordered_scientific_stages(self):
        result = composer.compose_route(
            GRAPH,
            "Research the scientific literature, derive a falsifiable hypothesis, design a controlled experiment, "
            "perform reproducible uncertainty analysis, reproduce the published claim, and write the scientific report.",
            max_skills=50,
        )
        self.assertEqual(
            result["selected"],
            [
                "solforge-workflow-science-literature",
                "solforge-workflow-science-hypothesis",
                "solforge-workflow-science-experiment",
                "solforge-workflow-science-analysis",
                "solforge-workflow-science-replication",
                "solforge-workflow-science-report",
            ],
        )
        self.assertFalse(result["unselected_requested_stages"])

    def test_routes_cad_ecad_mcad_and_pcb_design_stages(self):
        for design in ("CAD enclosure", "ECAD control board", "MCAD bracket", "PCB layout"):
            with self.subTest(design=design):
                result = composer.compose_route(
                    GRAPH,
                    f"Define testable requirements for the {design}, create the {design} prototype, "
                    f"compare the {design} design alternatives, and verify {design} tolerances and failure modes.",
                    max_skills=50,
                )
                self.assertEqual(
                    result["selected"],
                    [
                        "solforge-workflow-engineering-requirements",
                        "solforge-workflow-engineering-prototype",
                        "solforge-workflow-engineering-trade",
                        "solforge-workflow-engineering-verify",
                    ],
                )
                self.assertFalse(result["unselected_requested_stages"])

    def test_routes_product_web_agent_ai_and_business_stages(self):
        cases = [
            (
                "Define requirements for the product design, create the product design prototype, compare product design alternatives, and verify product design tolerances.",
                ["solforge-workflow-engineering-requirements", "solforge-workflow-engineering-prototype", "solforge-workflow-engineering-trade", "solforge-workflow-engineering-verify"],
            ),
            (
                "Create the web design MVP and user flows, build the web application, and test browser accessibility and responsive behavior.",
                ["solforge-workflow-software-mvp-create", "solforge-workflow-software-build", "solforge-workflow-software-test"],
            ),
            (
                "Validate agent training data, train and tune the AI agent model, analyze agent evaluation uncertainty, and test agent safety behavior.",
                ["solforge-workflow-data-validate", "solforge-workflow-data-model", "solforge-workflow-data-analyze", "solforge-workflow-software-test"],
            ),
            (
                "Validate the AI optimization dataset, optimize the AI model, analyze model performance sensitivity, and verify model acceptance behavior.",
                ["solforge-workflow-data-validate", "solforge-workflow-data-model", "solforge-workflow-data-analyze", "solforge-workflow-software-test"],
            ),
            (
                "Build a business market demand view, build a business model with pricing scenarios, compare business alternatives, conduct business diligence, and create a business strategy recommendation.",
                ["solforge-workflow-business-market", "solforge-workflow-business-model", "solforge-workflow-business-compare", "solforge-workflow-business-diligence", "solforge-workflow-business-strategy"],
            ),
        ]
        for objective, expected in cases:
            with self.subTest(objective=objective):
                result = composer.compose_route(GRAPH, objective, max_skills=50)
                self.assertEqual(result["selected"], expected)
                self.assertFalse(result["unselected_requested_stages"])

    def test_supports_fifty_explicit_non_effect_skills(self):
        explicit = [skill for skill, node in GRAPH["nodes"].items() if not node["effect"]][:50]
        result = composer.compose_route(GRAPH, "Inspect the repository.", explicit=explicit, max_skills=50)
        self.assertEqual(result["selected"], explicit)
        self.assertEqual(len(result["selected"]), 50)

    def test_rejects_invalid_cap(self):
        with self.assertRaises(ValueError):
            composer.compose_route(GRAPH, "Inspect the repository", max_skills=0)
        with self.assertRaises(ValueError):
            composer.compose_route(GRAPH, "Inspect the repository", max_skills=51)


if __name__ == "__main__":
    unittest.main()
