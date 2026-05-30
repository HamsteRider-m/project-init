#!/usr/bin/env python3
"""Validate the project document handoff loop.

The validator is intentionally deterministic: it checks files, headings,
reading order, wrappers, placeholders, prompt contracts, managed file
categories, workflow transitions, task audit fields, and obvious secrets.
It does not ask an LLM whether a project is acceptable.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    code: str
    path: str
    detail: str


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_headings(text: str) -> set[str]:
    headings: set[str] = set()
    for line in text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if match:
            headings.add(match.group(2).strip())
    return headings


def markdown_section(text: str, heading: str) -> str | None:
    pattern = re.compile(rf"^(?P<marks>#+)\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return None
    level = len(match.group("marks"))
    start = match.end()
    next_heading = re.compile(rf"^#{{1,{level}}}\s+.+?$", re.MULTILINE)
    next_match = next_heading.search(text, start)
    end = next_match.start() if next_match else len(text)
    return text[start:end]


def has_concrete_content(section: str) -> bool:
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if not line or line in {"-", "*"}:
            continue
        if line.startswith("<!--") and line.endswith("-->"):
            continue
        if "<!--" in line and "-->" in line and re.sub(r"<!--.*?-->", "", line).strip() in {"", "-", "*"}:
            continue
        return True
    return False


def load_contract(root: Path, contract_arg: Path | None) -> dict[str, Any]:
    path = contract_arg or root / ".github" / "project_handoff_contract.json"
    if not path.exists():
        raise FileNotFoundError(f"contract does not exist: {path}")
    return json.loads(read_text(path))


def validate_required_files(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for item in contract.get("required_files", []):
        path = root / item
        if not path.exists():
            findings.append(Finding("missing_file", item, "required file is absent"))
        elif not path.is_file():
            findings.append(Finding("not_file", item, "required path is not a file"))
    return findings


def validate_headings(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for file_name, required in contract.get("required_headings", {}).items():
        path = root / file_name
        if not path.exists():
            continue
        headings = markdown_headings(read_text(path))
        for heading in required:
            if heading not in headings:
                findings.append(Finding("missing_heading", file_name, f"missing heading: {heading}"))
    return findings


def ordered_positions(text: str, needles: list[str]) -> list[int]:
    positions: list[int] = []
    cursor = 0
    for needle in needles:
        pos = text.find(needle, cursor)
        positions.append(pos)
        if pos >= 0:
            cursor = pos + len(needle)
    return positions


def validate_reading_order(root: Path, contract: dict[str, Any]) -> list[Finding]:
    path = root / "AGENTS.md"
    if not path.exists():
        return []
    text = read_text(path)
    order = list(contract.get("reading_order", []))
    positions = ordered_positions(text, order)
    findings: list[Finding] = []
    for item, pos in zip(order, positions, strict=False):
        if pos < 0:
            findings.append(Finding("reading_order_missing", "AGENTS.md", f"missing reading-order item: {item}"))
    found_positions = [pos for pos in positions if pos >= 0]
    if found_positions != sorted(found_positions):
        findings.append(Finding("reading_order_wrong", "AGENTS.md", "reading-order items are not in contract order"))
    return findings


def validate_wrappers(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    required_reference = str(contract.get("wrapper_required_reference", "AGENTS.md"))
    for item in contract.get("wrapper_files", []):
        path = root / item
        if not path.exists():
            continue
        text = read_text(path)
        if required_reference not in text:
            findings.append(Finding("wrapper_missing_reference", item, f"wrapper must reference {required_reference}"))
        headings = [line for line in text.splitlines() if re.match(r"^#{1,6}\s+", line)]
        if len(headings) > 2:
            findings.append(Finding("wrapper_too_complex", item, "wrapper has too many headings; keep rules in AGENTS.md"))
    return findings


def validate_placeholders(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    patterns = list(contract.get("forbidden_placeholder_patterns", []))
    if not patterns:
        return findings
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = read_text(path)
        for pattern in patterns:
            if pattern in text:
                findings.append(Finding("forbidden_placeholder", rel(path, root), f"placeholder remains: {pattern}"))
    return findings


def validate_doc_audit(root: Path, contract: dict[str, Any]) -> list[Finding]:
    path = root / ".github" / "TaskLogs" / "Execution.md"
    if not path.exists():
        return []
    text = read_text(path)
    findings: list[Finding] = []
    if "Documentation Audit" not in text:
        findings.append(Finding("missing_doc_audit", rel(path, root), "Documentation Audit section is absent"))
        return findings
    for item in contract.get("doc_audit_required_fields", []):
        if item not in text:
            findings.append(Finding("missing_doc_audit_field", rel(path, root), f"missing audit field: {item}"))
    return findings


def validate_runbook_terms(root: Path, contract: dict[str, Any]) -> list[Finding]:
    path = root / "docs" / "runbook.md"
    if not path.exists():
        return []
    text = read_text(path)
    findings: list[Finding] = []
    for term in contract.get("runbook_required_terms", []):
        if term not in text:
            findings.append(Finding("missing_runbook_term", rel(path, root), f"missing required term: {term}"))
    return findings


def validate_prompt_files(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for item in contract.get("prompt_files", []):
        file_name = str(item.get("path", ""))
        if not file_name:
            findings.append(Finding("prompt_contract_invalid", ".github/project_handoff_contract.json", "prompt_files item has no path"))
            continue
        path = root / file_name
        if not path.exists():
            findings.append(Finding("missing_prompt_file", file_name, "prompt file is absent"))
            continue
        text = read_text(path)
        for reference in item.get("must_reference", []):
            if str(reference) not in text:
                findings.append(Finding("prompt_missing_reference", file_name, f"missing required reference: {reference}"))
        for term in item.get("must_include_terms", []):
            if str(term) not in text:
                findings.append(Finding("prompt_missing_term", file_name, f"missing required term: {term}"))
    return findings


def validate_managed_file_categories(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    categories = contract.get("managed_file_categories", {})
    owners: dict[str, str] = {}
    for category, files in categories.items():
        for item in files:
            item = str(item)
            previous = owners.get(item)
            if previous and previous != category:
                findings.append(Finding("managed_file_overlap", ".github/project_handoff_contract.json", f"{item} appears in both {previous} and {category}"))
            owners[item] = str(category)
    for item in contract.get("required_files", []):
        item = str(item)
        if item.startswith(("docs/", ".github/", "scripts/")) or item in {"AGENTS.md", "Project.md", "README.md", "CLAUDE.md", "CODEX.md"}:
            if item not in owners:
                findings.append(Finding("required_file_uncategorized", ".github/project_handoff_contract.json", f"{item} is required but not in managed_file_categories"))
    return findings


def validate_workflow_transitions(root: Path, contract: dict[str, Any]) -> list[Finding]:
    path = root / ".github" / "AI_WORKFLOW.md"
    if not path.exists():
        return []
    text = read_text(path)
    findings: list[Finding] = []
    for transition in contract.get("workflow_transitions", []):
        source = str(transition.get("from", ""))
        target = str(transition.get("to", ""))
        if not source or not target:
            findings.append(Finding("workflow_transition_invalid", ".github/project_handoff_contract.json", "transition must include from and to"))
            continue
        for mode in [source, target]:
            if f"`{mode}`" not in text and mode not in text:
                findings.append(Finding("workflow_mode_missing", rel(path, root), f"workflow mode not documented: {mode}"))
        for required in transition.get("requires", []):
            if str(required) not in text:
                findings.append(Finding("workflow_requirement_missing", rel(path, root), f"transition {source}->{target} does not reference {required}"))
    return findings


def validate_required_sections(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for file_name, headings in contract.get("required_non_placeholder_sections", {}).items():
        path = root / file_name
        if not path.exists():
            continue
        text = read_text(path)
        for heading in headings:
            section = markdown_section(text, str(heading))
            if section is None:
                findings.append(Finding("missing_required_section", file_name, f"missing section: {heading}"))
            elif not has_concrete_content(section):
                findings.append(Finding("empty_required_section", file_name, f"section has no concrete content: {heading}"))
    return findings


def validate_secret_patterns(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    patterns = [re.compile(pattern) for pattern in contract.get("secret_patterns", [])]
    if not patterns:
        return findings
    for path in root.rglob("*"):
        if ".git" in path.parts or not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".json", ".yml", ".yaml", ".txt", ".py", ".sh"}:
            continue
        text = read_text(path)
        for pattern in patterns:
            match = pattern.search(text)
            if match:
                findings.append(Finding("secret_pattern", rel(path, root), f"matches secret pattern: {pattern.pattern}"))
    return findings


def validate(root: Path, contract: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(validate_required_files(root, contract))
    findings.extend(validate_headings(root, contract))
    findings.extend(validate_reading_order(root, contract))
    findings.extend(validate_wrappers(root, contract))
    findings.extend(validate_placeholders(root, contract))
    findings.extend(validate_doc_audit(root, contract))
    findings.extend(validate_runbook_terms(root, contract))
    findings.extend(validate_prompt_files(root, contract))
    findings.extend(validate_managed_file_categories(root, contract))
    findings.extend(validate_workflow_transitions(root, contract))
    findings.extend(validate_required_sections(root, contract))
    findings.extend(validate_secret_patterns(root, contract))
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate project handoff documentation against a JSON contract.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root to validate.")
    parser.add_argument("--contract", type=Path, default=None, help="Contract JSON path. Defaults to <root>/.github/project_handoff_contract.json.")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON.")
    args = parser.parse_args()

    root = args.root.resolve()
    try:
        contract = load_contract(root, args.contract)
    except Exception as exc:
        print(f"FAIL contract_load: {exc}", file=sys.stderr)
        return 2
    findings = validate(root, contract)
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
    elif findings:
        print("Handoff validation failed:")
        for finding in findings:
            print(f"- {finding.code}: {finding.path}: {finding.detail}")
    else:
        print("Handoff validation passed.")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
