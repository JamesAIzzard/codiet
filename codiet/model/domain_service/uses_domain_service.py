from typing import ClassVar, TYPE_CHECKING

if TYPE_CHECKING:
    from codiet.model import DomainService

class UsesDomainService:
    _domain_service: ClassVar['DomainService']
    _setup_run: ClassVar[bool] = False

    @classmethod
    def setup(cls, domain_service: 'DomainService') -> None:
        """Sets up the domain service for the class."""
        cls._domain_service = domain_service
        cls._setup_run = True

    def __init__(self, *args, **kwargs) -> None:
        """Initialises the class."""
        super().__init__(*args, **kwargs)