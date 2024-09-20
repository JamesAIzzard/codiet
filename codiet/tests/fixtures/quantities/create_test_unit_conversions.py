# from codiet.model.quantities import UnitConversion, Quantity

# def _create_test_global_unit_conversions() -> dict[tuple[str, str], UnitConversion]:
#     return {
#         ("millilitre", "litre"): UnitConversion(
#             (
#                 Quantity(unit=self.units["millilitre"], value=1000),
#                 Quantity(unit=self.units["litre"], value=1),
#             )
#         ),
#         ("gram", "kilogram"): UnitConversion(
#             (
#                 Quantity(unit=self.units["gram"], value=1000),
#                 Quantity(unit=self.units["kilogram"], value=1),
#             )
#         )
#     }

# def _create_test_entity_unit_conversions() -> dict[tuple[str, str], UnitConversion]:
#     return {
#         ("gram", "millilitre"): UnitConversion(
#             (
#                 Quantity(unit=self.units["gram"], value=1),
#                 Quantity(unit=self.units["millilitre"], value=1),
#             )
#         ),
#         ("gram", "slice"): UnitConversion(
#             (
#                 Quantity(unit=self.units["gram"], value=100),
#                 Quantity(unit=self.units["whole"], value=1),
#             )
#         )
#     }