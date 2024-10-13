from codiet.optimisation.constraints import FlagConstraint

class ConstraintFactory:

    def create_flag_constraint(self, flag_name: str, flag_value: bool) -> "FlagConstraint":
        return FlagConstraint(flag_name, flag_value)