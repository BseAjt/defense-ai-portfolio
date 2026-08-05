from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str
    version: str
    base_dir: Path
    static_dir: Path
    data_dir: Path
    database_path: Path
    agent_config_path: Path


def load_settings() -> Settings:
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = Path(os.getenv("MEMORYOS_DATA_DIR", base_dir / "data")).resolve()
    agent_config_path = Path(
        os.getenv("MEMORYOS_AGENT_CONFIG", base_dir / "config" / "agents.json")
    ).resolve()
    data_dir.mkdir(parents=True, exist_ok=True)
    return Settings(
        app_name="MemoryOS MVP",
        version="0.3.0",
        base_dir=base_dir,
        static_dir=base_dir / "static",
        data_dir=data_dir,
        database_path=data_dir / "memoryos.db",
        agent_config_path=agent_config_path,
    )


settings = load_settings()
