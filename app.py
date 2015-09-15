from flask import Flask, render_template, request, redirect, url_for
from wakeonlan import wol
import ping, os
from tinydb import TinyDB, where
from collections import OrderedDict

app = Flask(__name__)

DB_FILE = '/tmp/db.json'

def menu():
    menu = OrderedDict()
    menu['index'] = { 'name' : 'Home', 'url' : url_for('index') }
    menu['add'] = { 'name' : 'Add', 'url' : url_for('add') }
    return menu

def render_extended(template, **kwargs):
    kwargs['menu'] = menu()
    kwargs['endpoint'] = request.endpoint
    return render_template(template, **kwargs)

def getdb():
    return TinyDB(DB_FILE)

@app.route('/wakehost/<string:mac>')
def wakehost(mac):
    wol.send_magic_packet(mac)
    return redirect(url_for('index'))

@app.route('/delete/<int:host_id>')
def delete(host_id):
    db = getdb()
    db.remove(eids=[host_id])
    return redirect(url_for('index'))

@app.route('/edit', defaults = { 'host_id' : None }, methods = [ 'GET', 'POST' ])
@app.route('/edit/<int:host_id>', methods = [ 'GET', 'POST' ])
def add(host_id = None):
    db = getdb()
    data = {}
    if request.method == 'POST':
        for item in request.form:
            data[item] = request.form[item]

        if host_id:
            db.update(data, eids=[host_id])
        else:
            host_id = db.insert(data)
            return redirect(url_for('add', host_id = host_id))
    else:
        if host_id:
            data = db.get(eid=host_id)
    return render_extended('add.html', data = data)

@app.route('/')
def index():
    db = getdb()
    data = db.all()
    print data
    return render_extended('index.html', data = data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
