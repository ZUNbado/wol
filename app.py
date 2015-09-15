from flask import Flask, render_template, request, redirect, url_for
from collections import OrderedDict
from menu import MenuClass
from utils import get_status, wakehost, getdb

app = Flask(__name__)
Menu = MenuClass()

@app.route('/wakehost/<int:host_id>')
def wakeup(host_id):
    db = getdb()
    host = db.get(eid = host_id)
    wakehost(host['inputMAC'])
    return redirect(url_for('index'))

@app.route('/delete/<int:host_id>')
def delete(host_id):
    db = getdb()
    db.remove(eids=[host_id])
    return redirect(url_for('index'))

@app.route('/')
@Menu.add(name = 'Home', url = '/')
def index():
    db = getdb()
    data = db.all()
    return Menu.render('index.html', data = data)

@app.route('/edit', defaults = { 'host_id' : None }, methods = [ 'GET', 'POST' ])
@app.route('/edit/<int:host_id>', methods = [ 'GET', 'POST' ])
@Menu.add(name = 'Add', url = '/edit')
def add(host_id = None):
    db = getdb()
    data = {}
    if request.method == 'POST':
        for item in request.form:
            if item == 'submit':
                action = request.form[item]
            else:
                data[item] = request.form[item]
        data['status'] = get_status(data['inputIP'])
        if host_id:
            if action == 'delete':
                db.remove(eids = [ host_id ])
                return redirect(url_for('index'))
            else:
                db.update(data, eids=[host_id])
        else:
            host_id = db.insert(data)
        
        if action == 'save':
            return redirect(url_for('add', host_id = host_id))
        else:
            return redirect(url_for('index'))
    else:
        if host_id:
            data = db.get(eid=host_id)
    return Menu.render('add.html', data = data, host_id = host_id)

@app.route('/update_status', defaults = { 'host_id' : None })
@app.route('/update_status/<int:host_id>')
@Menu.add(name = 'Update', url = '/update_status', order = 3)
def update_status(host_id = None):
    db = getdb()
    if host_id:
        hosts = [ db.get(eid = host_id) ]
    else:
        hosts = db.all()
    for host in hosts:
        status = get_status(host['inputIP'])
        db.update({ 'status' : status}, eids = [ host.eid ])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
