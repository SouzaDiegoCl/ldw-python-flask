from flask import Flask, url_for, render_template
from controllers import routes
from models.database import db
import os


app = Flask(__name__, template_folder='views')
routes.init_app(app)

#Extraindo o diretório absoluto do arquivo
dir = os.path.abspath(os.path.dirname(__file__))

#Criando o arquivo do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir, 'models/games.sqlite3')

#Se for executado diretamente pelo interpretador
if __name__ == '__main__':
    #Enviando o Flask para o SqlAlchemy
    db.init_app(app=app)
    #Verificar no início da aplicação se o BD já existe. Se não, ele cria.
    #Inicia execução e depois fecha o processo (Do mongodb)
    with app.test_request_context():
        db.createAll()
    
    
    #Iniciando o servidor
    app.run(host='0.0.0.0', port=5000, debug=True)