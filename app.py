from blacklist import BLACKLIST
from models.sqlalchemy import database
from decouple import config
from resources.usuario import UsuarioCadastro, Usuario, UsuarioLogin, UsuarioLogout
from resources.lembretes import CadastarLembrete, Lembretes, Lembrete
from flask import Flask, request, render_template
from flask_restful import Api
from flask_jwt_extended import JWTManager, exceptions
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = config("SECRET_KEY")
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['BUNDLE_ERRORS'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSON_AS_ASCII'] = False
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(token):
    return token['jti'] in BLACKLIST


@jwt.revoked_token_loader
def invalid_acess_token():
    return {"message": "Você não está logado"}, 401


@jwt.invalid_token_loader
def invalid_acess_token(reason):
    return {"message": f"Token invalido",
            "error": reason}


database.init_app(app)
api = Api(app)


@app.before_first_request
def cria_banco():
    database.create_all()


@app.errorhandler(exceptions.NoAuthorizationError)
def handle_exception_header(error):
    return {"message": "Você precisa logar para fazer esta ação"}, 401


api.add_resource(Lembretes, "/lembretes")
api.add_resource(CadastarLembrete, "/cadastrar/lembrete")
api.add_resource(Lembrete, "/lembrete/<string:id>")
api.add_resource(Usuario, "/usuario/<string:user_id>")
# api.add_resource(UsuarioCadastro, "/cadastro")
api.add_resource(UsuarioLogin, "/login")
api.add_resource(UsuarioLogout, "/logout")


@app.route("/create_html", methods=["POST"])
def html():
    data = request.form
    html = data['html']
    author_id = data['author_id']
    path = f"templates/{author_id}.html"

    if not (html and author_id):
        return '<html><body><h1>Houve um problema.</h1></body></html>'

    # os.makedirs('src/' + author_id + '/')
    arquivo = open(path, "w", encoding="utf-8")
    arquivo.write(html)
    arquivo.close()

    return {"message": "ok"}


@app.route('/html/<id>', methods=['GET'])
def get_html(id):

    return render_template(f"{id}.html")


if __name__ == '__main__':
    app.run(debug=True)
