from flask import Flask, render_template, for_url

def init_app(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')
    
    
    
    