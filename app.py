from flask import Flask
from flask import render_template, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('index.html', name=False, age=16)

@app.route("/hello")
def hello():
    return render_template('index.html', name="笹原", age=16)

@app.route("/age", methods=['POST', 'GET'])
def age():
    age = request.form['age']
    return render_template('index.html', name=False, age=age)

app.run()