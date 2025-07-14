from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.routes.m3u_parser import M3UParser
from src.utils.content_manager import ContentManager
import os

admin_bp = Blueprint('admin', __name__)

def require_admin():
    """Check if user is authenticated (simplified admin check)"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    user = User.query.get(user_id)
    if not user or not user.active:
        return None
    return user

@admin_bp.route('/create-sample-content', methods=['POST'])
def create_sample_content():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        if ContentManager.create_sample_content():
            stats = ContentManager.get_content_stats()
            return jsonify({
                'message': 'Conteúdo de exemplo criado com sucesso',
                'stats': stats
            }), 200
        else:
            return jsonify({'error': 'Erro ao criar conteúdo de exemplo'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/content-stats', methods=['GET'])
def get_content_stats():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    stats = ContentManager.get_content_stats()
    return jsonify(stats), 200

@admin_bp.route('/upload-m3u', methods=['POST'])
def upload_m3u():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    data = request.get_json()
    m3u_url = data.get('url')
    
    if not m3u_url:
        return jsonify({'error': 'URL da lista M3U é obrigatória'}), 400
    
    try:
        parser = M3UParser()
        if parser.load_from_url(m3u_url):
            if parser.save_to_database():
                return jsonify({
                    'message': 'Lista M3U processada com sucesso',
                    'stats': {
                        'channels': len(parser.channels),
                        'movies': len(parser.movies),
                        'series': len(parser.series)
                    }
                }), 200
            else:
                return jsonify({'error': 'Erro ao salvar no banco de dados'}), 500
        else:
            return jsonify({'error': 'Erro ao carregar lista M3U'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/upload-m3u-file', methods=['POST'])
def upload_m3u_file():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    try:
        # Save uploaded file temporarily
        upload_dir = os.path.join(os.path.dirname(__file__), '..', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)
        file.save(file_path)
        
        parser = M3UParser()
        if parser.load_from_file(file_path):
            if parser.save_to_database():
                # Clean up uploaded file
                os.remove(file_path)
                return jsonify({
                    'message': 'Arquivo M3U processado com sucesso',
                    'stats': {
                        'channels': len(parser.channels),
                        'movies': len(parser.movies),
                        'series': len(parser.series)
                    }
                }), 200
            else:
                os.remove(file_path)
                return jsonify({'error': 'Erro ao salvar no banco de dados'}), 500
        else:
            os.remove(file_path)
            return jsonify({'error': 'Erro ao processar arquivo M3U'}), 400
            
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@admin_bp.route('/clear-content', methods=['POST'])
def clear_content():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        if ContentManager.clear_all_content():
            return jsonify({'message': 'Todo o conteúdo foi removido'}), 200
        else:
            return jsonify({'error': 'Erro ao limpar conteúdo'}), 500
    except Exception as e:
        return jsonify({'error': f'Erro ao limpar conteúdo: {str(e)}'}), 500

