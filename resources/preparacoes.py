from flask_restful import Resource, marshal, reqparse
from helpers.database import db
from helpers.logger import logger
from sqlalchemy.exc import IntegrityError

from model.preparacao import Preparacao, preparacaoFields
from model.preparacao_ingrediente import PreparacaoIngrediente
from model.preparacao_utensilio import PreparacaoUtensilio
from model.modo_preparo import ModoPreparo

from model.mensagem import Message, msgFields
from model.empresa import Empresa


parser = reqparse.RequestParser()

parser.add_argument("nome", type=str, help="Nome não informado", required=True)
parser.add_argument("empresa", type=dict, help="Empresa não informada", required=False)
parser.add_argument("numPorcoes", type=float, help="Numero de porções não informado", required=True)

class Preparacoes(Resource):
  def get(self):
    logger.info("Preparações listadas com sucesso")
    return marshal(Preparacao.query.order_by(Preparacao.criacao).all(), preparacaoFields), 200

  def post(self):
    args = parser.parse_args()
    try:
      empresaId = args["empresa"]["id"]

      empresa = Empresa.query.get(empresaId)

      if empresa is None:
          codigo = Message(1, f"Empresa de id: {empresaId} não encontrado")
          return marshal(codigo, msgFields), 404

      preparacao = Preparacao(args['nome'], args['numPorcoes'], empresa)

      db.session.add(preparacao)
      db.session.commit()

      logger.info(f"Preparacao de id: {preparacao.id} criada com sucesso")
      return marshal(preparacao, preparacaoFields), 201
    except:
        logger.error("Error ao cadastrar preparacao")

        codigo = Message(2, "Error ao cadastrar preparacao")
        return marshal(codigo, msgFields), 400

class PreparacaoId(Resource):
  def get(self, id):
    preparacao = Preparacao.query.get(id)
    print(preparacao.criacao)

    if preparacao is None:
      logger.error(f"Preparação de id: {id} não encontrada")

      codigo = Message(1, f"Preparação de id: {id} não encontrada")
      return marshal(codigo, msgFields), 404

    logger.info(f"Preparacao de id: {id} listada com sucesso")
    return marshal(preparacao, preparacaoFields), 200

  def put(self, id):
    args = parser.parse_args()

    try:
      preparacaoBd = Preparacao.query.get(id)
      if preparacaoBd is None:
        logger.error(f"Preparação de id: {id} não encontrada")

        codigo = Message(1, f"Preparação de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404

      preparacaoBd.nome = args['nome']
      preparacaoBd.numPorcoes = args['numPorcoes']

      db.session.add(preparacaoBd)
      db.session.commit()

      logger.info(f"Preparação de id: {id} atualizada com sucesso")
      return marshal(preparacaoBd, preparacaoFields)
    except:
      logger.error("Erro ao atualizar a Preparação")

      codigo = Message(2, "Erro ao atualizar a Preparação")
      return marshal(codigo, msgFields), 400

  def delete(self, id):
    preparacaoBd = Preparacao.query.get(id)
    preparacaoIngredienteBd = PreparacaoIngrediente.query.filter_by(preparacao_id=id).all()
    preparacaoUtensilioBd = PreparacaoUtensilio.query.filter_by(preparacao_id=id).all()
    modoPreparoBd = ModoPreparo.query.filter_by(preparacao_id=id).all()

    try:
      if preparacaoBd is None:
        logger.error(f"Preparação de id: {id} não encontrada")

        codigo = Message(1, f"Preparação de id: {id} não encontrada")
        return marshal(codigo, msgFields), 404
      
      for i in preparacaoIngredienteBd:
        db.session.delete(i)
      for i in preparacaoUtensilioBd:
        db.session.delete(i)
      for i in modoPreparoBd:
        db.session.delete(i)

      db.session.delete(preparacaoBd)
      db.session.commit()

      logger.info(f"Preparacao de id: {id} deletada com sucesso")
      return {}, 200
    except IntegrityError:
      logger.error(f"Preparação de id: {id} não pode ser apagado ela possui dependencias")
      codigo = Message(1, f"Preparação de id: {id} possui dependencias e nao pode ser deletada, por favor delete as dependencias antes de deletar essa preparacao")
      return marshal(codigo, msgFields), 400
