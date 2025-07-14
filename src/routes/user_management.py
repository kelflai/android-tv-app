from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
from src.utils.user_manager import UserManager

user_management_bp = Blueprint('user_management', __name__)

def require_admin():
    """Check if user is authenticated (simplified admin check)"""
    user_id = session.get('user_id')
    if not user_id:
        return None
    user = User.query.get(user_id)
    if not user or not user.active:
        return None
    return user

@user_management_bp.route('/users', methods=['GET'])
def get_users():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    users = UserManager.get_active_users()
    return jsonify([user.to_dict() for user in users]), 200

@user_management_bp.route('/users/create-defaults', methods=['POST'])
def create_default_users():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    try:
        created_users = UserManager.create_default_users()
        return jsonify({
            'message': f'{len(created_users)} usuários criados com sucesso',
            'created_users': created_users
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao criar usuários: {str(e)}'}), 500

@user_management_bp.route('/users/<user_id>/activate', methods=['POST'])
def activate_user(user_id):
    admin_user = require_admin()
    if not admin_user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    if UserManager.activate_user(user_id):
        return jsonify({'message': 'Usuário ativado com sucesso'}), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404

@user_management_bp.route('/users/<user_id>/deactivate', methods=['POST'])
def deactivate_user(user_id):
    admin_user = require_admin()
    if not admin_user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    if UserManager.deactivate_user(user_id):
        return jsonify({'message': 'Usuário desativado com sucesso'}), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404

@user_management_bp.route('/users/<user_id>/change-password', methods=['POST'])
def change_user_password(user_id):
    admin_user = require_admin()
    if not admin_user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    data = request.get_json()
    new_password = data.get('new_password')
    
    if not new_password:
        return jsonify({'error': 'Nova senha é obrigatória'}), 400
    
    if UserManager.change_password(user_id, new_password):
        return jsonify({'message': 'Senha alterada com sucesso'}), 200
    else:
        return jsonify({'error': 'Usuário não encontrado'}), 404

@user_management_bp.route('/users/stats', methods=['GET'])
def get_user_stats():
    user = require_admin()
    if not user:
        return jsonify({'error': 'Autenticação necessária'}), 401
    
    total_users = UserManager.get_user_count()
    active_users = len(UserManager.get_active_users())
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': total_users - active_users
    }), 200

