from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def select_test(student_id, test_id):
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()

    cursor.execute('select * from score where test_id = test_id and student_id = student_id')
    select_test = cursor.fetchone()
    connection.close()
    return select_test

def get_db():
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    return cursor

@app.route("/")
def indexAccess():
    
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()

    cursor.execute('''
    create table IF NOT exists score (
    `student_id` integer not null,
    `test_id` integer not null,
    `html_score` integer not null default 0 CHECK(html_score >= 0),
    `css_score` integer not null default 0 CHECK(css_score >= 0),
    `js_score` integer not null default 0 CHECK(js_score >= 0),
    `python_score` integer not null default 0 CHECK(python_score >= 0),
    `java_score` integer not null default 0 CHECK(java_score >= 0),
    foreign key(student_id) references student(student_id)
    foreign key(test_id) references test_number(test_id)
    Primary key(student_id, test_id)
    );
    ''')
    
    cursor.execute('''
    create table IF NOT exists student (
    `student_id` integer not null Primary key,
    `name` text not null
    );
    ''')
    
    cursor.execute('''
    create table IF NOT exists test_number (
    `test_id` integer not null Primary key,
    `name` text not null
    );
    ''')

    cursor.execute('select * from student')
    student_list = cursor.fetchall()
    connection.close()

    return render_template('index.html', student_list = student_list)

@app.route("/show")
def show_list():
    
# 成績入力画面に遷移時実行
@app.route("/regist")
def score_register():
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from test_number order by test_id asc')
    tests = cursor.fetchall()
    connection.close()

    return render_template('score_regist.html', tests = tests)

# 成績入力確定後に実行
@app.route("/create_score", methods=['POST', 'GET'])
def regist_score():
    student_id = int(request.form.get('student_id'))
    test_id = int(request.form.get('test_id'))
    html = int(request.form.get('html_score'))
    css = int(request.form.get('css_score'))
    js = int(request.form.get('js_score'))
    py = int(request.form.get('python_score'))
    ja = int(request.form.get('java_score'))
    
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('''
    insert into score (student_id, test_id, html_score,
    css_score, js_score, python_score, java_score) values
    (?, ?, ?, ?, ?, ?, ?)''',(student_id, test_id, html, css, js, py, ja))
    connection.commit()
    connection.close()
    
    return redirect('/')

@app.route("/editer")
def score_editer():
    student_id = int(request.form.get('student_id'))
    test_id = int(request.form.get('test_id'))

    selectTest = select_test(student_id, test_id)
    
    # 取得したテストの名前を取得
    cor = get_db()
    cor.execute('select * from test_number where test_id = test_id')
    test_name = cor.fetchone()
    
    return render_template('score_editer.html', select_test = selectTest, test_name = test_name)
    


app.run()