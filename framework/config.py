from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunConfig:
    base_url: str
    env: str  # local | grid
    browser: str  # chrome | firefox
    grid_url: str
    headless: bool
    implicit_wait_s: float
    explicit_wait_s: float
