from dataclasses import dataclass
from typing import Optional


@dataclass
class Target:

    type: str

    minimum: Optional[float]

    maximum: Optional[float]

    unit: str


@dataclass
class WorkoutStep:

    name: str

    duration_seconds: int

    target: Optional[Target]

    description: str = ""


@dataclass
class RepeatBlock:

    repeat: int

    steps: list
