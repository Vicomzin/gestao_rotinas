import os
from flask import Flask, render_template
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db
from routes import bp

# Carrega as variáveis do arquivo .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configurações do Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///rotinas.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 1. Inicializa o banco de dados (UMA única vez)
    db.init_app(app)
    
    # 2. Inicializa a ferramenta de Migrations
    Migrate(app, db)

    # 3. Registra as rotas (Backend)
    app.register_blueprint(bp, url_prefix='/api')

    # 4. Rota para a interface visual (Frontend)
    @app.route('/')
    def index():
        return render_template('index.html')

    # Repare que removemos o db.create_all() daqui!
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)