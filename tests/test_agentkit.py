"""Tests for deterministic agent tools (no external services needed)."""

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import agentkit


class ArtifactTests(unittest.TestCase):
    def test_spec_is_valid_when_proposed(self):
        result = agentkit.validate(
            "spec",
            {
                "id": "S-1",
                "project": "demo",
                "objective": "Reliable events",
                "status": "proposed",
                "in_scope": ["record events"],
                "out_of_scope": [],
                "acceptance_criteria": ["event is unique"],
                "unknowns": [],
            },
        )
        self.assertEqual(result, [])

    def test_approved_spec_requires_approval_reference(self):
        data = {
            "id": "S-1",
            "project": "demo",
            "objective": "Reliable events",
            "status": "approved",
            "in_scope": ["record events"],
            "out_of_scope": [],
            "acceptance_criteria": ["event is unique"],
            "unknowns": [],
        }
        self.assertTrue(agentkit.validate("spec", data))
        data["approval_reference"] = "https://example.com/decision-1"
        self.assertEqual(agentkit.validate("spec", data), [])

    def test_spec_rejects_missing_acceptance(self):
        self.assertTrue(
            agentkit.validate(
                "spec",
                {
                    "id": "S-1",
                    "project": "demo",
                    "objective": "Goal",
                    "status": "proposed",
                    "in_scope": [],
                    "out_of_scope": [],
                    "acceptance_criteria": [],
                    "unknowns": [],
                },
            )
        )

    def test_plan_detects_cycle(self):
        data = {
            "id": "P-1",
            "project": "demo",
            "objective": "something",
            "tasks": [
                {
                    "id": "A",
                    "owner": "dev",
                    "depends_on": ["B"],
                    "acceptance": ["done"],
                },
                {
                    "id": "B",
                    "owner": "qa",
                    "depends_on": ["A"],
                    "acceptance": ["tested"],
                },
            ],
        }
        self.assertTrue(any("ciclo" in e for e in agentkit.validate("plan", data)))

    def test_plan_detects_missing_dependency(self):
        data = {
            "id": "P-1",
            "project": "demo",
            "objective": "something",
            "tasks": [
                {
                    "id": "A",
                    "owner": "dev",
                    "depends_on": ["MISSING"],
                    "acceptance": ["done"],
                }
            ],
        }
        self.assertTrue(any("ausente" in e for e in agentkit.validate("plan", data)))

    def test_review_rejects_self_approval(self):
        data = {
            "commit": "abcdef1234567",
            "author": "agent1",
            "reviewer": "agent1",
            "status": "approved",
            "findings": [],
        }
        self.assertTrue(
            any("próprio autor" in e for e in agentkit.validate("review", data))
        )

    def test_review_rejects_blocker_with_approval(self):
        data = {
            "commit": "abcdef1234567",
            "author": "agent1",
            "reviewer": "agent2",
            "status": "approved",
            "findings": [
                {
                    "severity": "blocker",
                    "file": "src/a.py",
                    "scenario": "duplicate send",
                    "reason": "retry is not safe",
                    "fix": "make idempotent",
                }
            ],
        }
        self.assertTrue(
            any("contradiz" in e for e in agentkit.validate("review", data))
        )

    def test_qa_cannot_claim_pass_when_not_run(self):
        data = {
            "commit": "abcdef1234567",
            "developer": "dev",
            "executed_by": "qa",
            "environment": "sandbox",
            "status": "passed",
            "scenarios": [{"id": "T1", "result": "not_run", "evidence": ""}],
        }
        self.assertTrue(any("todos" in e for e in agentkit.validate("qa", data)))

    def test_qa_requires_evidence_for_pass(self):
        data = {
            "commit": "abcdef1234567",
            "developer": "dev",
            "executed_by": "qa",
            "environment": "sandbox",
            "status": "passed",
            "scenarios": [{"id": "T1", "result": "passed", "evidence": ""}],
        }
        self.assertTrue(any("evidência" in e for e in agentkit.validate("qa", data)))

    def test_reject_unknown_document_kind(self):
        self.assertTrue(agentkit.validate("something", {}))


class GateTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        self.sha = "abcdef1234567890"

    def tearDown(self):
        self.folder.cleanup()

    def write(self, kind, data):
        (self.root / f"{kind}.json").write_text(json.dumps(data), encoding="utf-8")

    def valid_bundle(self):
        self.write(
            "review",
            {
                "commit": self.sha,
                "author": "developer",
                "reviewer": "reviewer",
                "status": "approved",
                "findings": [],
            },
        )
        self.write(
            "qa",
            {
                "commit": self.sha,
                "developer": "developer",
                "executed_by": "tester",
                "environment": "ci",
                "status": "passed",
                "scenarios": [
                    {"id": "T1", "result": "passed", "evidence": "CI / test"}
                ],
            },
        )
        self.write(
            "ci",
            {
                "commit": self.sha,
                "status": "passed",
                "url": "https://github.com/test/checks/1",
            },
        )

    def test_gate_never_grants_human_approval(self):
        self.valid_bundle()
        output = agentkit.release_gate(self.root)
        self.assertEqual(output["status"], "READY_FOR_HUMAN_DECISION")
        self.assertTrue(output["human_approval_required"])
        self.assertFalse(output["errors"])

    def test_gate_rejects_mismatch_commit(self):
        self.valid_bundle()
        data = agentkit.load(self.root / "qa.json")
        data["commit"] = "fedcba9876543210"
        self.write("qa", data)
        output = agentkit.release_gate(self.root)
        self.assertEqual(output["status"], "BLOCKED")
        self.assertTrue(any("mesmo commit" in e for e in output["errors"]))

    def test_gate_rejects_missing_file(self):
        self.valid_bundle()
        (self.root / "ci.json").unlink()
        self.assertEqual(agentkit.release_gate(self.root)["status"], "BLOCKED")

    def test_gate_rejects_failed_ci(self):
        self.valid_bundle()
        data = agentkit.load(self.root / "ci.json")
        data["status"] = "failed"
        self.write("ci", data)
        self.assertEqual(agentkit.release_gate(self.root)["status"], "BLOCKED")


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)

    def tearDown(self):
        self.folder.cleanup()

    def file(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_detects_local_import_cycle(self):
        self.file("a.py", "import b\n")
        self.file("b.py", "import a\n")
        report = agentkit.inspect_project(self.root)
        self.assertEqual(report["cycles"], [["a", "b"]])
        self.assertEqual(len(report["static_import_edges"]), 2)

    def test_does_not_see_stdlib_as_project_dependency(self):
        self.file("app.py", "import json\nimport pathlib\n")
        report = agentkit.inspect_project(self.root)
        self.assertEqual(report["static_import_edges"], [])

    def test_skips_venv_and_symlinked_modules(self):
        self.file(".venv/bad.py", "import app\n")
        self.file("app.py", "import json\n")
        report = agentkit.inspect_project(self.root)
        self.assertEqual(report["python_modules"], 1)

    def test_unknown_project_is_error(self):
        with self.assertRaisesRegex(ValueError, "inexistente"):
            agentkit.inspect_project(self.root / "missing")

    def test_syntax_failure_returns_warning(self):
        self.file("bad.py", "def broken(:\n")
        report = agentkit.inspect_project(self.root)
        self.assertEqual(report["python_modules"], 0)
        self.assertEqual(len(report["parse_warnings"]), 1)


class ScopeTests(unittest.TestCase):
    def test_scope_allowlist(self):
        with patch.object(
            agentkit,
            "changed_files",
            return_value=[
                "src/api.py",
                "README.md",
            ],
        ):
            output = agentkit.scope_check(Path("."), "main", ["src/*.py"])
        self.assertEqual(output["status"], "OUT_OF_SCOPE")
        self.assertEqual(output["unexpected"], ["README.md"])

    def test_scope_passes_when_all_paths_match(self):
        with patch.object(agentkit, "changed_files", return_value=["src/api.py"]):
            output = agentkit.scope_check(Path("."), "main", ["src/*.py"])
        self.assertEqual(output["status"], "IN_SCOPE")

    def test_changed_files_reports_git_error(self):
        proc = subprocess.CompletedProcess(
            args=[], returncode=1, stdout=b"", stderr=b"invalid ref"
        )
        with patch.object(agentkit.subprocess, "run", return_value=proc):
            with self.assertRaisesRegex(ValueError, "invalid ref"):
                agentkit.changed_files(Path("."), "nope")


class BlackTests(unittest.TestCase):
    def test_black_check_has_no_write_flag_by_default(self):
        proc = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch.object(agentkit.subprocess, "run", return_value=proc) as run:
            output, code = agentkit.black_check(Path("."), False, None)
        self.assertEqual(code, 0)
        args = run.call_args.args[0]
        self.assertEqual(
            args[:5], [agentkit.sys.executable, "-m", "black", "--check", "--diff"]
        )
        self.assertEqual(output["mode"], "CHECK_ONLY")

    def test_black_skips_when_no_changed_python_files(self):
        with patch.object(agentkit, "changed_files", return_value=["README.md"]):
            output, code = agentkit.black_check(Path("."), False, "main")
        self.assertEqual(code, 0)
        self.assertEqual(output["status"], "SKIPPED_NO_PYTHON_CHANGES")

    def test_black_apply_requires_explicit_mode(self):
        proc = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        with patch.object(agentkit.subprocess, "run", return_value=proc) as run:
            agentkit.black_check(Path("."), True, None)
        self.assertNotIn("--check", run.call_args.args[0])
        self.assertNotIn("--diff", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
