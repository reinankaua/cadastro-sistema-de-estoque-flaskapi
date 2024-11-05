from database.sessao import db

class Estoque(db.Model):
    __tablename__ = 'estoque'
    id = db.Column(db.Integer, primary_key=True)
    ID_Cliente = db.Column(db.String(), nullable=False)
    ID_Produto = db.Column(db.String(), nullable=False)
    Quantidade = db.Column(db.String(), nullable=False, unique=True)