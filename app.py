from blacklist import BLACKLIST
from models.sqlalchemy import database
from decouple import config
from resources.usuario import UsuarioCadastro, Usuario, UsuarioLogin, UsuarioLogout
from resources.lembretes import CadastarLembrete, Lembretes, Lembrete
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, exceptions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnybody'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalid_acess_token():
    return jsonify({'message': 'You are not logged'}), 401


database.init_app(app)
api = Api(app)


@app.before_first_request
def cria_banco():
    database.create_all()


@app.errorhandler(exceptions.NoAuthorizationError)
def handle_exception_header(error):
    return {"message": "Você precisa estar logado para fazer esta ação"}, 401


api.add_resource(Lembretes, "/lembretes")
api.add_resource(CadastarLembrete, "/cadastrar/lembrete")
api.add_resource(Lembrete, "/lembrete/<string:id>")
api.add_resource(Usuario, "/usuario/<string:user_id>")
api.add_resource(UsuarioCadastro, "/cadastro")
api.add_resource(UsuarioLogin, "/login")
api.add_resource(UsuarioLogout, "/logout")

if __name__ == '__main__':

    app.run(debug=True)
