from flask import request, jsonify
from database.sessao import db
from model.cliente import Cliente
from sqlalchemy.exc import SQLAlchemyError


def register_routes_cliente(app):
    @app.route('/cadastrar/cliente', methods=['POST'])
    def criar_cliente():

        data = request.get_json(force=True)

        nome = data.get('Nome')
        endereco = data.get('Endereço')
        contato = data.get('Contato')

        if not all([nome, endereco, contato]):
            return jsonify({'erro': 'Nome, Endereço e Contato são obrigatórios'}), 400

        cliente_existente = Cliente.query.filter_by(contato=contato).first()

        if cliente_existente:
            return jsonify({'erro': 'Contato já registrado para outro cliente'}), 409

        try:
            novo_cliente = Cliente(
                nome=nome,
                endereco=endereco,
                contato=contato,
            )
            db.session.add(novo_cliente)
            db.session.commit()
            return jsonify({'mensagem': 'Novo cliente cadastrado'}), 200

        except Exception as err:
            db.session.rollback()
            return jsonify({'erro': err}), 500

    @app.route('/listar/cliente', methods=['GET'])
    def listar_cliente():

        clientes = Cliente.query.all()

        resultados = [{
                'id': cliente.id,
                'nome': cliente.nome,
                'endereco': cliente.endereco,
                'contato': cliente.contato,
            } for cliente in clientes
        ]

        return jsonify(resultados), 200

    @app.route('/listar/cliente/<int:id>', methods=['GET'])
    def listar_cliente_por_id(id):

        cliente = Cliente.query.get_or_404(id)

        resultado = {
            'id': cliente.id,
            'nome': cliente.nome,
            'endereco': cliente.endereco,
            'contato': cliente.contato,
        }

        return jsonify(resultado), 200

    @app.route('/atualizar/cliente/<int:id>', methods=['PUT'])
    def atualizar_cliente(id):
        data = request.get_json()

        cliente = Cliente.query.get_or_404(id)

        novo_nome = data.get('Nome', cliente.nome)
        novo_endereco = data.get('Endereço', cliente.endereco)
        novo_contato = data.get('Contato', cliente.contato)

        cliente_existente = Cliente.query.filter_by(contato=novo_contato).first()

        if cliente_existente and cliente_existente.id != cliente.id:
            return jsonify({'erro': 'Contato já registrado para outro cliente'}), 409

        cliente.nome = novo_nome
        cliente.endereco = novo_endereco
        cliente.contato = novo_contato

        try:
            db.session.commit()

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({"erro": "Erro ao atualizar cliente"}), 500

        return jsonify({"mensagem": "Cliente atualizado com sucesso."}), 200