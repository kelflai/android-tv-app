from src.models.user import db
import uuid

class Category(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'filme', 'serie', 'canal'

    def __repr__(self):
        return f'<Category {self.name} ({self.type})>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        }

