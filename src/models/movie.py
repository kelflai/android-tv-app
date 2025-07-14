from src.models.user import db
import uuid

class Movie(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    poster_url = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.Text, nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('category.id'), nullable=False)
    
    category = db.relationship('Category', backref=db.backref('movies', lazy=True))

    def __repr__(self):
        return f'<Movie {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'poster_url': self.poster_url,
            'video_url': self.video_url,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None
        }

