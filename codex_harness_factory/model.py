from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HarnessMetadata:
    """Light deterministic metadata extracted from a request file."""

    title: str
    slug: str
    entity: str
    domain: str
    operations: tuple[str, ...]
    goals: tuple[str, ...] = field(default_factory=tuple)
    constraints: tuple[str, ...] = field(default_factory=tuple)
    non_goals: tuple[str, ...] = field(default_factory=tuple)
    source_request: str = ""
    content_hash: str = ""

    @property
    def job_id(self) -> str:
        return f"{self.slug}-{self.content_hash[:10]}"

    def to_dict(self) -> dict[str, object]:
        return {
            "title": self.title,
            "slug": self.slug,
            "entity": self.entity,
            "domain": self.domain,
            "operations": list(self.operations),
            "goals": list(self.goals),
            "constraints": list(self.constraints),
            "non_goals": list(self.non_goals),
            "source_request": self.source_request,
            "content_hash": self.content_hash,
            "job_id": self.job_id,
        }
