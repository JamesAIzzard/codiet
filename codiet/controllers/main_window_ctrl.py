class MainWindowCtrl:
    def __init__(self, view, db_service):
        self.view = view
        self.db_service = db_service

        # Connect the signals and slots
        self.view.new_ingredient_action.triggered.connect(self.on_new_ingredient_clicked)
        self.view.new_recipe_action.triggered.connect(self.on_new_recipe_clicked)

    def on_new_ingredient_clicked(self):
        self.view.show_ingredient_editor()
        print("New Ingredient clicked")

    def on_new_recipe_clicked(self):
        self.view.show_recipe_editor()
        print("New Recipe clicked")