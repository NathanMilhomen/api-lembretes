from flask_restful import Resource, reqparse
from models.lembreteModel import LembreteModel


class Lembretes(Resource):
    arguments = reqparse.RequestParser()
    arguments.add_argument('servidor', type=str,
                           required=True, help="Campo obrigatório")
    arguments.add_argument('nota', type=str, required=True,
                           help="Nota não pode ser vazio")
    arguments.add_argument('dia', type=str, required=True,
                           help="Dia não pode ser vazio")
    arguments.add_argument(
        'hora', type=str, required=True, help="Campo hora obrigatório")
    arguments.add_argument('autor_id', type=str,
                           required=True, help="Campo autorID obrigatório")
    arguments.add_argument('autor_nome', type=str,
                           required=True, help="Campo nome obrigatório")
    arguments.add_argument('canal', type=str,
                           required=True, help="Campo canal obrigatório")

    def get(self):
        lembretes = LembreteModel.query.all()
        return [lembrete.convert_to_json() for lembrete in lembretes]

    def post(self):
        dados = Lembretes.arguments.parse_args()
        print(dados)
        lembrete = LembreteModel(**dados)
        # try:
        lembrete.save_lembrete()
        return lembrete.convert_to_json()
        # except:
        #     return {'message': 'Erro ao salvar lembrete'}, 500


class Lembrete(Resource):

    def get(self, id):
        return {"message": "get not implemented"}

    def put(self, id):
        pass

    def delete(self, id):
        pass
