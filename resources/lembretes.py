from flask_restful import Resource, reqparse
from sqlalchemy.orm import query
from models.lembreteModel import LembreteModel
from decouple import config
# from datetime import timezone, timedelta, datetime
import psycopg2


class Lembretes(Resource):
    path_param = reqparse.RequestParser()
    path_param.add_argument("dia", type=str)
    path_param.add_argument("autor_nome", type=str)
    path_param.add_argument("limit", type=float)
    path_param.add_argument("offset", type=float)

    def normalize_params(
        dia=None,
        autor_nome=None,
        limit=50,
        offset=0
    ):
        if dia and not autor_nome:
            return [{
                "dia": dia
            }, 0]

        elif autor_nome and not dia:
            return [{
                "autor_nome": autor_nome,
                "limit": limit,
                "offset": offset
            }, 1]
        elif autor_nome and dia:
            return [{
                "dia": dia,
                "autor_nome": autor_nome,
                "limit": limit,
                "offset": offset
            }, 2]

        else:
            return None

    def get(self):
        data = self.path_param.parse_args()
        valid_data = {key: data[key] for key in data if data[key] is not None}
        params = Lembretes.normalize_params(**valid_data)
        if not params:
            lembretes = LembreteModel.query.all()
            return [lembrete.convert_to_json() for lembrete in lembretes], 200
        elif params[1] == 1:
            query = """
            SELECT * FROM lembretes_app_lembrete
            where autor_nome = %s
            LIMIT %s OFFSET %s 
            """
        elif params[1] == 2:
            query = """
            SELECT * FROM lembretes_app_lembrete
            WHERE dia = %s AND autor_nome = %s
            LIMIT %s OFFSET %s 
            """
        else:
            query = "SELECT * FROM lembretes_app_lembrete WHERE dia = %s"
        values = tuple([params[0][key] for key in params[0]])
        # from app import cursor
        connection = psycopg2.connect(
            host=config("HOST"), user=config("USER"), password=config("PASSWORD"), database=config("DBNAME"))
        cursor = connection.cursor()
        cursor.execute(query, values)
        result = cursor.fetchall()
        lembretes = []

        for row in result:
            lembretes.append({
                "lembrete_id": row[0],
                "servidor": row[1],
                "nota": row[2],
                "dia": row[3],
                "hora": row[4],
                "autor_id": row[5],
                "autor_nome": row[6],
                "canal": row[7]
            })
        return {"lembretes": lembretes}, 200 if lembretes else 204


class CadastarLembrete(Resource):
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

    def post(self):
        dados = CadastarLembrete.arguments.parse_args()

        lembrete = LembreteModel(**dados)
        try:
            lembrete.save_lembrete()
            return lembrete.convert_to_json()
        except:
            return {'message': 'Erro ao salvar lembrete'}, 500


class Lembrete(Resource):

    def put(self, id):
        pass

    def delete(self, id):
        lembrete = LembreteModel.query.get(id)
        if lembrete:
            lembrete.delete_lembrete()
            return {"message": "lembrete apagado"}, 200
        return {"message": "Esse lembrete não existe"}, 400


# TODO: Terminar put
# Tentar limitar IP de acesso a api
