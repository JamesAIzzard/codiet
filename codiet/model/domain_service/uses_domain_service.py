from codiet.model.domain_service.domain_service import DomainService

class UsesDomainService:
    _domain_service: DomainService|None = None

    @classmethod
    def get_domain_service(cls) -> DomainService:
        if cls._domain_service is None:
            cls._domain_service = DomainService.get_instance()
        return cls._domain_service # type: ignore
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def domain_service(self) -> DomainService:
        return self.get_domain_service()