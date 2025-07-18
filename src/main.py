import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.category import Category
from src.models.channel import Channel
from src.models.movie import Movie
from src.models.series import Series
from src.models.episode import Episode
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.content import content_bp
from src.routes.admin import admin_bp
from src.routes.user_management import user_management_bp

# Inicializando a aplicação
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitando CORS
CORS(app)

# Registrando Blueprints para as rotas
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(content_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(user_management_bp, url_prefix='/api/admin')

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Verificar se a pasta 'database' existe
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'database')):
    os.makedirs(os.path.join(os.path.dirname(__file__), 'database'))

# Inicializando o banco de dados
db.init_app(app)

with app.app_context():
    db.create_all()

    # Criando usuários padrão, caso não existam
    from src.utils.user_manager import UserManager
    from src.utils.content_manager import ContentManager
    if UserManager.get_user_count() == 0:
        UserManager.create_default_users()
        print("Usuários padrão criados automaticamente")

    # Criando conteúdo de exemplo, caso não exista
    stats = ContentManager.get_content_stats()
    if stats['categories'] == 0:
        ContentManager.create_sample_content()
        print("Conteúdo de exemplo criado automaticamente")

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Configuração do servidor para execução em produção
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)  # Permitindo a configuração da porta via variável de ambiente
    app.run(host='0.0.0.0', port=port, debug=False)  # Desabilitando debug em produção
