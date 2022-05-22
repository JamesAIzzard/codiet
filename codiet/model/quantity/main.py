from multiprocessing.sharedctypes import Value
import typing

from codiet import model, data

_mass_units: typing.Dict[str, float] = {}
_vol_units: typing.Dict[str, float] = {}


def mass_units() -> typing.Dict[str, float]:
    """Returns dict of mass unit names and grams/unit values.
    - Cached for efficiency.
    """
    global _mass_units
    if len(_mass_units) == 0:
        _mass_units = data.quantity.get_mass_units()
    return _mass_units


def vol_units() -> typing.Dict[str, float]:
    """Returns dict of vol unit names and mls/unit values.
    - Cached for efficiency.
    """
    global _vol_units
    if len(_vol_units) == 0:
        _vol_units = data.quantity.get_vol_units()
    return _vol_units

def pc_units() -> str:
    """Returns the string to represent the piece unit."""
    return "pc"


def units_are_masses(*units: str) -> bool:
    """Returns True/False to indicate if EVERY parameter is a mass unit."""
    for unit in units:
        if unit not in mass_units().keys():
            return False
    return True


def units_are_volumes(*units: str) -> bool:
    """Returns True/False to indicate if EVERY parameter is a volumetric unit."""
    for unit in units:
        if unit not in vol_units().keys():
            return False
    return True


def units_are_pieces(*units: str) -> bool:
    """Returns True or false to indicate if EVERY unit is the piece unit."""
    for unit in units:
        if unit != "pc":
            return False
    return True


def unit_is_extended(unit: str) -> bool:
    """Returns True/False to indicate if unit is extended."""
    if unit == pc_units or unit in vol_units().keys():
        return True
    else:
        return False


def _convert_like2like(qty: float, start_unit: str, end_unit: str) -> float:
    """Handles mass<->mass and vol<->vol"""
    # Figure out the conversion factor;
    if units_are_masses(start_unit, end_unit):
        u_i = mass_units()[start_unit]
        u_o = mass_units()[end_unit]
    elif units_are_volumes(start_unit, end_unit):
        u_i = vol_units()[start_unit]
        u_o = vol_units()[end_unit]
    else:  # Units are pieces.
        u_i = 1
        u_o = 1
    k = u_i / u_o
    return qty * k


def _convert_mass_and_vol(
    qty: float, start_unit: str, end_unit: str, g_per_ml: float
) -> float:
    """Handles mass<->vol and vol<->mass"""
    if units_are_masses(start_unit):  # Start unit is mass.
        qty_g = _convert_like2like(qty, start_unit, "g")
        qty_ml = qty_g / g_per_ml
        return _convert_like2like(qty_ml, "ml", end_unit)  # Return vol.
    else:  # Start unit is vol.
        qty_ml = _convert_like2like(qty, start_unit, "ml")
        qty_g = qty_ml * g_per_ml
        return _convert_like2like(qty_g, "g", end_unit)


def _convert_pc_and_mass(
    qty: float, start_unit: str, end_unit: str, piece_mass_g: float
) -> float:
    """Handles pc<->mass and mass<->pc"""
    if units_are_pieces(start_unit):  # Start unit is pc.
        qty_g = qty * piece_mass_g
        return _convert_like2like(qty_g, "g", end_unit)  # Return mass.
    else:  # Start unit is mass.
        qty_g = _convert_like2like(qty, start_unit, "g")
        return qty_g / piece_mass_g  # Return pieces.


def _convert_pc_and_vol(
    qty: float, start_unit: str, end_unit: str, piece_mass_g: float, g_per_ml: float
) -> float:
    """Handles pc<->vol and vol<->pc"""
    if units_are_pieces(start_unit):  # Start unit is pc.
        qty_g = _convert_pc_and_mass(qty, "pc", "g", piece_mass_g)
        return _convert_mass_and_vol(qty_g, "g", end_unit, g_per_ml)  # Return vol.
    else:  # Start unit is vol.
        qty_ml = _convert_like2like(qty, start_unit, "ml")
        qty_g = _convert_mass_and_vol(qty_ml, "ml", "g", g_per_ml)
        return _convert_pc_and_mass(qty_g, "g", "pc", piece_mass_g)  # Return pieces.


def convert_qty_unit(
    qty: float,
    start_unit: str,
    end_unit: str,
    g_per_ml: typing.Optional[float] = None,
    piece_mass_g: typing.Optional[float] = None,
) -> float:
    """Converts any quantity unit to any other quantity unit."""
    # like2like;
    if (
        units_are_masses(start_unit, end_unit)
        or units_are_volumes(start_unit, end_unit)
        or units_are_pieces(start_unit, end_unit)
    ):
        return _convert_like2like(qty, start_unit, end_unit)

    # mass<->vol;
    elif (units_are_masses(start_unit) and units_are_volumes(end_unit)) or (
        units_are_volumes(start_unit) and units_are_masses(end_unit)
    ):
        if g_per_ml is None:
            raise ValueError
        return _convert_mass_and_vol(qty, start_unit, end_unit, g_per_ml)

    # pc<->mass;
    elif (units_are_pieces(start_unit) and units_are_masses(end_unit)) or (
        units_are_masses(start_unit) and units_are_pieces(end_unit)
    ):
        if piece_mass_g is None:
            raise ValueError
        return _convert_pc_and_mass(qty, start_unit, end_unit, piece_mass_g)

    # pc->vol;
    elif (units_are_pieces(start_unit) and units_are_volumes(end_unit)) or (
        units_are_volumes(start_unit) and units_are_pieces(end_unit)
    ):
        if piece_mass_g is None or g_per_ml is None:
            raise ValueError
        return _convert_pc_and_vol(qty, start_unit, end_unit, piece_mass_g, g_per_ml)

    else:
        raise LookupError("Unable to find a converter for this combination of units.")


def convert_density_unit(
    qty: float,
    start_mass_unit: str,
    start_vol_unit: str,
    end_mass_unit: str,
    end_vol_unit: str,
) -> float:
    """Converts any density unit to any other density unit."""
    # m_in/v_in = k(m_out/v_out) => k = (m_in*v_out)/(v_in*m_out)
    # Set the conversion factors;
    m_in = mass_units()[start_mass_unit]
    m_out = mass_units()[end_mass_unit]
    v_in = vol_units()[start_vol_unit]
    v_out = vol_units()[end_vol_unit]
    # Calc ratio;
    k = (m_in * v_out) / (m_out * v_in)

    return qty * k
