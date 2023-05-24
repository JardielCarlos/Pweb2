from flask_restful import fields
from helpers.database import db
from model.usuario import Usuario

class Gestor(Usuario):
  __tablename__ = "tb_gestor"

  usuario_id = db.Column(db.Integer ,db.ForeignKey("tb_usuario.id"), primary_key=True)

  __mapper_args__ = {"polymorphic_identity": "gestor"}

  def __init__(self, nome, email, senha):
    super().__init__(nome, email, senha)

  def __repr__(self):
    return f"<Gestor {self.nome}>"