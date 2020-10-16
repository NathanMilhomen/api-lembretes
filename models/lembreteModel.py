from models.sqlalchemy import database


class LembreteModel(database.Model):
    __tablename__ = 'lembretes_app_lembrete'

    lembrete_id = database.Column(
        database.Integer, primary_key=True)
    servidor = database.Column(database.String(50))
    nota = database.Column(database.String(100))
    dia = database.Column(database.String(5))
    hora = database.Column(database.String(5))
    autor_id = database.Column(database.String(30))
    autor_nome = database.Column(database.String(30))
    canal = database.Column(database.String(50))

    def __init__(self, servidor, nota, dia, hora, autor_id, autor_nome, canal):
        self.servidor = servidor
        self.nota = nota
        self.dia = dia
        self.hora = hora
        self.autor_id = autor_id
        self.autor_nome = autor_nome
        self.canal = canal

    def convert_to_json(self):
        return {
            "id": self.lembrete_id,
            "servidor": self.servidor,
            "nota": self.nota,
            "dia": self.dia,
            "hora": self.hora,
            "autor_id": self.autor_id,
            "autor_nome": self.autor_nome,
            "canal": self.canal
        }

    def save_lembrete(self):
        database.session.add(self)
        database.session.commit()

    def delete_lembrete(self):
        database.session.delete(self)
        database.session.commit()
