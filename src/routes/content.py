from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.models.category import Category
from src.models.channel import Channel
from src.models.movie import Movie
from src.models.series import Series
from src.models.episode import Episode

content_bp = Blueprint('content', __name__)

def require_auth():
    user_id = session.get('user_id')
    if not user_id:
        return None
    user = User.query.get(user_id)
    if not user or not user.active:
        return None
    return user

@content_bp.route('/categories', methods=['GET'])
def get_categories():
    user = require_auth()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    content_type = request.args.get('type')  # 'filme', 'serie', 'canal'
    
    query = Category.query
    if content_type:
        query = query.filter_by(type=content_type)
    
    categories = query.all()
    return jsonify([cat.to_dict() for cat in categories]), 200

@content_bp.route('/channels', methods=['GET'])
def get_channels():
    user = require_auth()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    category_id = request.args.get('category_id')
    
    query = Channel.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    channels = query.all()
    return jsonify([channel.to_dict() for channel in channels]), 200

@content_bp.route('/movies', methods=['GET'])
def get_movies():
    user = require_auth()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    category_id = request.args.get('category_id')
    
    query = Movie.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    movies = query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200

@content_bp.route('/series', methods=['GET'])
def get_series():
    user = require_auth()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    category_id = request.args.get('category_id')
    
    query = Series.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    series = query.all()
    return jsonify([serie.to_dict() for serie in series]), 200

@content_bp.route('/series/<series_id>/episodes', methods=['GET'])
def get_episodes(series_id):
    user = require_auth()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    season = request.args.get('season')
    
    query = Episode.query.filter_by(series_id=series_id)
    if season:
        query = query.filter_by(season_number=int(season))
    
    episodes = query.order_by(Episode.season_number, Episode.episode_number).all()
    return jsonify([episode.to_dict() for episode in episodes]), 200

