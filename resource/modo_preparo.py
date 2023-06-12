from flask_restful import Resource, reqparse, marshal
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError

from model.modo_preparo import ModoPreparo, modoPreparoFields

parser = reqparse.RequestParser()

parser.add_argument("text", type=str, help="text nao informada", required=True)

class ModosPreparo(Resource):
    
    def get(self):
      logger.info("ModosPreparo listados com sucesso")
      return marshal(ModoPreparo.query.all(), modoPreparoFields), 200
    
    def post(self):
       
      args = parser.parse_args()

      try:
        modoPreparo = ModoPreparo(args['text'])

        db.session.add(modoPreparo)
        db.session.commit()

        logger.info(f"Medida Caseira de id: {modoPreparo.id} criado com sucesso")
        return marshal(modoPreparo, modoPreparoFields), 201
      except:
        logger.error("Error ao cadastrar Modo de preparo")

        codigo = Message(2, "Error ao cadastrar Modo de preparo")
        return marshal(codigo, msgError), 400
      
class ModosPreparoId(Resource):

  def get(self, id):
    logger.info(f"Modo de preparo de id: {id} listada com sucesso")

    return marshal(ModoPreparo.query.get(id), modoPreparoFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      modoPreparoBd = ModoPreparo.query.get(id)

      if modoPreparoBd is None:
        logger.error(f"Modo de preparo de id: {id} nao encontrado")

        codigo = Message(1, f"Modo de preparo de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      modoPreparoBd.text = args["text"]

      db.session.add(modoPreparoBd)
      db.session.commit()

      logger.info(f"Modo de preparo de id: {id} atualizado com sucesso")
      return marshal(modoPreparoBd, modoPreparoFields), 200
    except:
      logger.error("Erro ao atualizar Modo de preparo")
      codigo = Message(2, "Erro ao atualizar Modo de preparo")
      return marshal(codigo, msgError)
    
  def delete(self, id):
    modoPreparoBd = ModoPreparo.query.get(id)
    
    if modoPreparoBd is None:
      logger.error(f"Modo de preparo de id: {id} nao encontrado")
      codigo = Message(1, f"Modo de preparo de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    db.session.delete(modoPreparoBd)
    db.session.commit()

    logger.info(f"Modo de preparo de id: {id} deletado com sucesso")
    return {}, 200