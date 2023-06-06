from flask_restful import Resource, marshal, reqparse, request
from model.empresa import Empresa, empresaFields
from model.proprietario import Proprietario
from helpers.database import db
from helpers.logger import logger
from model.mensagem import Message, msgError
from model.token import Token, tokenFields

import jwt

parser = reqparse.RequestParser()


parser.add_argument("nome", type=str, help="Nome nao informado", required=True)
parser.add_argument("cnpj", type=str, help="CNPJ nao informado", required=True)
parser.add_argument("proprietario", type=dict, help="proprietario nao informado", required=False)

class Empresas(Resource):
  def get(self):
    rawToken = request.headers["Authorization"]
    if not rawToken:
      logger.error("Sem token!")

      codigo = Message(1, "Sem token!")
      return marshal(codigo, msgError), 401
    
    try:
      token = rawToken.split()[1]
      informationToken = jwt.decode(token, key="1234", algorithms="HS256")

      if informationToken['Tipo'] != 'proprietario':
        logger.error("Usuario sem autorização suficiente!")

        codigo = Message(1, "Usuario sem autorização suficiente!")
        return marshal(codigo, msgError), 403
    except jwt.InvalidSignatureError:
      token = Token("Token invalido!")
      return marshal(token, tokenFields), 401
    
    except jwt.ExpiredSignatureError:
      token = Token("Token Expirado!")

      return marshal(token, tokenFields), 401
    
    logger.info("Empresas listadas com Sucesso")
    return marshal(Empresa.query.all(), empresaFields), 200
  
  def post(self):
    args = parser.parse_args()

    try:
      proprietarioId = args["proprietario"]['id']
      proprietario = Proprietario.query.get(proprietarioId)
      
      if proprietario is None:
        logger.error(f"Proprietario de id: {proprietarioId} nao encontrado")
        
        codigo = Message(1, f"Proprietario de id: {proprietarioId} nao encontrado")
        return marshal(codigo, msgError), 404
      
      empresa = Empresa(args['nome'], args["cnpj"], proprietario)
      
      db.session.add(empresa)
      db.session.commit()

      logger.info(f"Empresa de id: {empresa.id} criado com sucesso")
      return marshal(empresa, empresaFields), 201
    
    except:
      logger.error("Error ao cadastrar o Empresa")

      codigo = Message(2, "Error ao cadastrar a empresa verifique os campos")
      return marshal(codigo, msgError), 400
    
class EmpresaId(Resource):
  def get(self, id):
    empresa = Empresa.query.get(id)

    if empresa is None:
      logger.error(f"Empresa de id: {id} nao encontrado")

      codigo = Message(1, f"Empresa de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404
    
    logger.info(f"Empresa de id: {empresa.id} Listado com Sucesso")
    return marshal(empresa, empresaFields), 200
  
  def put(self, id):
    args = parser.parse_args()

    try:
      empresaBd = Empresa.query.get(id)

      if empresaBd is None:
        logger.error(f"Empresa de id: {id} nao encontrado")

        codigo = Message(1, f"Empresa de id: {id} nao encontrado")
        return marshal(codigo, msgError), 404
      
      empresaBd.nome = args["nome"]
      empresaBd.cnpj = args["cnpj"]

      db.session.add(empresaBd)
      db.session.commit()
      
      logger.info(f"Empresa de id: {id} atualizado com Sucesso")
      return marshal(empresaBd, empresaFields), 200
    
    except:
      logger.error("Error ao atualizar o Empresa")

      codigo = Message(2, "Error ao atualizar o Empresa")
      return marshal(codigo, msgError), 400
    
  def delete(self, id):

    empresaBd = Empresa.query.get(id)

    if empresaBd is None:
      logger.error(f"Empresa de id: {id} nao encontrado")

      codigo = Message(1, f"Empresa de id: {id} nao encontrado")
      return marshal(codigo, msgError), 404

    db.session.delete(empresaBd)
    db.session.commit()
    
    logger.info(f"Empresa de id: {id} deletado com sucesso")
    return {}, 200