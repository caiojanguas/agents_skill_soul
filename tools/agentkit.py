#!/usr/bin/env python3
"""Deterministic, read-only evidence helpers for the agent team.

Only 'black --apply' changes files, and only after an explicit CLI flag.
This module is not an authorization mechanism for deployment.
"""

import argparse
import ast
import fnmatch
import json
import re
import subprocess
import sys
from pathlib import Path

EXCLUDED = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".mypy_cache",
    ".pytest_cache",
    "dist",
    "build",
}
SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{7,40}$")
ROLES = {"lider-po", "arquiteto", "dev", "reviewer", "qa", "sustentacao"}


def report(payload, exit_code=0):
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return exit_code


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"Não foi possível ler JSON {path}: {exc}") from exc


def validate(kind, data):
    """Validate structure and consistency, never the semantic truth of claims."""
    errors = []
    if not isinstance(data, dict):
        return ["O artefato precisa ser um objeto JSON."]

    def string(key):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"{key}: texto obrigatório.")

    def items(key, nonempty=False):
        value = data.get(key)
        if not isinstance(value, list) or (nonempty and not value):
            errors.append(f"{key}: lista obrigatória.")
            return []
        return value

    if kind == "spec":
        for key in ("id", "project", "objective", "status"):
            string(key)
        if data.get("status") not in {"proposed", "approved"}:
            errors.append("status: use proposed ou approved.")
        for key in ("in_scope", "out_of_scope", "acceptance_criteria", "unknowns"):
            for item in items(key, nonempty=key == "acceptance_criteria"):
                if not isinstance(item, str) or not item.strip():
                    errors.append(f"{key}: itens precisam ser textos não vazios.")
        if data.get("status") == "approved" and not (
            isinstance(data.get("approval_reference"), str)
            and data["approval_reference"].strip()
        ):
            errors.append(
                "approval_reference: link/registro obrigatório; "
                "é necessária conferência humana no runtime."
            )

    elif kind == "plan":
        for key in ("id", "project", "objective"):
            string(key)
        tasks = items("tasks", nonempty=True)
        ids = set()
        graph = {}
        for index, task in enumerate(tasks):
            if not isinstance(task, dict):
                errors.append(f"tasks[{index}]: objeto obrigatório.")
                continue
            task_id = task.get("id")
            if not isinstance(task_id, str) or not task_id.strip():
                errors.append(f"tasks[{index}].id: texto obrigatório.")
                continue
            if task_id in ids:
                errors.append(f"tasks: ID duplicado {task_id}.")
            ids.add(task_id)
            if task.get("owner") not in ROLES:
                errors.append(f"{task_id}: owner desconhecido.")
            deps = task.get("depends_on")
            if not isinstance(deps, list) or any(
                not isinstance(dep, str) for dep in deps
            ):
                errors.append(f"{task_id}: depends_on precisa ser lista de IDs.")
                deps = []
            graph[task_id] = deps
            criteria = task.get("acceptance")
            if (
                not isinstance(criteria, list)
                or not criteria
                or any(
                    not isinstance(item, str) or not item.strip() for item in criteria
                )
            ):
                errors.append(f"{task_id}: acceptance precisa de texto(s).")
        for task_id, deps in graph.items():
            for dep in deps:
                if dep not in ids:
                    errors.append(f"{task_id}: dependência ausente {dep}.")
                if dep == task_id:
                    errors.append(f"{task_id}: dependência de si mesmo.")
        visited = set()
        visiting = set()

        def walk(item):
            if item in visiting:
                return True
            if item in visited:
                return False
            visiting.add(item)
            cycle = any(walk(dep) for dep in graph.get(item, []) if dep in graph)
            visiting.remove(item)
            visited.add(item)
            return cycle

        if any(walk(item) for item in sorted(graph)):
            errors.append("tasks: grafo de dependências contém ciclo.")

    elif kind == "handoff":
        for key in ("task_id", "project", "from", "to", "status", "next_action"):
            string(key)
        items("evidence")
        items("risks")
        if data.get("status") not in {
            "in_progress",
            "ready_for_review",
            "blocked",
            "failed",
            "completed",
        }:
            errors.append("status: estado de handoff inválido.")

    elif kind == "review":
        for key in ("commit", "author", "reviewer", "status"):
            string(key)
        if data.get("status") not in {
            "approved",
            "changes_requested",
            "inconclusive",
        }:
            errors.append("status: parecer de revisão inválido.")
        if data.get("author") == data.get("reviewer"):
            errors.append("review: revisão não pode ser do próprio autor.")
        if not SHA_PATTERN.fullmatch(str(data.get("commit", ""))):
            errors.append("commit: SHA hexadecimal de 7 a 40 caracteres.")
        findings = items("findings")
        for index, finding in enumerate(findings):
            if not isinstance(finding, dict):
                errors.append(f"findings[{index}]: objeto obrigatório.")
                continue
            if finding.get("severity") not in {
                "blocker",
                "important",
                "suggestion",
            }:
                errors.append(f"findings[{index}]: severidade inválida.")
            for key in ("file", "scenario", "reason", "fix"):
                if not isinstance(finding.get(key), str) or not finding[key]:
                    errors.append(f"findings[{index}].{key}: obrigatório.")
        if data.get("status") == "approved" and any(
            isinstance(finding, dict) and finding.get("severity") == "blocker"
            for finding in findings
        ):
            errors.append("review: aprovação contradiz achado bloqueador.")

    elif kind == "qa":
        for key in ("commit", "developer", "executed_by", "environment", "status"):
            string(key)
        if not SHA_PATTERN.fullmatch(str(data.get("commit", ""))):
            errors.append("commit: SHA hexadecimal de 7 a 40 caracteres.")
        if data.get("executed_by") == data.get("developer"):
            errors.append("qa: execução não é independente do desenvolvedor.")
        if data.get("status") not in {"passed", "failed", "inconclusive"}:
            errors.append("status: parecer QA inválido.")
        scenarios = items("scenarios", nonempty=True)
        for index, scenario in enumerate(scenarios):
            if not isinstance(scenario, dict):
                errors.append(f"scenarios[{index}]: objeto obrigatório.")
                continue
            if scenario.get("result") not in {
                "passed",
                "failed",
                "not_run",
                "blocked",
            }:
                errors.append(f"scenarios[{index}]: resultado inválido.")
            if not isinstance(scenario.get("id"), str) or not scenario["id"]:
                errors.append(f"scenarios[{index}].id: obrigatório.")
            if scenario.get("result") in {"passed", "failed"} and not (
                isinstance(scenario.get("evidence"), str)
                and scenario["evidence"].strip()
            ):
                errors.append(f"scenarios[{index}]: evidência obrigatória.")
        if data.get("status") == "passed" and any(
            not isinstance(scenario, dict) or scenario.get("result") != "passed"
            for scenario in scenarios
        ):
            errors.append("qa: status passed exige todos os cenários passed.")

    elif kind == "ci":
        for key in ("commit", "status", "url"):
            string(key)
        if not SHA_PATTERN.fullmatch(str(data.get("commit", ""))):
            errors.append("commit: SHA hexadecimal de 7 a 40 caracteres.")
        if data.get("status") not in {"passed", "failed", "pending"}:
            errors.append("status: CI inválido.")
        if not str(data.get("url", "")).startswith("https://"):
            errors.append("url: link HTTPS obrigatório (não é prova autenticada).")
    else:
        errors.append(f"Tipo desconhecido: {kind}.")
    return errors


def release_gate(directory):
    """Structural gate. A passing result NEVER authorizes a release."""
    directory = Path(directory)
    errors = []
    objects = {}
    for name in ("review", "qa", "ci"):
        try:
            objects[name] = load(directory / f"{name}.json")
            errors.extend(f"{name}: {x}" for x in validate(name, objects[name]))
        except ValueError as exc:
            errors.append(str(exc))
    if len(objects) == 3:
        commits = [objects[name].get("commit") for name in ("review", "qa", "ci")]
        if len(set(commits)) != 1:
            errors.append("Os três artefatos precisam apontar para o mesmo commit.")
        if objects["review"].get("status") != "approved":
            errors.append("Revisão independente não aprovada.")
        if objects["qa"].get("status") != "passed":
            errors.append("QA não aprovado.")
        if objects["ci"].get("status") != "passed":
            errors.append("CI não aprovado.")
    return {
        "status": "BLOCKED" if errors else "READY_FOR_HUMAN_DECISION",
        "errors": errors,
        "human_approval_required": True,
        "warning": (
            "JSON não atesta autenticidade; valide SHAs e CI no GitHub. "
            "A ferramenta não faz deploy, merge nem concede permissão."
        ),
    }


def python_modules(root):
    modules = {}
    warnings = []
    for path in sorted(root.rglob("*.py")):
        if set(path.relative_to(root).parts) & EXCLUDED or path.is_symlink():
            continue
        parts = list(path.relative_to(root).with_suffix("").parts)
        if parts and parts[0] == "src":
            parts.pop(0)
        if parts and parts[-1] == "__init__":
            parts.pop()
        if not parts or not all(part.isidentifier() for part in parts):
            continue
        module = ".".join(parts)
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (OSError, UnicodeError, SyntaxError) as exc:
            warnings.append({"file": str(path.relative_to(root)), "error": str(exc)})
            continue
        modules[module] = (path, tree)
    return modules, warnings


def inspect_project(root):
    """Only literal Python imports; not runtime architecture or proof of coupling."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise ValueError(f"Projeto inexistente ou não é diretório: {root}")
    modules, warnings = python_modules(root)
    available = set(modules)
    edges = set()

    def resolve_target(candidate):
        while candidate:
            if candidate in available:
                return candidate
            candidate = candidate.rpartition(".")[0]
        return None

    for module, (_, tree) in modules.items():
        package = module.rpartition(".")[0]
        for node in ast.walk(tree):
            targets = []
            if isinstance(node, ast.Import):
                targets = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    base = package.split(".") if package else []
                    remove = node.level - 1
                    if remove > len(base):
                        continue
                    base = base[: len(base) - remove] if remove else base
                    prefix = ".".join(base)
                    target = ".".join(filter(None, [prefix, node.module or ""]))
                else:
                    target = node.module or ""
                targets = [f"{target}.{alias.name}" for alias in node.names]
                targets.append(target)
            for candidate in targets:
                dest = resolve_target(candidate)
                if dest and dest != module:
                    edges.add((module, dest))

    graph = {name: set() for name in modules}
    for source, target in edges:
        graph[source].add(target)
    cycles = set()
    seen = set()
    active = []

    def visit(node):
        if node in active:
            cycle = active[active.index(node) :]
            rotations = [tuple(cycle[i:] + cycle[:i]) for i in range(len(cycle))]
            cycles.add(min(rotations))
            return
        if node in seen:
            return
        active.append(node)
        for neighbor in sorted(graph[node]):
            visit(neighbor)
        active.pop()
        seen.add(node)

    for name in sorted(graph):
        visit(name)
    return {
        "project": str(root),
        "python_modules": len(modules),
        "static_import_edges": [list(item) for item in sorted(edges)],
        "cycles": [list(item) for item in sorted(cycles)],
        "parse_warnings": warnings,
        "limitations": [
            "Não detecta imports dinâmicos ou dependências injetadas.",
            "Nomes de módulos e imports podem variar com sys.path.",
            "Ciclos estáticos são indícios, não prova de falha de execução.",
        ],
    }


def changed_files(root, base):
    proc = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "diff",
            "--name-only",
            "-z",
            "--diff-filter=ACMRD",
            f"{base}...HEAD",
        ],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode:
        raise ValueError(
            proc.stderr.decode("utf-8", "replace").strip() or "git diff falhou."
        )
    return sorted({name for name in proc.stdout.decode("utf-8").split("\0") if name})


def scope_check(root, base, allow):
    files = changed_files(root, base)
    extras = [
        path
        for path in files
        if not any(fnmatch.fnmatchcase(path, pat) for pat in allow)
    ]
    return {
        "status": "OUT_OF_SCOPE" if extras else "IN_SCOPE",
        "changed": files,
        "unexpected": extras,
        "patterns": allow,
        "note": "Somente diff base...HEAD; alterações uncommitted não são auditadas.",
    }


def black_check(root, apply, base):
    if base:
        files = [
            name
            for name in changed_files(root, base)
            if name.endswith(".py") and (root / name).is_file()
        ]
        if not files:
            return {"status": "SKIPPED_NO_PYTHON_CHANGES", "files": []}, 0
    else:
        files = ["."]
    command = [sys.executable, "-m", "black"]
    if not apply:
        command += ["--check", "--diff"]
    command += files
    proc = subprocess.run(
        command,
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return {
        "status": "PASS" if proc.returncode == 0 else "FAIL",
        "code": proc.returncode,
        "mode": "APPLY" if apply else "CHECK_ONLY",
        "files": files,
        "command": command,
        "stdout": proc.stdout[-12000:],
        "stderr": proc.stderr[-12000:],
    }, proc.returncode


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)

    v = sub.add_parser("validate", help="Validar artefato JSON de agentes.")
    v.add_argument("kind", choices=["spec", "plan", "handoff", "review", "qa", "ci"])
    v.add_argument("file")

    g = sub.add_parser("gate", help="Verificar evidence/review,qa,ci.json.")
    g.add_argument("folder")

    ins = sub.add_parser("inspect", help="Mapa estático de imports Python.")
    ins.add_argument("project")
    ins.add_argument("--mermaid", action="store_true")

    sc = sub.add_parser("scope", help="Arquivos de diff fora de escopo.")
    sc.add_argument("project")
    sc.add_argument("--base", required=True)
    sc.add_argument("--allow", action="append", required=True)

    b = sub.add_parser("black", help="Verificar Black (não altera sem --apply).")
    b.add_argument("project")
    b.add_argument("--changed-base")
    b.add_argument("--apply", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.action == "validate":
            errors = validate(args.kind, load(args.file))
            return report({"valid": not errors, "errors": errors}, 2 if errors else 0)
        if args.action == "gate":
            output = release_gate(args.folder)
            return report(output, 3 if output["errors"] else 0)
        if args.action == "inspect":
            output = inspect_project(args.project)
            if args.mermaid:
                print("flowchart LR")
                for src, dst in output["static_import_edges"]:
                    label = lambda s: re.sub(r"[^A-Za-z0-9_]", "_", s)
                    print(f"  {label(src)} --> {label(dst)}")
                return 0
            return report(output)
        if args.action == "scope":
            output = scope_check(Path(args.project).resolve(), args.base, args.allow)
            return report(output, 3 if output["unexpected"] else 0)
        if args.action == "black":
            output, code = black_check(
                Path(args.project).resolve(), args.apply, args.changed_base
            )
            return report(output, code)
    except ValueError as exc:
        return report({"status": "ERROR", "error": str(exc)}, 2)
    return 2


if __name__ == "__main__":
    sys.exit(main())
