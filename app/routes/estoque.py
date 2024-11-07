from flask import Flask, request, jsonify
from model.estoque import Estoque
import pandas as pd

app = Flask(__name__)

# Carregar o CSV no DataFrame
estoque_df = pd.read_csv("estoque.csv")


@app.route('/estoque/', methods=['GET'])
def listar_estoque():
    cliente = request.args.get('ID_Cliente')
    produto = request.args.get('ID_Produto')

    # Copia o DataFrame para aplicar filtros
    filtro_df = estoque_df.copy()

    # Aplica o filtro por cliente
    if cliente:
        filtro_df = filtro_df[filtro_df['id_cliente'] == int(cliente)]

    # Aplica o filtro por produto
    if produto:
        filtro_df = filtro_df[filtro_df['id_produto'] == int(produto)]

    #Converter o DF filtrado em uma lista
    resultado = filtro_df.to_dict(orient='records')

    return jsonify(resultado), 200


if __name__ == '__main__':
    app.run(debug=True)