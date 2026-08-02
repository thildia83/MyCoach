
from dataclasses import dataclass


@dataclass
class Announcement:
    time: int
    text: str


class ScenarioBuilder:

    def __init__(self):
        self.timeline = []
        self.current_time = 0

    def build(self, steps):

        self.timeline = []
        self.current_time = 0

        self._parse_steps(steps)

        return self.timeline

    def _parse_steps(self, steps):

        for step in steps:

            if step["Type"] == "Step":

                duration = int(step["Length"]["Value"])

                name = step.get("Name", "")

                self.timeline.append(
                    Announcement(
                        self.current_time,
                        f"Début : {name}"
                    )
                )

                self.current_time += duration

            elif step["Type"] == "Repetition":

                repeat = int(step["Length"]["Value"])

                self.timeline.append(
                    Announcement(
                        self.current_time,
                        f"Début d'un bloc de {repeat} répétitions"
                    )
                )

                for i in range(repeat):

                    self.timeline.append(
                        Announcement(
                            self.current_time,
                            f"Répétition {i+1} sur {repeat}"
                        )
                    )

                    self._parse_steps(step["Steps"])
