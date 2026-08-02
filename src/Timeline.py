"""
Aplatit la structure parsée (avec répétitions imbriquées) en une liste
chronologique de "steps" avec leur temps de départ / fin absolu.

Chaque step porte aussi son contexte de répétition (bloc X, répétition i/N)
pour que le Coach puisse dire "Répétition 2 sur 4" au bon moment.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TimelineStep:

    start: int
    end: int
    name: str
    intensity_class: Optional[str]
    target: Optional[dict]
    duration: int

    # Contexte de répétition, si applicable
    repeat_total: Optional[int] = None
    repeat_index: Optional[int] = None
    is_first_in_repeat_block: bool = False


def build_timeline(steps):

    result = []
    current_time = [0]  # liste pour être mutable dans la closure

    _walk(steps, current_time, result)

    return result


def _walk(steps, current_time, result, repeat_total=None):

    for step in steps:

        if step["type"] == "step":

            duration = step["duration"]

            start = current_time[0]
            end = start + duration

            result.append(
                TimelineStep(
                    start=start,
                    end=end,
                    name=step["name"],
                    intensity_class=step.get("intensity_class"),
                    target=step.get("target"),
                    duration=duration,
                )
            )

            current_time[0] = end

        elif step["type"] == "repeat":

            repeat_count = step["repeat"]

            for i in range(repeat_count):

                before = len(result)

                _walk(step["steps"], current_time, result)

                # Marque le premier step ajouté durant cette itération
                # avec le contexte de répétition
                if len(result) > before:
                    first_new = result[before]
                    first_new.repeat_total = repeat_count
                    first_new.repeat_index = i + 1
                    first_new.is_first_in_repeat_block = True
