import typing

from codiet import model


class Ingredient:
    def __init__(
        self,
        name: typing.Optional[str] = None,
        cost_per_ref_qty: typing.Optional[float] = None,
        cost_ref_qty: typing.Optional[float] = None,
        cost_pref_unit: str = "g",
        dens_vol_ref_qty: typing.Optional[float] = None,
        dens_vol_unit: str = "ml",
        dens_mass_ref_qty: typing.Optional[float] = None,
        dens_mass_unit: str = "g",
        piece_mass_ref_num: typing.Optional[float] = None,
        piece_mass_ref_mass: typing.Optional[float] = None,
        piece_mass_ref_units: str = "g",
        flags: typing.Optional[typing.List[str]] = None,
        gi: typing.Optional[float] = None,
        nutrients: typing.Optional[typing.Dict[str, model.nutrients.NutrientRatioData]] = None
    ):
        # Init the members
        # Ingredient name
        self.name = name
        # Cost info
        self.cost_per_ref_qty = cost_per_ref_qty
        self.cost_ref_qty = cost_ref_qty
        self.cost_pref_unit = cost_pref_unit
        # Density info
        self.dens_vol_ref_qty = dens_vol_ref_qty
        self.dens_vol_unit = dens_vol_unit
        self.dens_mass_ref_qty = dens_mass_ref_qty
        self.dens_mass_unit = dens_mass_unit
        # Piece mass info
        self.piece_mass_ref_num = piece_mass_ref_num
        self.piece_mass_ref_mass = piece_mass_ref_mass
        self.piece_mass_ref_units = piece_mass_ref_units
        # Flag info
        if flags is None:
            self.flags = []
        else:
            self.flags = flags
        # GI info
        self.gi = gi
        # Nutrinet info
        if nutrients is None:
            self.nutrients = {}
        else:
            self.nutrients = nutrients