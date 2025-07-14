from src.models.user import db
import uuid

class Episode(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    series_id = db.Column(db.String(36), db.ForeignKey('series.id'), nullable=False)
    season_number = db.Column(db.Integer, nullable=False)
    episode_number = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.Text, nullable=False)
    
    series = db.relationship('Series', backref=db.backref('episodes', lazy=True))

    def __repr__(self):
        return f'<Episode {self.title} (S{self.season_number}E{self.episode_number})>'

    def to_dict(self):
        return {
            'id': self.id,
            'series_id': self.series_id,
            'season_number': self.season_number,
            'episode_number': self.episode_number,
            'title': self.title,
            'description': self.description,
            'video_url': self.video_url,
            'series': self.series.to_dict() if self.series else None
        }

