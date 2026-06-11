from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Relacionamento 1:N com Rotinas
    routines = db.relationship('Routine', backref='user', lazy=True)

# --- A NOSSA NOVA 4ª TABELA (Requisito 1.2) ---
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    # Relacionamento 1:N com Rotinas
    routines = db.relationship('Routine', backref='category', lazy=True)

class Routine(db.Model):
    __tablename__ = 'routines'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # NOVA CHAVE ESTRANGEIRA: Liga a Rotina à Categoria
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True) 
    
    name = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    executions = db.relationship('Execution', backref='routine', lazy=True)

class Execution(db.Model):
    __tablename__ = 'executions'
    id = db.Column(db.Integer, primary_key=True)
    routine_id = db.Column(db.Integer, db.ForeignKey('routines.id'), nullable=False)
    date = db.Column(db.Date, default=date.today, nullable=False)