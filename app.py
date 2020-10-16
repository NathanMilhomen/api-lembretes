from flask import Flask
from flask_restful import Api
from resources.lembretes import CadastarLembrete, Lembretes, Lembrete
from decouple import config
from models.sqlalchemy import database
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database.init_app(app)
api = Api(app)


@app.before_first_request
def cria_banco():
    database.create_all()
    connection = psycopg2.connect(
        host=config("HOST"), user=config("USER"), password=config("PASSWORD"), database=config("DBNAME"))
    cursor = connection.cursor()


api.add_resource(Lembretes, "/lembretes")
api.add_resource(CadastarLembrete, "/cadastrar/lembrete")
api.add_resource(Lembrete, "/lembrete/<string:id>")


if __name__ == '__main__':

    app.run(debug=True)
