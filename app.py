from flask import Flask
from flask_restful import Resource, Api
from resources.lembretes import Lembretes, Lembrete
from decouple import config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def cria_banco():
    database.create_all()


api.add_resource(Lembretes, '/lembretes')
api.add_resource(Lembrete, '/lembrete/<string:id>')


if __name__ == '__main__':
    from models.sqlalchemy import database
    database.init_app(app)
    app.run(debug=True)
