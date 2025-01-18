from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def select_test(student_id, test_id):
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    print(student_id)
    print(test_id)
    cursor.execute('select * from score where test_id = ? and student_id = ?',(test_id, student_id))
    # select * from score where test_id = 2 and student_id = 1
    select_test = cursor.fetchone()
    print(select_test)
    connection.close()
    return select_test

def get_db():
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    return cursor

def get_test_number(id):
    if id == "":
        connection = sqlite3.connect('result.db')
        cursor = connection.cursor()
        cursor.execute('select * from test_number ')
        tests = cursor.fetchall()
        connection.close()
    else:
        connection = sqlite3.connect('result.db')
        cursor = connection.cursor()
        cursor.execute('select t.test_id, t.name from score as s join test_number as t on s.test_id = t.test_id where s.student_id = ? order by t.test_id asc',(id,))
        tests = cursor.fetchall()  #特定の生徒のテストの回ごとの点数を取得
        connection.close()
    connection.close()
    return tests

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
    `student_id` integer not null Primary key autoincrement,
    `name` text not null
    );
    ''')
    
    cursor.execute('''
    create table IF NOT exists test_number (
    `test_id` integer not null Primary key autoincrement,
    `name` text not null
    );
    ''')

    cursor.execute('select * from student')
    student_list = cursor.fetchall()
    connection.close()

    return render_template('index.html', student_list = student_list)

# 生徒の成績を確認(レーダーチャートページへ遷移)
@app.route("/show/<id>")
def show_list(id):
    # student_id = int(request.form.get('student_id'))

    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from student where student_id = ?',(id,))
    student_name = cursor.fetchone()  #生徒名を取得

    cursor.execute('select student_id, AVG(html_score), AVG(css_score), AVG(js_score), AVG(python_score), AVG(java_score) from score group by (?)',(id,))
    avg_score = cursor.fetchone()  #選択した生徒の全教科平均点を取得
    # print(avg_score)

    cursor.execute('select t.name, s.test_id, s.html_score, s.css_score, s.js_score, s.python_score, s.java_score from score as s join test_number as t on s.test_id = t.test_id where s.student_id = ? order by t.test_id asc',(id,))
    tests_score = cursor.fetchall()  #選択した生徒のテストの回ごとの点数を取得

    connection.close()
    return render_template('show_score.html', student_name = student_name, avg_score = avg_score, tests_score = tests_score)

# テストの回を一覧表示
@app.route("/create_test")
def create_test_number():
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from test_number')
    tests = cursor.fetchall() 
    connection.close()

    return render_template('test_number_edit.html', tests = tests)


# テストの回追加
@app.route("/add_test", methods=["POST"])
def add_test_number():
    test = request.form.get('test_name')

    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('''
    insert into test_number (name) values (?)''',(test,))
    connection.commit()
    connection.close()

    return redirect('/create_test')

# テストの回編集
@app.route("/edit_test/<id>", methods=["POST"])
def edit_test_number(id):
    test = request.form.get('modal_name')

    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('''
    update test_number set name = ? where test_id = ?''',(test, id,))
    connection.commit()
    connection.close()

    return redirect('/create_test')

# テストの回削除
@app.route("/delete_test/<id>")
def delete_test_number(id):

    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('''
    delete from test_number where test_id = (?)''',(id,))
    connection.commit()
    connection.close()

    return redirect('/create_test')


# 過去の過去のテスト一覧を表示
@app.route("/select_test/<id>")
def select_tests(id):
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from student where student_id = ?',(id,))
    student_name = cursor.fetchone()  #生徒名を取得
    connection.close()
    tests = get_test_number(id)  #選択した生徒のテストの一覧を取得
    id = id

    return render_template('select_score.html', tests = tests, student_name = student_name, id = id)


# 成績入力画面に遷移
@app.route("/regist/<id>")
def score_register(id):

    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from student where student_id = ?',(id,))
    student_name = cursor.fetchone()  #生徒名を取得
    connection.close()

    tests = get_test_number(id) #idの値がidの生徒のテスト回一覧を取得
    id = id
    
    return render_template('score_regist.html', student_name = student_name, tests = tests, id = id)


# 成績入力確定ボタン
@app.route("/create_score/<id>", methods=['POST', 'GET'])
def regist_score(id):
    student_id = id
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


# 成績の編集画面へ遷移
@app.route("/editer/<student_id>/<test_id>")
def score_editer(student_id, test_id):
    student_id = student_id
    test_id = test_id
    # print(student_id)
    # print(test_id)

    selectTest = select_test(student_id, test_id)  #特定のidの生徒の特定のidのテストを取得
    
    # 取得したテストの名前を取得
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from test_number where test_id = ?',(test_id,))
    test_name = cursor.fetchone()  #test_idのテストを取得
    connection.close()

    #生徒名を取得
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()
    cursor.execute('select * from student where student_id = ?',(student_id,))
    student_name = cursor.fetchone()  #生徒名を取得
    connection.close()
    
    return render_template('score_editer.html', select_test = selectTest, test_name = test_name, student_name = student_name, id = student_id)

app.run()