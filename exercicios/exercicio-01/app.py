from flask import flask
from controllers import routes
    
app = Flask(__name__, template_folder='views')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)