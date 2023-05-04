from flask import Flask, render_template, request, redirect, url_for
import csv
import datetime
import os.path

app = Flask(__name__)

# [ Tests ]
import tests as base


# [ Setup CSV ]
if (os.path.exists(f'answers_{datetime.date.today()}.csv')) == False:
    with open(f'answers_{datetime.date.today()}.csv', 'w', newline='') as csvfile:
        fieldnames = ['Test_ID', 'User_Name', 'Score', 'Answers']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

# [ Homepage ]
@app.route('/')
def index():
    return render_template('index.html', tests=base.tests)


@app.route('/back')
def back_to_index():
    return render_template('index.html', tests=base.tests)


# [ Test page ]
@app.route('/test/<int:test_id>')
def test(test_id):
    test = next((t for t in base.tests if t["id"] == test_id), None)
    if not test:
        return redirect(url_for('index'))
    return render_template('test.html', test=test)


# [ Submit page ]
@app.route('/test/<int:test_id>/submit', methods=['POST'])
def submit(test_id):
    test = next((t for t in base.tests if t["id"] == test_id), None)
    if not test:
        return redirect(url_for('index'))
    score = 0
    answers = []
    for question in test['questions']:
        answer = int(request.form.get(str(question['id'])))
        answers.append(answer)
        if answer == question['answer']:
            score += 1
    name = request.form['user']

    with open(f'answers_{datetime.date.today()}.csv', 'a', newline='\n') as csvfile:
        fieldnames = ['Test_ID', 'User_Name', 'Score', 'Answers']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writerow({'Test_ID': test_id, 'User_Name': name, 'Score': score, 'Answers': answers})

    print("Test ID = {}; User name = {}; Score = {}; Answers = {}".format(test_id, name, score, answers))
    return render_template('submit.html', score=score, total=len(test['questions']))


app.jinja_env.globals.update(enumerate=enumerate)


@app.route('/debug')
def debug():
    with open(f'answers_{datetime.date.today()}.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        debug_data = ''
        for row in reader:
            debug_data += '; '.join(row) + '\n'
        return str(debug_data)


if __name__ == '__main__':
    app.run(debug=True)