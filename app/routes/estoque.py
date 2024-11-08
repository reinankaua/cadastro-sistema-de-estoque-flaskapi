from flask import request, jsonify
from model.estoque import Estoque
from database.sessao import db

def register_routes_estoque(app):
    @app.route('/cadastrar/estoque', methods=['POST'])
    def criar_estoque():

        data = request.get_json(force=True)

        id_cliente = data.get('ID_Cliente')
        id_produto = data.get('ID_Produto')
        quantidade = data.get('Quantidade')

        if not all([id_cliente, id_produto, quantidade]):
            return jsonify({'erro': 'id_cliente, id_produto e quantidade são obrigatorios'}), 400

        try:
            novo_produto = Estoque(
                id_cliente=id_cliente,
                id_produto=id_produto,
                quantidade=quantidade,
            )
            db.session.add(novo_produto)
            db.session.commit()
            return jsonify({'mensagem': 'Novo registro no estoque cadastrado'}), 200

        except Exception as err:
            db.session.rollback()
            return jsonify({'erro': err}), 500


    @app.route('/listar/estoque', methods=['GET'])
    def listar_estoque():
        lista_estoque = Estoque.query.all()

        resultados = [{
            'id_cliente': estoque.id_cliente,
            'id_produto': estoque.id_produto,
            'quantidade': estoque.quantidade,
            } for estoque in lista_estoque
        ]

        return jsonify(resultados), 200
    @app.route('/listar/estoque/filtro', methods=['GET'])
    def listar_estoque_com_filtros():

        id_cliente = request.args.get('id_cliente')
        id_produto = request.args.get('id_produto')

        query = Estoque.query

        if id_cliente and id_produto:
            query = query.filter_by(id_cliente=id_cliente, id_produto=id_produto)
        elif id_cliente:
            query = query.filter_by(id_cliente=id_cliente)
        elif id_produto:
            query = query.filter_by(id_produto=id_produto)

        estoque_filtrado = query.all()
        resultado = [
            {
                'id_cliente': estoque.id_cliente,
                'id_produto': estoque.id_produto,
                'quantidade': estoque.quantidade,
            } for estoque in estoque_filtrado
        ]

        return jsonify(resultado), 200