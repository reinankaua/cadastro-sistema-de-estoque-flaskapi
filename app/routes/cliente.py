from flask import request, jsonify

from database.sessao import db
from model.cliente import Cliente


def register_routes_cliente(app):
    @app.route('/cadastrar/cliente', methods=['POST'])
    def criar_cliente():
        data = request.get_json(force=True)

        novo_cliente = Cliente(
            nome=data.get('nome'),
            endereco=data['endereco'],
            contato=data.get('contato'),
        )

        db.session.add(novo_cliente)
        db.session.commit()

        return jsonify({'mensagem': 'Novo cliente cadastrado'}), 200

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
        cliente.nome = data.get('nome', cliente.nome)
        cliente.endereco = data.get('endereco', cliente.endereco)
        cliente.contato = data.get('contato', cliente.contato)

        db.session.add(cliente)
        db.session.commit()

        return jsonify({"message": "Cliente atualizado com sucesso."}), 200
