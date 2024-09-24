from codiet.model.flags import Flag, HasFlags

class Solution(HasFlags):
    
    def get_flag(self, name: str) -> Flag:
        raise NotImplementedError