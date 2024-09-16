"""This module contains the UsesDomainService class."""

from codiet.model.domain_service.domain_service import DomainService

class UsesDomainService:
    
    """Base class for all classes that use the domain service singleton."""
    def __init__(self, *args, **kwargs) -> None:
        """Initializes the class."""
        super().__init__(*args, **kwargs)
        self._domain_service = DomainService.get_instance()

    @property
    def domain_service(self) -> DomainService:
        """Get the domain service."""
        return self._domain_service