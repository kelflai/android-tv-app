from src.models.user import db
import uuid

class Channel(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    stream_url = db.Column(db.Text, nullable=False)
    logo_url = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.String(36), db.ForeignKey('category.id'), nullable=False)
    
    category = db.relationship('Category', backref=db.backref('channels', lazy=True))

    def __repr__(self):
        return f'<Channel {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'stream_url': self.stream_url,
            'logo_url': self.logo_url,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None
        }

