""""Module providing view functions for all endpoints."""
from flask import render_template, request, url_for, redirect

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

problems_list = [
    {"name": "Sudoku Solver", "solutionPercent": 65.2,
        "difficulty": "Hard", "done": True},
    {"name": "Two Sum", "solutionPercent": 56.2,
        "difficulty": "Easy", "done": True},
    {"name": "Add Two Numbers", "solutionPercent": 46.8,
        "difficulty": "Medium", "done": True},
    {"name": "Longest Substring Without Repeating Characters",
        "solutionPercent": 37.5, "difficulty": "Medium", "done": False},
    {"name": "Median of Two Sorted Arrays",
        "solutionPercent": 44.6, "difficulty": "Hard", "done": False},
    {"name": "Longest Palindromic Substring",
        "solutionPercent": 36.3, "difficulty": "Medium", "done": False},
    {"name": "Zigzag Conversion", "solutionPercent": 52.2,
        "difficulty": "Medium", "done": False},
    {"name": "Reverse Integer", "solutionPercent": 30.7,
        "difficulty": "Medium", "done": False},
    {"name": "String to Integer (atoi)",
     "solutionPercent": 19.7, "difficulty": "Medium", "done": False},
    {"name": "Palindrome Number", "solutionPercent": 59.6,
        "difficulty": "Easy", "done": False},
    {"name": "Regular Expression Matching",
        "solutionPercent": 29.6, "difficulty": "Hard", "done": False},
    {"name": "Container With Most Water",
        "solutionPercent": 58.2, "difficulty": "Medium", "done": False},
    {"name": "Integer to Roman", "solutionPercent": 69.3,
        "difficulty": "Medium", "done": False},
    {"name": "Roman to Integer", "solutionPercent": 65.4,
        "difficulty": "Easy", "done": False},
    {"name": "Longest Common Prefix", "solutionPercent": 46.0,
        "difficulty": "Easy", "done": False},
    {"name": "3Sum", "solutionPercent": 37.6,
        "difficulty": "Medium", "done": False},
    {"name": "3Sum Closest", "solutionPercent": 47.2,
        "difficulty": "Medium", "done": False},
    {"name": "Letter Combinations of a Phone Number",
        "solutionPercent": 64.4, "difficulty": "Medium", "done": False},
    {"name": "4Sum", "solutionPercent": 38.8,
        "difficulty": "Medium", "done": False},
    {"name": "Remove Nth Node From End of List",
        "solutionPercent": 49.7, "difficulty": "Medium", "done": False},
    {"name": "Valid Parentheses", "solutionPercent": 42.8,
        "difficulty": "Easy", "done": False},
    {"name": "Merge Two Sorted Lists", "solutionPercent": 67.2,
        "difficulty": "Easy", "done": False},
    {"name": "Generate Parentheses", "solutionPercent": 77.6,
        "difficulty": "Medium", "done": False},
    {"name": "Merge k Sorted Lists", "solutionPercent": 57.5,
        "difficulty": "Hard", "done": False},
    {"name": "Swap Nodes in Pairs", "solutionPercent": 67.8,
        "difficulty": "Medium", "done": False},
    {"name": "Reverse Nodes in k-Group",
        "solutionPercent": 63.9, "difficulty": "Hard", "done": False},
    {"name": "Remove Duplicates from Sorted Array",
        "solutionPercent": 61.0, "difficulty": "Easy", "done": False},
    {"name": "Remove Element", "solutionPercent": 60.5,
        "difficulty": "Easy", "done": False},
    {"name": "Find the Index of the First Occurrence in a String",
        "solutionPercent": 45.4, "difficulty": "Easy", "done": False},
    {"name": "Divide Two Integers", "solutionPercent": 18.7,
        "difficulty": "Medium", "done": False},
    {"name": "Substring with Concatenation of All Words",
        "solutionPercent": 33.2, "difficulty": "Hard", "done": False},
    {"name": "Next Permutation", "solutionPercent": 43.7,
        "difficulty": "Medium", "done": False},
    {"name": "Longest Valid Parentheses",
        "solutionPercent": 36.8, "difficulty": "Hard", "done": False},
    {"name": "Search in Rotated Sorted Array",
        "solutionPercent": 43.3, "difficulty": "Medium", "done": False},
    {"name": "Find First and Last Position of Element in Sorted Array",
        "solutionPercent": 47.4, "difficulty": "Medium", "done": False},
    {"name": "Search Insert Position", "solutionPercent": 49.6,
        "difficulty": "Easy", "done": False},
    {"name": "Valid Sudoku", "solutionPercent": 63.4,
        "difficulty": "Medium", "done": False},
    {"name": "Sudoku", "solutionPercent": 65.2,
        "difficulty": "Hard", "done": False}
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
            problems_solved = [
                item for item in problems_list if item.get("done") is True]
            qtd_problems_solved = len(problems_solved)

            return render_template('index.html', my_list=my_list, problems_list=problems_list, problems_solved=qtd_problems_solved)

    @app.route('/edit_problems_list', methods=['GET'])
    def edit_problems_list():
        return render_template('edit_problems_list.html', problems_list=problems_list)

    @app.route('/remove_item/<string:problem_name>', methods=['DELETE'])
    def remove_item(problem_name):
        global problems_list
        updated_items = [item for item in problems_list if item.get(
            "name") != problem_name]
        problems_list = updated_items

    @app.route('/add_problem', methods=['POST'])
    def add_problem():
        global problems_list

        name = request.form.get('nameInput')
        difficulty = request.form.get('difficultInput')
        problems_list.insert(0, {"name": name, "solutionPercent": 00.0,
                                 "difficulty": difficulty, "done": False})
        return redirect(url_for('edit_problems_list'))

    @app.route('/edit_single_problem/<string:name>', methods=['GET', 'POST'])
    def edit_single_problem(name=None):
        global problems_list

        if name and request.method == 'GET':
            selected_problem = [
                problem for problem in problems_list if problem["name"] == name][0]
            return render_template('edit_single_problem.html', selected_problem=selected_problem)
        elif name and request.method == 'POST':
            inputNameValue = request.form.get('editNameInput')
            inputDifficultyValue = request.form.get('editDifficultyInput')
            inputSolutionPercentValue = request.form.get(
                'editSolutionPercentInput')

            for problem in problems_list:
                if problem['name'] == name:
                    problem['name'] = inputNameValue
                    problem['difficulty'] = inputDifficultyValue
                    problem['solutionPercent'] = inputSolutionPercentValue
                    break  # já encontrou, pode sair do loop
            return redirect(url_for('index'))
        else:
            return redirect(url_for('index'))
    
    @app.route('/store', methods=['GET'])
    def store():
        return render_template('store_page.html')
