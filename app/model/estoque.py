from database.sessao import db

class Estoque(db.Model):
    __tablename__ = 'estoque'
    id = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.String(), nullable=False)
    id_produto = db.Column(db.String(), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
