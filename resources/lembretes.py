from flask_restful import Resource, reqparse
from models.lembreteModel import LembreteModel


class Lembretes(Resource):
    def get(self):
        lembretes = LembreteModel.query.all()
        return [lembrete.convert_to_json() for lembrete in lembretes]


class Lembrete(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('id')
    arguments.add_argument('nota')
    arguments.add_argument('dia')
    arguments.add_argument('hora')
    arguments.add_argument('autor_id')
    arguments.add_argument('autor_nome')

    def get(self, id):
        return {"message": "get not implemented"}

    def post(self, id):
        dados = Lembrete.arguments.parse_args()
        lembrete = LembreteModel(**dados)
        try:
            lembrete.save_lembrete()
            return lembrete.convert_to_json()
        except:
            return {'message': 'erro'}, 404
