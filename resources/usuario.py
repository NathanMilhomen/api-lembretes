from flask_restful import Resource, reqparse, request

from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)

from models.usuarioModel import UsuarioModel
from blacklist import BLACKLIST

arguments = reqparse.RequestParser()
arguments.add_argument(
    'login', type=str, required=True, help="The field login can't be empty")
arguments.add_argument(
    'senha', type=str, required=True, help="The field senha can't be empty")
arguments.add_argument(
    'secret', type=str, required=True, help="The field login can't be empty")


class Usuario(Resource):

    @jwt_required
    def get(self, user_id):
        usuario = UsuarioModel.query.get(user_id)
        if usuario:
            return usuario.json()
        return {'message': 'Usuário não encontrado'}, 404

    @jwt_required
    def delete(self, user_id):
        usuario = UsuarioModel.query.get(user_id)
        current_user_id = get_jwt_identity()
        if current_user_id == usuario.user_id:
            usuario.delete_user()
            return {'message': 'Usuário deletado'}, 200

        return {'message': 'Usuário não encontrado ou você está tentando deletar outro usuário'}, 404


class UsuarioCadastro(Resource):

    def post(self):
        if not request.is_json():
            return {"message": "json com os dados faltando"}, 401

        data = arguments.parse_args()

        if UsuarioModel.query.filter_by(login=data['login']).first():
            return {'message': 'Esse usuário já existe'}, 400

        usuario = UsuarioModel(**data)
        usuario.save_user()
        return {'message': 'Usuário criado com sucesso'}, 201


class UsuarioLogin(Resource):

    def post(self):
        data = arguments.parse_args()
        user = UsuarioModel.query.filter_by(login=data['login']).first()
        if user:
            if safe_str_cmp(user.senha, data["senha"]) and safe_str_cmp(user.secret, data["secret"]):
                acess_token = create_access_token(identity=user.login)
                return {"acess_token": acess_token}, 200

            return {"message": "Acesso negado"}, 401
        return {'message': 'Usuário não existe'}, 400


class UsuarioLogout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {"message": "Deslogado com sucesso"}, 200
