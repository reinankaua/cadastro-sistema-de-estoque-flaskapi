from database.sessao import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    endereco = db.Column(db.String(), nullable=False)
    contato = db.Column(db.String(), nullable=False, unique=True)
