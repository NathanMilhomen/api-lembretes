from models.sqlalchemy import database


class UsuarioModel(database.Model):
    __tablename__ = "usuario_api_lembretes"

    user_id = database.Column(database.Integer, primary_key=True)
    login = database.Column(database.String(40))
    secret = database.Column(database.String(40))
    senha = database.Column(database.String(100))

    # Não passar o id
    def __init__(self, login, senha, secret):
        self.login = login
        self.senha = senha
        self.secret = secret

    def json(self):
        return {
            "user_id": self.user_id,
            "login": self.login
        }

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
