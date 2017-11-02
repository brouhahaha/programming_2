
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__)



def make_dict (filename):
    with open (filename, 'r', encoding = 'utf-8') as file:
        content = file.read()
        d = {}
        langs_and_codes = content.split('\n')
        for lang_and_code in langs_and_codes:
            language = lang_and_code.split(',')[0]
            code = lang_and_code.split(',')[1]
            d [language] = code
    return d

langcodes = make_dict("lang_codes.csv")

@app.route('/')
def index():
    return render_template('htmllangs.html', langcodes=langcodes)



@app.route('/langs/<q>')
def first_letts(q):
    found_languages = {}
    for d in langcodes:
        if langcodes[d].startswith(q)== True:
            found_languages [d] = langcodes [d]
    return render_template('htmllangs.html', langcodes=found_languages)

@app.route('/form/')
def form():
    return render_template('formhtml.html')

@app.route ('/lang/<r>')
def func(q):
    dict((c, l) for l, c in langcodes.iteritems())
    langs = []
    
@app.route('/search')
def search():
    return redirect (url_for('/lang/'+request.args['lang']))


if __name__ == '__main__':
    app.run(debug=True)





