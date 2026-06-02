from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .model import HarnessMetadata

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_BULLET_RE = re.compile(r"^\s*[-*+]\s+(.+?)\s*$")
_FIELD_RE = re.compile(r"^\s*(?:[-*+]\s*)?([A-Za-z][A-Za-z0-9 _-]{1,40})\s*:\s*(.+?)\s*$")


def extract_metadata(request_path: Path) -> HarnessMetadata:
    text = request_path.read_text(encoding="utf-8")
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    slug = _slug_from_path(request_path)
    title = _title_from_text(text) or _title_from_slug(slug)
    fields = _field_map(text)
    sections = _sections(text)

    entity = fields.get("entity") or _entity_from_slug(slug) or _entity_from_title(title)
    domain = fields.get("domain") or fields.get("app") or f"{entity} CRUD"
    goals = _items_from_sections(sections, {"goal", "goals", "mvp goal", "requirements", "user stories"})
    constraints = _items_from_sections(sections, {"constraints", "rules", "requirements"})
    non_goals = _items_from_sections(sections, {"non-goals", "non goals", "out of scope"})
    operations = _operations(text, slug)

    return HarnessMetadata(
        title=title,
        slug=slug,
        entity=entity,
        domain=domain,
        operations=tuple(operations),
        goals=tuple(_dedupe(goals)) or (f"Generate a reusable Codex harness for {domain}.",),
        constraints=tuple(_dedupe(constraints)),
        non_goals=tuple(_dedupe(non_goals)),
        source_request=str(request_path),
        content_hash=content_hash,
    )


def _slug_from_path(path: Path) -> str:
    stem = path.name
    for suffix in (".request.md", ".md", ".request"):
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-").lower()
    return slug or "codex-harness"


def _title_from_text(text: str) -> str | None:
    for line in text.splitlines():
        match = _HEADING_RE.match(line)
        if match:
            return match.group(2).strip()
    return None


def _title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def _field_map(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in text.splitlines():
        match = _FIELD_RE.match(line)
        if match:
            key = re.sub(r"\s+", " ", match.group(1).strip().lower())
            fields[key] = match.group(2).strip()
    return fields


def _sections(text: str) -> dict[str, list[str]]:
    current = "overview"
    sections: dict[str, list[str]] = {current: []}
    for line in text.splitlines():
        heading = _HEADING_RE.match(line)
        if heading:
            current = heading.group(2).strip().lower()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)
    return sections


def _items_from_sections(sections: dict[str, list[str]], names: set[str]) -> list[str]:
    items: list[str] = []
    for name, lines in sections.items():
        normalized = re.sub(r"\s+", " ", name.strip().lower())
        if normalized not in names:
            continue
        for line in lines:
            bullet = _BULLET_RE.match(line)
            if bullet:
                items.append(bullet.group(1).strip())
            elif line.strip() and not line.strip().endswith(":"):
                items.append(line.strip())
    return items


def _operations(text: str, slug: str) -> list[str]:
    lowered = f"{slug}\n{text}".lower()
    if "crud" in lowered:
        return ["Create", "Read", "Update", "Delete"]
    operations = []
    for label in ("Create", "Read", "Update", "Delete", "List", "Search"):
        if label.lower() in lowered:
            operations.append(label)
    return operations or ["Analyze", "Plan", "Implement", "Review", "Debug"]


def _entity_from_slug(slug: str) -> str:
    parts = [part for part in slug.split("-") if part and part != "crud"]
    if not parts:
        return "Artifact"
    return " ".join(part.capitalize() for part in parts)


def _entity_from_title(title: str) -> str:
    cleaned = re.sub(r"\bCRUD\b", "", title, flags=re.IGNORECASE).strip(" -:")
    return cleaned or "Artifact"


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = re.sub(r"\s+", " ", item).strip()
        key = normalized.lower()
        if normalized and key not in seen:
            seen.add(key)
            result.append(normalized)
    return result
