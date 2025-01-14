from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    # 全てのテーブルを作成
    connection = sqlite3.connect('result.db')
    cursor = connection.cursor()

    cursor.execute('''
    create table IF NOT exists score (
    `student_id` integer not null,
    `test_number_id` integer not null,
    `curriculum_id` integer not null,
    `point` integer not null,
    foreign key(student_id) references student(student_id)
    foreign key(test_number_id) references test_number(test_number_id)
    foreign key(curriculum_id) references curriculum(curriculum_id)
    Primary key(student_id, test_number_id, curriculum_id)
    );

    create table IF NOT exists student (
    `student_id` integer not null Primary key,
    `name` integer not null
    );

    create table IF NOT exists test_number (
    `test_number_id` integer not null Primary key,
    `name` integer not null
    );

    create table IF NOT exists curriculum (
    `curriculum_id` integer not null Primary key,
    `name` integer not null
    );
    ''')

    cursor.execute('select * from student')
    student_list = cursor.fetchall()
    connection.close()

    return render_template('index.html')


app.run()