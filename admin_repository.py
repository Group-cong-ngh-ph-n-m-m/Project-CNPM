from infrastructure.databases import db
from infrastructure.models.admin_model import AdminEntity

class AdminRepository:
    def get_all(self):
        return AdminEntity.query.all()

    def get_by_id(self, admin_id):
        return AdminEntity.query.get(admin_id)

    def create(self, data):
        admin = AdminEntity(**data)
        db.session.add(admin)
        db.session.commit()
        return admin

    def update(self, admin_id, data):
        admin = AdminEntity.query.get(admin_id)
        if not admin:
            return None
        for key, value in data.items():
            setattr(admin, key, value)
        db.session.commit()
        return admin

    def delete(self, admin_id):
        admin = AdminEntity.query.get(admin_id)
        if not admin:
            return False
        db.session.delete(admin)
        db.session.commit()
        return True
