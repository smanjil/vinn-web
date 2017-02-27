
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
from models import IncomingLog, Users
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    print username, password
    try:
        user = Users.select().where(Users.username == username, Users.password == password)[0]
    except:
        raise RuntimeError('User does not exist!')
    else:
        print user.org_id
    return redirect('/nuwakotreport')


@app.route('/nuwakotreport')
def testreport():
    reports = []
    for i in IncomingLog.select().where(IncomingLog.extension == 3001):
        item = []
        item.append(i.incoming_number)
        item.append(i.call_start_time)
        item.append(i.generalized_data_incoming_id.data)
        org_name = i.org.name
        to = i.extension
        reports.append(item)
#    print '\n\n', reports, '\n\n'
    return render_template(
        'test_report.html',
        title='Report',
        output=reports,
        org_name=org_name,
        to=to
    )

if __name__ == "__main__":
    app.run(debug=True)
