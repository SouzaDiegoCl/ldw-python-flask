""""Module providing view functions for all endpoints."""
from flask import render_template, request, url_for, redirect

myList = [
    {
        "title": "Favorite",
        "visibility": "private",
        "problems": [
            "problem 1",
            "problem 2",
        ],
        "description": "",
    }
]


def init_app(app):
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':

            title = request.form.get('inputTitle')
            description = request.form.get('inputDescription')
            isPrivate = request.form.get('inputIsPrivate')

            if title and description:
                myList.append({
                    'title': title,
                    'visibility': 'private' if isPrivate else 'public',
                    'problems': [],
                    'description': description,
                })
            return redirect(url_for('index'))

        if request.method == 'GET':
            return render_template('index.html', myList=myList)
