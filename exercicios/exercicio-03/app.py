from flask import Flask
from controllers import routes
import pymysql
from models.database import db

app = Flask(__name__, template_folder='views')
routes.init_app(app)

# Define o nome do banco de dados
# SQLAlchemy → conexão ORM para trabalhar com o banco depois que ele existe.
DB_NAME = 'banco_exercicio_03'
PASSWORD = '123'
app.config['DATABASE_NAME'] = DB_NAME
# Passando o endereço do banco ao SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://root@localhost/{DB_NAME}'

if __name__ == '__main__':
    #pymysql → conexão direta para criar/configurar o banco inicial.    
    connection = pymysql.connect(host='localhost', 
                                user='root',              
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Cria o banco de dados, se não existir
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
            connection.commit() 
    except Exception as e:
        print(f'Erro ao criar o banco de dados: {e}')
    finally:
        connection.close()
    
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    
    # Inicia o aplicativo Flask
    app.run(host='0.0.0.0', port=4000, debug=True)
