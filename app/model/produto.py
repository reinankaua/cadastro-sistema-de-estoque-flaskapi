from database.sessao import db

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    codigo = db.Column(db.String(), nullable=False, unique=True)
    categoria = db.Column(db.String(), nullable=False)

