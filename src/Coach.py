class Coach:

    def __init__(self):
        pass

    def build_script(self, workout):

        script = []

        script.append(
            f"Aujourd'hui : {workout['title']}."
        )

        self._describe_steps(workout["steps"], script)

        return script

    def _describe_steps(self, steps, script):

        for step in steps:

            if step["type"] == "step":

                script.append(
                    self._describe_step(step)
                )

            elif step["type"] == "repeat":

                repeat = step["repeat"]

                script.append(
                    f"Bloc de {repeat} répétitions."
                )

                for i in range(repeat):

                    script.append(
                        f"Répétition {i+1}."
                    )

                    self._describe_steps(step["steps"], script)

    def _describe_step(self, step):

        duration = self._duration(step["duration"])

        target = self._target(step["target"])

        name = step["name"]

        if target:
            return f"{name}. {duration}. Objectif : {target}."

        return f"{name}. {duration}."

    def _duration(self, seconds):

        minutes = seconds // 60
        sec = seconds % 60

        if minutes and sec:
            return f"{minutes} minutes {sec} secondes"

        if minutes:
            return f"{minutes} minutes"

        return f"{sec} secondes"

    def _target(self, target):

        if not target:
            return ""

        minimum = target.get("MinValue")
        maximum = target.get("MaxValue")

        unit = target.get("Unit")

        if minimum is None:
            return ""

        if unit == "PercentOfThresholdSpeed":
            return f"{minimum} à {maximum} % de la vitesse seuil"

        if unit == "PercentOfThresholdHeartRate":
            return f"{minimum} à {maximum} % de la fréquence cardiaque seuil"

        return f"{minimum} à {maximum} {unit}"