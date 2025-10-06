""""Module providing view functions for all endpoints."""
from flask import render_template, request, url_for, redirect
import abacatepay
import json  # Conversão dos dados
import urllib  # Envia Requisições a uma URL
from models.database import Exercicio
from models.database import Dica

from models.database import db
import random

# client = abacatepay.AbacatePay("<your-api-key>")
isPaid = False

client = abacatepay.AbacatePay("API-KEY")
ONE_MINUTE = 60

pix_qr = client.pixQrCode.create(
    data='',
    amount=500_00,  # (1)
    description="Assinatura mensal",
    expires_in=ONE_MINUTE,  # (2)
    customer={  # (3)
        "name": "Maria Silva",
        "email": "maria@email.com",
        "cellphone": "(11) 90000-0000",
        "taxId": "506.201.998-22"
    }
)

my_list = [
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
                my_list.append({
                    'title': title,
                    'visibility': 'private' if isPrivate else 'public',
                    'problems': [],
                    'description': description,
                })
            return redirect(url_for('index'))

        if request.method == 'GET':                      
            page = request.args.get('page', 1, type=int)            
            per_page = 2

            exercises = Exercicio.query.paginate(page=page, per_page=per_page)            
            qtd_problems_solved = random.randint(0, len(exercises.items))            

            return render_template('index.html', my_list=my_list, problems_list=exercises, problems_solved=qtd_problems_solved)

    @app.route('/edit_problems_list', methods=['GET'])
    def edit_problems_list():
        exercises = Exercicio.query.all()                
        return render_template('edit_problems_list.html', problems_list=exercises)

    @app.route('/remove_item/<int:exercise_id>', methods=['DELETE'])
    def remove_item(exercise_id=None):
        exercise = Exercicio.query.get(exercise_id)

        if exercise:
            db.session.delete(exercise)
            db.session.commit()

        return redirect(url_for('edit_problems_list'))

    @app.route('/add_problem', methods=['POST'])
    def add_problem():
        newExercise = Exercicio(request.form['tituloInput'], request.form['difficultInput'], float(request.form['solutionRateInput']), request.form['descricaoInput'])
        
        db.session.add(newExercise)
        db.session.commit()

        return redirect(url_for('edit_problems_list'))

    @app.route('/edit_single_problem/<int:id>', methods=['GET', 'POST'])
    def edit_single_problem(id=None):

        if id and request.method == 'GET':
            selected_problem = Exercicio.query.get(id)
            return render_template('edit_single_problem.html', selected_problem=selected_problem)
        elif id and request.method == 'POST':
            selected_problem = Exercicio.query.get(id)

            print(request.form['editNameInput'])
            selected_problem.titulo = request.form['editNameInput']            
            selected_problem.dificuldade = request.form['editDifficultyInput']
            selected_problem.solution_rate = request.form['editSolutionPercentInput']
            db.session.commit()

            return redirect(url_for('index'))        

    @app.route('/store', methods=['GET', 'POST'])
    def store():
        global isPaid
        if request.method == 'GET':
            return render_template('store_page.html', isPaid=isPaid, URL=pix_qr.brcode_base64)
        elif request.method == 'POST':
            pixPago = client.pixQrCode.simulate(pix_qr.id)
            isPaid = True
            return render_template('store_page.html', isPaid=isPaid, paymentStatus=pixPago)

    @app.route('/real_problems', methods=['GET'])
    @app.route('/real_problems/<string:title_slug>', methods=['GET'])
    def real_problems(title_slug=None):

        if title_slug is None:
            url = 'https://leetcode-api-pied.vercel.app/problems'
            response = urllib.request.urlopen(url)
            data = response.read()
            real_problems_list = json.loads(data)

            # {
            #     "id": "1",
            #     "frontend_id": "1",
            #     "title": "Two Sum",
            #     "title_slug": "two-sum",
            #     "url": "https://leetcode.com/problems/two-sum/",
            #     "difficulty": "Easy",
            #     "paid_only": false,
            #     "has_solution": true,
            #     "has_video_solution": true
            # }

            return render_template('real_problems.html', problems_list=real_problems_list)
        else:
            url = 'https://leetcode-api-pied.vercel.app/problem/' + title_slug
            response = urllib.request.urlopen(url)
            data = response.read()
            real_problem = json.loads(data)

            # {
            #     "id": "1",
            #     "frontend_id": "1",
            #     "title": "Two Sum",
            #     "title_slug": "two-sum",
            #     "url": "https://leetcode.com/problems/two-sum/",
            #     "difficulty": "Easy",
            #     "paid_only": false,
            #     "has_solution": true,
            #     "has_video_solution": true
            # }

            return render_template('real_problem_info.html', real_problem=real_problem)
    @app.route('/remove_hint/<int:hint_id>', methods=['DELETE'])
    def remove_hint(hint_id=None):
        hint = Dica.query.get(hint_id)

        if hint:
            db.session.delete(hint)
            db.session.commit()
                    
        return {"success": True, "message": "Dica removida com sucesso"}

    @app.route('/add_hint', methods=['POST'])
    def add_hint():
        data = request.get_json()
        exercicio_id = data.get('exercicio_id')
        hint_text = data.get('hint')

        if exercicio_id and hint_text:
            new_hint = Dica(exercicio_id, hint_text)
            db.session.add(new_hint)
            db.session.commit()
            return {"success": True, "message": "Dica adicionada com sucesso"}

        return {"success": False, "message": "Dados inválidos"}