import os
from flask import Flask, flash, make_response, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from werkzeug.serving import run_simple
from tree import *

#curpath = os.path.dirname(__file__).replace('\\','/')
UPLOAD_FOLDER = 'uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['SERVER_NAME'] = '0.0.0.0'
app.static_folder = 'static'
app.template_folder = 'templates'
app.secret_key = 'key'

n = None
t = None
pf1 = None
pf2 = None

def allowed_file(filename, ext): return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() == ext

@app.route('/')
def index():
    global n, t
    base, f1, f2, f1m, f2m = '/base.html', '/f1.html', '/f2.html', '/pf1.html','/pf2.html'
    return render_template('index.html', base=base, f1=f1, f2=f2, t=t, n=n, f1m=f1m, f2m=f2m)

@app.route('/base.html')
def base():
    return render_template('/base.html', n = n)
@app.route('/f1.html')
def f1():
    return render_template('/f1.html', n = n)
@app.route('/f2.html')
def f2():
    return render_template('/f2.html', n = n)
@app.route('/pf1.html')
def f1m():
    return render_template('/pf1.html', pf1 = pf1)
@app.route('/pf2.html')
def f2m():
    return render_template('/pf2.html', pf2 = pf2)

@app.route('/<which>')
def chart(which): return render_template('/lchart.html', pf1 = pf1, pf2 = pf2, which = which)

@app.route('/diagram')
def graph(): return render_template('/graph.html', n = n)

@app.route('/', methods=['GET', 'POST'])
def upload():
    global n, t, pf1, pf2
    file = request.files['treefile']
    if file and allowed_file(file.filename, 'xml'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        n = Tree(UPLOAD_FOLDER + filename)
        if n.viable: n.name = filename
        else: n = None
        t, pf1, pf2 = None, None, None
    elif file and allowed_file(file.filename, 'txt'):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        if n: n.updateTypes(UPLOAD_FOLDER + filename)
        if n.nudf < len(n.leaves):
            t, pf1, pf2 = filename, None, None
    return index()

@app.route('/download_<table>')
def download(table):
    global n, t, pf1, pf2
    tsv = n.TSV(table)
    response = make_response(tsv)
    response.headers["Content-Disposition"] = "attachment; filename=%s_%s.tsv" % (n.tree.keys()[0], table)
    return response


@app.route('/migrations', methods=['POST'])
def clustering():
    global n, t, pf1, pf2
    if n and t:
        if request.form.get('range'):           
            start = int(request.form.get('start'))
            stop = int(request.form.get('stop'))
            step = int(request.form.get('step'))
            mutRate = int(request.form.get('mutRate1'))
            effective = True if request.form.get('effective') else False
            pf1 = n.migrationProbs(xrange(start, stop + 1, step), mutRate, 1, effective)
            pf2 = n.migrationProbs(xrange(start, stop + 1, step), mutRate, 2, effective)
        elif request.form.get('comma'):
            dates = [int(x) for x in request.form.get('dates').split(',')]
            mutRate = int(request.form.get('mutRate2'))
            effective = True if request.form.get('effective') else False
            pf1 = n.migrationProbs(dates, mutRate, 1, effective)
            pf2 = n.migrationProbs(dates, mutRate, 2, effective)
    return redirect('/')

if __name__=='__main__':
    port = int(os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port)
