from typing import Collection

from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC

class FlagDefinition:

    def __init__(
        self,
        flag_name: str,
        must_contain: Collection[str]|None=None,
        cannot_contain: Collection[str]|None=None,
        implies: Collection[str]|None=None,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._flag_name = flag_name
        self._must_contain = MUC(must_contain) or MUC[str]()
        self._cannot_contain = MUC(cannot_contain) or MUC[str]()
        self._implies = MUC(implies) or MUC[str]()

    @property
    def flag_name(self) -> str:
        return self._flag_name
    
    @property
    def must_contain(self) -> IUC[str]:
        return self._must_contain.immutable
    
    @property
    def cannot_contain(self) -> IUC[str]:
        return self._cannot_contain.immutable
    
    @property
    def implies(self) -> IUC[str]:
        return self._implies.immutable
