from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import db, User, Routine, Execution
from datetime import date

# Blueprint para organizar as rotas
bp = Blueprint('api', __name__)

@bp.route('/usuarios', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(username=data.get('username'))
    
    try:
        # Tenta salvar no banco
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Usuário criado com sucesso!", "id": new_user.id}), 201
    
    except IntegrityError:
        # Se o banco reclamar de duplicidade, desfaz a ação e avisa o Frontend
        db.session.rollback() 
        return jsonify({"message": "Este nome de usuário já está em uso."}), 400

@bp.route('/rotinas', methods=['POST'])
def create_routine():
    data = request.get_json()
    new_routine = Routine(
        user_id=data.get('user_id'),
        name=data.get('name')
    )
    db.session.add(new_routine)
    db.session.commit()
    return jsonify({"message": "Rotina criada com sucesso!", "id": new_routine.id}), 201

@bp.route('/rotinas/<int:user_id>', methods=['GET'])
def list_routines(user_id):
    routines = Routine.query.filter_by(user_id=user_id).all()
    output = []
    for r in routines:
        output.append({
            "id": r.id,
            "name": r.name,
            "is_active": r.is_active
        })
    return jsonify({"rotinas": output}), 200

@bp.route('/rotinas/<int:routine_id>/status', methods=['PUT'])
def toggle_routine_status(routine_id):
    data = request.get_json()
    routine = Routine.query.get_or_404(routine_id)
    routine.is_active = data.get('is_active', routine.is_active)
    db.session.commit()
    return jsonify({"message": f"Status da rotina atualizado para {'Ativo' if routine.is_active else 'Inativo'}"}), 200

@bp.route('/rotinas/executar', methods=['POST'])
def execute_routine():
    data = request.get_json()
    routine_id = data.get('routine_id')
    
    routine = Routine.query.get(routine_id)
    if not routine:
        return jsonify({"error": "Rotina não encontrada."}), 404

    # REGRA DE NEGÓCIO 1: A rotina precisa estar ativa
    if not routine.is_active:
        return jsonify({"error": "Esta rotina está inativa e não pode ser executada."}), 400

    today = date.today()
    
    # REGRA DE NEGÓCIO 2: Apenas uma execução por dia
    already_executed = Execution.query.filter_by(
        routine_id=routine_id, 
        execution_date=today
    ).first()

    if already_executed:
        return jsonify({"error": "Esta rotina já foi registrada hoje. Evitando inconsistência de dados."}), 400

    # Registrar a execução
    new_execution = Execution(routine_id=routine_id, execution_date=today)
    db.session.add(new_execution)
    db.session.commit()

    return jsonify({"message": "Rotina executada com sucesso!"}), 201

@bp.route('/rotinas/usuario/<int:user_id>', methods=['GET'])
def get_routines(user_id):
    """Consulta de dados (READ) - Retorna todas as rotinas de um usuário"""
    rotinas = Routine.query.filter_by(user_id=user_id).all()
    
    if not rotinas:
        return jsonify({"message": "Nenhuma rotina encontrada para este usuário."}), 404
        
    resultado = [
        {
            "id": r.id, 
            "name": r.name, 
            "is_active": r.is_active,
            "category_id": r.category_id
        } for r in rotinas
    ]
    return jsonify(resultado), 200

@bp.route('/rotinas/<int:routine_id>', methods=['DELETE'])
def delete_routine(routine_id):
    """Remoção de dados (DELETE) - Apaga uma rotina do banco"""
    rotina = Routine.query.get(routine_id)
    
    if not rotina:
        return jsonify({"error": "Rotina não encontrada."}), 404
        
    try:
        # Apaga primeiro as execuções ligadas a esta rotina (Integridade Referencial)
        from models import Execution
        Execution.query.filter_by(routine_id=routine_id).delete()
        
        # Agora apaga a rotina de forma segura
        db.session.delete(rotina)
        db.session.commit()
        return jsonify({"message": "Rotina e histórico removidos com sucesso!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Erro interno ao remover os dados."}), 500