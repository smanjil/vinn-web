
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import IncomingLog, Users, Services
app = Flask(__name__)

# set the secret key.  keep this really secret: required to use session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/modules')
def organization_modules():
    org_id = request.args['org_id']
    session_org_id = session.get('org_id', None)
    if session.get('logged_in') is not None and str(session_org_id) == org_id:
        print 'Organization id: ', org_id
        service = Services.select().where(Services.org_id == org_id)
        print 'Services rows: ', len(service)
        services = [[items.service_type.name, items.extension] for items in service]
        return render_template('services.html',
                        services=services,
                        org_id=org_id)
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = Users.select().where(Users.username == username,
                                    Users.password == password)[0]
    except:
        raise RuntimeError('User does not exist!')
    else:
        session['logged_in'] = True
        session['org_id'] = user.org_id
    return redirect(url_for('organization_modules', org_id=user.org_id))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/pullreport', methods=['GET'])
def get_report():
    org_id = int(request.args['org_id'])
    extension = str(request.args['extension'])
    session_org_id = session.get('org_id', None)
    if session.get('logged_in') is not None and session_org_id == org_id:
        service_name = str(request.args['service'])
        reports = []
        try:
            for i in IncomingLog.select().where(IncomingLog.org == org_id, IncomingLog.service == service_name, IncomingLog.extension == extension):
                item = []
                item.append(i.incoming_number)
                item.append(i.call_start_time)
                item.append(i.generalized_data_incoming_id.data)
                org_name = i.org.name
                reports.append(item)
            return render_template(
                'test_report.html',
                title='Report',
                output=reports,
                org_name=org_name,
                to=extension,
                service_name=service_name
            )
        except:
            flash('No reports available for this service!')
            return redirect(url_for('organization_modules', org_id=org_id))
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
