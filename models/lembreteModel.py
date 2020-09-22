from models.sqlalchemy import database


class LembreteModel(database.Model):
    __tablename__ = 'lembretes_app_lembrete'

    id = database.Column(
        database.Integer, primary_key=True)
    nota = database.Column(database.String(100))
    dia = database.Column(database.String(5))
    hora = database.Column(database.String(5))
    autor_id = database.Column(database.String(30))
    autor_nome = database.Column(database.String(30))

    def __init__(self, id, nota, dia, hora, autor_id, autor_nome):
        self.id = id
        self.nota = nota
        self.dia = dia
        self.hora = hora
        self.autor_id = autor_id
        self.autor_nome = autor_nome

    def convert_to_json(self):
        return {
            "id": self.id,
            "nota": self.nota,
            "dia": self.dia,
            "hora": self.hora,
            "authorID": self.autor_id,
            "authorName": self.autor_nome
        }

    def save_lembrete(self):
        database.session.add(self)
        database.session.commit()

    # def delete_lembrete(self):
    #     database.session.delete(self)
    #     database.session.commit()
