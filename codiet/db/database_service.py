from codiet.db.repository import Repository

class DatabaseService:
    def __init__(self, repo: Repository):
        self.repo = repo