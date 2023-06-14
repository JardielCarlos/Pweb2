from flask_restful import Resource, reqparse, marshal
from helpers.logger import logger

from model.mensagem import Message, msgError
from model.usuario import Usuario

from helpers.auth.token_handler import token_creator

parser = reqparse.RequestParser()

parser.add_argument("email", type=str, help="Email não informado", required=True)
parser.add_argument("senha", type=str, help="Senha não informada", required=True)


class Login(Resource):
    def post(self):
        args = parser.parse_args()
        user = Usuario.query.filter_by(email=args["email"]).first()
        if user is None:
            logger.error(f"Usuario de email: {args['email']} não encontrado")

            codigo = Message(1, f"email:{args['email']} não encontrado")
            return marshal(codigo, msgError), 404

        if not user.verify_password(args['senha']):
            codigo = Message(1, "Senha Incorreta ou inexistente")
            return marshal(codigo, msgError), 404

        token = token_creator.create(user.tipo)

        return {"token": token}, 200
