class FlagNotDefinedError(ValueError):
    def __init__(self, flag_name, parent_instance_name):
        super().__init__(f"Flag {flag_name} is not defined on {parent_instance_name}.")
        self.flag_name = flag_name
        self.parent_instance_name = parent_instance_name