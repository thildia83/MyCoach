"""
Conversion des cibles d'intensité en allure réelle (min/km).

TrainingPeaks exprime les objectifs en % de la vitesse seuil (ThresholdSpeed,
exprimée en m/s). Le coureur, lui, pense en allure : minutes par kilomètre.
Ce module fait la conversion.
"""


def speed_to_pace_seconds(speed_m_s):
    """Convertit une vitesse en m/s en allure (secondes par kilomètre)."""

    if not speed_m_s or speed_m_s <= 0:
        return None

    return 1000.0 / speed_m_s


def format_pace(seconds_per_km):
    """Formate une allure en 'X minutes Y' (arrondi à la seconde)."""

    if seconds_per_km is None:
        return None

    total_seconds = round(seconds_per_km)

    minutes = total_seconds // 60
    seconds = total_seconds % 60

    if seconds == 0:
        return f"{minutes} minutes"

    return f"{minutes} minutes {seconds:02d}"


def target_pace_text(target, threshold_speed):
    """
    Calcule l'allure cible "parlée" à partir d'une cible TrainingPeaks.

    On prend le milieu de la fourchette Min/Max (le coach annonce une seule
    allure, pas une fourchette à retenir en courant).
    """

    if not target or not threshold_speed:
        return None

    unit = target.get("Unit")

    if unit != "PercentOfThresholdSpeed":
        return None

    minimum = target.get("MinValue")
    maximum = target.get("MaxValue")

    if minimum is None or maximum is None:
        return None

    pct_mid = (minimum + maximum) / 2.0

    speed = threshold_speed * (pct_mid / 100.0)

    pace_seconds = speed_to_pace_seconds(speed)

    pace_text = format_pace(pace_seconds)

    if pace_text is None:
        return None

    return f"{pace_text} au kilomètre"
