from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import settings


REQUIRED_FIELDS = {
    "name",
    "inspiration",
    "role",
    "mission",
    "mindset",
    "questions",
    "refuses",
    "blind_spots",
    "style",
    "analysis",
    "keywords",
}


class AgentConfigurationError(RuntimeError):
    pass


@dataclass(frozen=True)
class AgentRegistry:
    agents: tuple[dict[str, Any], ...]
    default_agents: tuple[str, ...]
    source_path: Path

    @classmethod
    def load(cls, path: Path | None = None) -> "AgentRegistry":
        source_path = path or settings.agent_config_path
        try:
            payload = json.loads(source_path.read_text(encoding="utf-8"))
        except FileNotFoundError as exc:
            raise AgentConfigurationError(f"Agent configuration not found: {source_path}") from exc
        except json.JSONDecodeError as exc:
            raise AgentConfigurationError(f"Invalid agent JSON: {exc}") from exc

        raw_agents = payload.get("agents")
        defaults = payload.get("default_agents")
        if not isinstance(raw_agents, list) or not raw_agents:
            raise AgentConfigurationError("The agent configuration must contain a non-empty 'agents' list.")
        if not isinstance(defaults, list):
            raise AgentConfigurationError("The agent configuration must contain a 'default_agents' list.")

        names: set[str] = set()
        validated: list[dict[str, Any]] = []
        for index, agent in enumerate(raw_agents):
            if not isinstance(agent, dict):
                raise AgentConfigurationError(f"Agent at index {index} must be an object.")
            missing = REQUIRED_FIELDS - set(agent)
            if missing:
                raise AgentConfigurationError(
                    f"Agent at index {index} is missing fields: {', '.join(sorted(missing))}"
                )
            name = agent["name"]
            if not isinstance(name, str) or not name.strip():
                raise AgentConfigurationError(f"Agent at index {index} has an invalid name.")
            if name in names:
                raise AgentConfigurationError(f"Duplicate agent name: {name}")
            for field in ("mindset", "questions", "refuses", "blind_spots", "keywords"):
                if not isinstance(agent[field], list) or not all(
                    isinstance(item, str) and item.strip() for item in agent[field]
                ):
                    raise AgentConfigurationError(f"Agent '{name}' has an invalid '{field}' list.")
            names.add(name)
            validated.append(dict(agent))

        unknown_defaults = set(defaults) - names
        if unknown_defaults:
            raise AgentConfigurationError(
                f"Unknown default agents: {', '.join(sorted(unknown_defaults))}"
            )

        return cls(tuple(validated), tuple(defaults), source_path)

    def list(self) -> list[dict[str, Any]]:
        return [dict(agent) for agent in self.agents]

    def select(self, subject: str) -> list[dict[str, Any]]:
        normalized = subject.casefold()
        selected_names = set(self.default_agents)
        for agent in self.agents:
            if any(keyword.casefold() in normalized for keyword in agent["keywords"]):
                selected_names.add(agent["name"])
        return [dict(agent) for agent in self.agents if agent["name"] in selected_names]
