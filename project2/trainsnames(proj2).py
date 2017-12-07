import sqlite3
from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
import json
import csv 

app = Flask(__name__)
conn = sqlite3.connect('data_trains.db', check_same_thread = False)
@app.route('/')
def index():
    return render_template('train.html')

@app.route('/thanks/')
def thanks():
    with open ('results_data.json', 'r') as f:
        content = f.read()
        final_data = json.loads(content)
    data = dict(request.args)
    final_data ['ages'].append(data['age'][0])
    final_data ['cities'].append(data['city'][0])
    final_data ['sex'].append(data['sex'][0])
    final_data ['freq'].append(data['freq_use'])
    i = len(final_data['ages'])
    final_data ['user'+str(i)] = data
    with open('results_data.json', "w", newline="") as file:
        file.write(json.dumps(final_data, ensure_ascii = False))
    keys = list(data.keys())
    vars_to_db = []
    for key in keys[4:len(keys)+1]:
        vars_to_db.append(data[key][0])
    str_vars_to_db = ';'.join(vars_to_db)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, sex TEXT, age INTEGER, city TEXT, freq TEXT, vars VARCHAR)")
    c.execute("INSERT INTO users (id, sex, age, city, freq, vars) VALUES (?, ?, ?, ?, ?, ?)", [i,data['sex'][0],data['age'][0], data['city'][0], data['freq_use'][0], str_vars_to_db])
    conn.commit()
    conn.close()
    return render_template ('thanks.html')

def analyse(key_name):
    with open ('results_data.json', 'r') as f:
        content = f.read()
        python_content = json.loads(content)
    contents = python_content[key_name]
    counted = {}
    for token in contents:
        if list(counted.keys()).count(token)==0:
            counted[token]=contents.count(token)
    return counted

def analyse_var(var):
    with open ('results_data.json', 'r') as f:
        content = f.read()
        python_content = json.loads(content)
        var_count = 0
    for i in range(1, len(python_content['ages'])+1):
        if list(python_content['user'+str(i)].keys()).count(var)!= 0 :
            var_count+=1
    return var_count
        

@app.route('/stats/')
def statistcs():
    sexs = analyse('sex')
    cities = analyse('cities')
    ages = analyse ('ages')
    variants = {}
    trains = ['Поезд', 'Электричка', 'Собака', 'Липа', 'Электрос', 'Электрон', 'Пригородка','Эл(ь)ка']
    for z in range(1,9):
        variants[trains[z-1]]=analyse_var('var'+str(z))
    return render_template('statistics.html', sexs = sexs, cities = cities, ages=ages, variants = variants)

@app.route('/json/')
def json_on_page():
    with open('results_data.json', "r") as file:
       content = file.read()
    return '<a href="http://127.0.0.1:5000/">Главная страница</a></br><a href="http://127.0.0.1:5000/stats/">Статистика</a></br><a href="http://127.0.0.1:5000/json/">json</a></br>  <a href="http://127.0.0.1:5000/search/">Поиск</a></br>'+content

@app.route('/search/')
def search():
    return render_template('searching.html')

@app.route('/results/')
def results():
    total_entries = analyse_var(request.args['var'])
    cities = searching(request.args['var'], 'city')
    ages = searching(request.args['var'], 'age')
    sex = searching(request.args['var'], 'sex')
    fnum = sex.count('f')
    mnum = sex.count('m')
    return render_template ('searesults.html', total = total_entries, cities = cities, ages = ages, fnum = fnum, mnum = mnum)
    

def searching(variant, key):
    with open ('results_data.json', 'r') as f:
        content = f.read()
        python_content = json.loads(content)
    data = []
    for i in range(1, len(python_content['ages'])+1):
        if list(python_content['user'+str(i)].keys()).count(variant)!= 0 :
            data.append(python_content['user'+str(i)][key][0])
    return data

                       
if __name__ == '__main__':
    app.run(debug=True)
