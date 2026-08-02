import json
from pathlib import Path


class WorkoutParser:

    def __init__(self, filename):
        self.filename = Path(filename)

    def load(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def parse(self):

        workout = self.load()

        print("=" * 60)
        print("MYCOACH - WORKOUT PARSER")
        print("=" * 60)

        print(f"Titre : {workout['Title']}")
        print(f"Type  : {workout['Type']}")
        print()

        print("Structure")
        print("-" * 60)

        self._parse_steps(workout["Structure"])

    def _parse_steps(self, steps, indent=0):

        prefix = "    " * indent

        for step in steps:

            if step["Type"] == "Step":

                duration = step["Length"]["Value"]
                duration = int(duration)

                minutes = duration // 60
                seconds = duration % 60

                target = step.get("IntensityTarget", {})

                if target:
                    zone = (
                        f"{target.get('MinValue', target.get('Value'))}"
                        f"-"
                        f"{target.get('MaxValue', target.get('Value'))}%"
                    )
                else:
                    zone = "-"

                print(
                    f"{prefix}"
                    f"STEP | "
                    f"{step.get('Name','')} | "
                    f"{minutes:02d}:{seconds:02d} | "
                    f"{zone}"
                )

            elif step["Type"] == "Repetition":

                repeat = int(step["Length"]["Value"])

                print(
                    f"{prefix}"
                    f"REPEAT x{repeat}"
                )

                self._parse_steps(step["Steps"], indent + 1)


if __name__ == "__main__":

    parser = WorkoutParser("samples/workout.jsonV2")
    parser.parse()
