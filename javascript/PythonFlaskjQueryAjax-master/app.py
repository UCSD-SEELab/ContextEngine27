import os
from flask import Flask,render_template, request,json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to Python Flask!'

@app.route('/accessor')
def accessor():
    return render_template('accessor.html')

@app.route('/accessorOutput', methods=['POST'])
def accessorOutput():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

if __name__=="__main__":
    app.run()

# def run_Tesla(arg1, arg2):
#     os.system('Tesla.py' + arg1 + arg2)
