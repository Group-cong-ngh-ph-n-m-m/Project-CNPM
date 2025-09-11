from typing import List, Optional
from domain.service import Service
from infrastructure.models.service import ServiceModel
from infrastructure.databases import db

class ServiceRepository:
    def get_all(self) -> List[Service]:
        services = ServiceModel.query.all()
        return [
            Service(id=s.id, name=s.name, description=s.description, price=s.price)
            for s in services
        ]
    def get_by_id(self, service_id: int) -> Optional[Service]:
        s = ServiceModel.query.get(service_id)
        if not s:
            return None
        return Service(id=s.id, name=s.name, description=s.description, price=s.price)
    def create(self, data: dict) -> Service:
        service_model = ServiceModel(**data)
        db.session.add(service_model)
        db.session.commit()
        return Service(
            id=service_model.id,
            name=service_model.name,
            description=service_model.description,
            price=service_model.price
        )
    def update(self, service_id: int, data: dict) -> Optional[Service]:
        service_model = ServiceModel.query.get(service_id)
        if not service_model:
            return None
        for key, value in data.items():
            setattr(service_model, key, value)
        db.session.commit()
        return Service(
            id=service_model.id,
            name=service_model.name,
            description=service_model.description,
            price=service_model.price
        )
    def delete(self, service_id: int) -> bool:
        service_model = ServiceModel.query.get(service_id)
        if not service_model:
            return False
        db.session.delete(service_model)
        db.session.commit()
        return True
