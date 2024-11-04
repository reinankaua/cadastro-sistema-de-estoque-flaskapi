from flask import request, jsonify
from database.sessao import db
from model.produto import Produto


def register_routes_produto(app):
    @app.route('/cadastrar/produto', methods=['POST'])
    def criar_produto():
        data = request.get_json(force=True)

         Nome=data.get('Nome'),
         Código=data.get('Código'),
         Categoria=data.get('Categoria'),

         if not  all([nome, codigo, categoria]):
             return jsonify({'erro': 'Nome, codigo e endereço são obrigatorios'}) . 400
             produto_existente = Produto.query.filter_by(categoria=categoria).first()

        if Produto existente:
             return jsonify('erro': 'endereço já registrado para outro produto'}) , 409
            novo_produto = Produto(
                nome=nome,
                codigo=codigo,
                categpria=categoria,
        )
        try:
            db.session.add(novo_produto)
            db.session.commit()
            return jsonify('mensagem': 'Novo porduto cadastrado'}) , 200

        except Integrityerror:
            db.session.rollback()
            return jsonify('erro': 'ero de integridade ao cadastrar produto'}) , 500
 
        novo_produto = Produto(
            nome=data.get('Nome'),
            codigo=data.get('Código'),
            categoria=data.get('Categoria'),
        )

        db.session.add(novo_produto)
        db.session.commit()

        return jsonify({'mensagem': 'Novo produto cadastrado'}), 200

    @app.route('/listar/produto', methods=['GET'])
    def listar_produto():
        produtos = Produto.query.all()

        resultados = [{
                'Id': produto.id,
                'Nome': produto.nome,
                'Código': produto.codigo,
                'Categoria': produto.categoria,
            } for produto in produtos
        ]

        return jsonify(resultados), 200

    @app.route('/listar/produto/<int:id>', methods=['GET'])
    def listar_produto_por_id(id):
        produto = Produto.query.get_or_404(id)

        resultado = {
            'Id': produto.id,
            'Nome': produto.nome,
            'Código': produto.codigo,
            'Categoria': produto.categoria,
        }

        return jsonify(resultado), 200


    @app.route('/atualizar/produto/<int:id>', methods=['PUT'])
    def atualizar_produto(id):
        data = request.get_json()

        produto = Produto.query.get_or_404(id)
        produto.nome = data.get('Nome', produto.nome)
        produto.codigo = data.get('Código', produto.codigo)
        produto.categoria = data.get('Categoria', produto.categoria)

        db.session.add(produto)
        db.session.commit()

        return jsonify({"mensagem": "Produto atualizado com sucesso."}), 200

