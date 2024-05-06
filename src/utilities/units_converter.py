def cm_to_inches(cm: float | int) -> float:
    """
    Converts centimeters to inches.

    Parameters
    ----------
    cm: float | int
        A float representing the length in centimeters.
    Returns
    ----------
      A float representing the equivalent length in inches.
    """
    inches_per_cm = 0.393701
    return cm * inches_per_cm


def m_to_inches(meters: float | int) -> float:
    """
    Converts meters to inches.

    Parameters
    ----------
    meters: float | int
        A float representing the length in meters.
    Returns
    ----------
      A float representing the equivalent length in inches.
    """
    inches_per_meter = 39.3701
    return meters * inches_per_meter


def feet_to_inches(feet: float | int) -> float:
    """
    Converts feet to inches.

    Parameters
    ----------
    feet: float | int
      A float representing the length in feet.
    Returns
    ----------
      A float representing the equivalent length in inches.
    """
    inches_per_foot = 12
    return feet * inches_per_foot


def g_to_pounds(grams):
    """
    Converts grams to pounds.

    Parameters
    ----------
    grams: float | int
        A float representing the weight in grams.
    Returns
    ----------
      A float representing the equivalent weight in pounds.
    """
    pounds_per_gram = 0.00220462
    return grams * pounds_per_gram


def kg_to_pounds(kg: float | int) -> float:
    """
    Converts kilograms to pounds.

    Parameters
    ----------
    kg: float | int
      A float representing the weight in kilograms.
    Returns
    ----------
      A float representing the equivalent weight in pounds.
    """
    pounds_per_kg = 2.20462
    return kg * pounds_per_kg


def oz_to_pounds(oz: float | int) -> float:
    """
    Converts ounces to pounds.

    Parameters
    ----------
    oz: float | int
        A float representing the weight in ounces.
    Returns
    ----------
      A float representing the equivalent weight in pounds.
    """
    pounds_per_oz = 0.0625
    return oz * pounds_per_oz


converter_map = {
    "cm": cm_to_inches,
    "m": m_to_inches,
    "feet": feet_to_inches,
    "g": g_to_pounds,
    "kg": kg_to_pounds,
    "oz": oz_to_pounds,
}
