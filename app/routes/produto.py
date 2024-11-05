from flask import request, jsonify
from database.sessao import db
from model.produto import Produto


def register_routes_produto(app):
    @app.route('/cadastrar/produto', methods=['POST'])
    def criar_produto():
        data = request.get_json(force=True)

         nome=data.get('Nome'),
         codigo=data.get('Código'),
         categoria=data.get('Categoria'),

         if not  all([nome, codigo, categoria]):
             return jsonify({'erro': 'Nome, codigo e categoria são obrigatorios'}) . 400
            produto_existente = Produto.query.filter_by(categoria=categoria).first()

        if Produto_existente:
             return jsonify('erro': 'endereço já registrado para outro produto'}) , 409
        novo_produto = Produto(
            nome=nome,
            codigo=codigo,
            categoria=categoria,
        )
        try:
            db.session.add(novo_produto)
            db.session.commit()
            return jsonify('mensagem': 'Novo produto cadastrado'}) , 200

        except Integrityerror:
            db.session.rollback()
            return jsonify('erro': 'Erro de integridade ao cadastrar produto'}) , 500

    
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


   @app.route('/atualizar/cliente/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = Produto.get_json()

    produto = Produto.query.get_or_404(id)
    novo_nome = data.get('Nome', produto.nome)
    novo_codigo = data.get('Código', produto.codigo)
    novo_categoria = data.get('Categoria', produto.categoria)

    produto_existente = Produto.query.filter_by(categoria=novo_categoria).first()

    if produto_existente and produto_existente.id != produto.id:
        return jsonify({'erro': 'categoria já registrada para outro cliente'}), 409

    produto.nome = novo_nome
    produto.codigo = novo_codigo
    produto.categoria = novo_categoria

    try:
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar produto}), 500

 return jsonify({"mensagem": "Produto atualizado com sucesso."}), 200
