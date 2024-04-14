class Recipe:
    def __init__(self):
        self.name: str | None = None
        self.id: int | None = None
        self.description: str | None = None
        self.instructions: str | None = None
        self.ingredients: dict[str, dict] = {}
        self.serve_times: list[str] = []
        self.recipe_types: list[str] = []