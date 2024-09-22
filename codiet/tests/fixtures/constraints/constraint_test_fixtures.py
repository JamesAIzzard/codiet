from codiet.tests.fixtures import BaseTestFixture
from codiet.optimisation.constraints import FlagConstraint

class ConstraintTestFixtures(BaseTestFixture):

    def create_flag_constraint(self, flag_name:str, value:bool|None) -> FlagConstraint:
        return FlagConstraint(
            flag_name=flag_name,
            value=value,
        )