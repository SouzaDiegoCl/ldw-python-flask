from flask_sqlalchemy import SQLAlchemy
import enum

db = SQLAlchemy()   

class DificuldadeEnum(enum.Enum):
    easy = "Easy"
    medium = "Medium"
    hard = "Hard"

# Classe responsável por criar a entidade "Exercicios" com seus atributos.
class Exercicio(db.Model):
    __tablename__ = "exercicios"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150))
    dificuldade = db.Column(db.Enum(DificuldadeEnum), nullable=False)
    solution_rate = db.Column(db.Float)
    descricao = db.Column(db.Text)

    dicas = db.relationship("Dica", backref="exercicio", cascade="all, delete-orphan")
    
    def __init__(self, titulo, dificuldade, solution_rate, descricao):
        self.titulo = titulo
        self.dificuldade = dificuldade
        self.solution_rate = solution_rate
        self.descricao = descricao

# Classe responsável por criar a entidade "Dicas" com seus atributos.
class Dica(db.Model):
    __tablename__ = "dicas"

    id = db.Column(db.Integer, primary_key=True)    
    exercicio_id = db.Column(db.Integer, db.ForeignKey('exercicios.id'), nullable=False)
    hint = db.Column(db.Text)
    
    def __init__(self, exercicio_id, hint):
        self.exercicio_id = exercicio_id
        self.hint = hint