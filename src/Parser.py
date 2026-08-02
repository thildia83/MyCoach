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

        return {
            "title": workout["Title"],
            "description": workout.get("Description", ""),
            "type": workout["Type"],
            "threshold_speed": workout.get("ThresholdSpeed"),
            "ftp": workout.get("Ftp"),
            "threshold_hr": workout.get("ThresholdHr"),
            "max_hr": workout.get("MaxHr"),
            "steps": self._parse_steps(workout["Structure"])
        }

    def _parse_steps(self, steps):

        result = []

        for step in steps:

            if step["Type"] == "Step":

                result.append({
                    "type": "step",
                    "name": step.get("Name", ""),
                    "duration": int(step["Length"]["Value"]),
                    "duration_unit": step["Length"]["Unit"],

                    "intensity_class": step.get("IntensityClass"),

                    "target": step.get("IntensityTarget"),

                    "cadence": step.get("CadenceTarget"),

                    "description": step.get("Description", "")
                })

            elif step["Type"] == "Repetition":

                result.append({
                    "type": "repeat",
                    "repeat": int(step["Length"]["Value"]),
                    "steps": self._parse_steps(step["Steps"])
                })

        return result


if __name__ == "__main__":

    parser = WorkoutParser("samples/workout.jsonV2")

    workout = parser.parse()

    print(workout["title"])
    print()

    from pprint import pprint

    pprint(workout["steps"])
