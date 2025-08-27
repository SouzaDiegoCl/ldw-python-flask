from flask import Flask, render_template, url_for

def init_app(app):
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')
    
    
    
    