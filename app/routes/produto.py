from flask import request, jsonify
from database.sessao import db
from model.produto import Produto


def register_routes_produto(app):
    @app.route('/cadastrar/produto', methods=['POST'])
    def criar_produto():
        data = request.get_json(force=True)

        novo_produto = Produto(
            nome=data.get('nome'),
            codigo=data.get('codigo'),
            categoria=data.get('categoria'),
        )

        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({'mensagem': 'Novo produto cadastrado'}), 200

    @app.route('/listar/produto', methods=['GET'])
    def listar_produto():
        produtos = Produto.query.all()

        resultados = [{
                'id': produto.id,
                'nome': produto.nome,
                'codigo': produto.codigo,
                'categoria': produto.categoria,
            } for produto in produtos
        ]

        return jsonify(resultados), 200

    @app.route('/listar/produto/<int:id>', methods=['GET'])
    def listar_produto_por_id(id):
        produto = Produto.query.get_or_404(id)

        resultado = {
            'id': produto.id,
            'nome': produto.nome,
            'codigo': produto.codigo,
            'categoria': produto.categoria,
        }

        return jsonify(resultado), 200


    @app.route('/atualizar/produto/<int:id>', methods=['PUT'])
    def atualizar_produto(id):
        data = request.get_json()

        produto = Produto.query.get_or_404(id)
        produto.nome = data.get('nome', produto.nome)
        produto.codigo = data.get('codigo', produto.codigo)
        produto.categoria = data.get('categoria', produto.categoria)

        db.session.add(produto)
        db.session.commit()

        return jsonify({"mensagem": "Produto atualizado com sucesso."}), 200

