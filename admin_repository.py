from typing import List, Optional
from domain.admin import Admin                
from infrastructure.models.admin import AdminModel   
from infrastructure.databases import db
class AdminRepository:
    def get_all(self) -> List[Admin]:
        admins = AdminModel.query.all()
        return [
            Admin(id=a.id, username=a.username, email=a.email)
            for a in admins
        ]
    def get_by_id(self, admin_id: int) -> Optional[Admin]:
        a = AdminModel.query.get(admin_id)
        if not a:
            return None
        return Admin(id=a.id, username=a.username, email=a.email)
    def create(self, data: dict) -> Admin:
        admin_model = AdminModel(**data)
        db.session.add(admin_model)
        db.session.commit()
        return Admin(id=admin_model.id, username=admin_model.username, email=admin_model.email)
    def update(self, admin_id: int, data: dict) -> Optional[Admin]:
        admin_model = AdminModel.query.get(admin_id)
        if not admin_model:
            return None
        for key, value in data.items():
            setattr(admin_model, key, value)
        db.session.commit()
        return Admin(id=admin_model.id, username=admin_model.username, email=admin_model.email)
    def delete(self, admin_id: int) -> bool:
        admin_model = AdminModel.query.get(admin_id)
        if not admin_model:
            return False
        db.session.delete(admin_model)
        db.session.commit()
        return True
