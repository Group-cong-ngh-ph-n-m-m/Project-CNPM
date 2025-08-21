from infrastructure.databases import db
from infrastructure.models.service_model import ServiceEntity

class ServiceRepository:
    def get_all(self):
        return ServiceEntity.query.all()

    def get_by_id(self, service_id):
        return ServiceEntity.query.get(service_id)

    def create(self, data):
        service = ServiceEntity(**data)
        db.session.add(service)
        db.session.commit()
        return service

    def update(self, service_id, data):
        service = ServiceEntity.query.get(service_id)
        if not service:
            return None
        for key, value in data.items():
            setattr(service, key, value)
        db.session.commit()
        return service

    def delete(self, service_id):
        service = ServiceEntity.query.get(service_id)
        if not service:
            return False
        db.session.delete(service)
        db.session.commit()
        return True
