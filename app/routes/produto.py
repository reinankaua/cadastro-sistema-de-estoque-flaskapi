from flask import request, jsonify
from database.sessao import db
from model.produto import Produto


def register_routes_produto(app):
    @app.route('/cadastrar/produto', methods=['POST'])
    def criar_produto():

        data = request.get_json(force=True)

        nome = data.get('Nome')
        codigo = data.get('Código')
        categoria = data.get('Categoria')

        if not all([nome, codigo, categoria]):
            return jsonify({'erro': 'Nome, codigo e categoria são obrigatorios'}), 400

        produto_existente = Produto.query.filter_by(codigo=codigo).first()

        if produto_existente:
            return jsonify({'erro': 'codigo já registrado para outro produto'}), 409

        try:
            novo_produto = Produto(
                nome=nome,
                codigo=codigo,
                categoria=categoria,
            )
            db.session.add(novo_produto)
            db.session.commit()
            return jsonify({'mensagem': 'Novo produto cadastrado'}), 200

        except Exception as err:
            db.session.rollback()
            return jsonify({'erro': err}), 500

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