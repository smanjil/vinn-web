
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import IncomingLog, Users, Services, Comment
app = Flask(__name__)

# set the secret key.  keep this really secret: required to use session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route('/')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = Users.select().where(Users.username == username,
                                    Users.password == password)[0]
    except:
        flash('Username/Password does not match')
        return redirect(url_for('index'))
    else:
        session['logged_in'] = True
        session['org_id'] = user.org_id
        session['username'] = username
    return redirect(url_for('get_report', org_id=user.org_id))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


@app.route('/pullreport', methods=['GET', 'POST'])
def get_report():
    org_id = request.args['org_id']
    session_org_id = session.get('org_id', None)

    if session.get('logged_in') is not None and str(session_org_id) == org_id:
        print 'Organization id: ', org_id
        service = Services.select().where(Services.org_id == org_id)
        print 'Services rows: ', len(service)
        services = [[items.service_type.name, items.extension] for items in service]

        i = IncomingLog.select().where(IncomingLog.org == org_id)
        org_name = i[0].org.name

        if request.method == 'POST':
            if 'commentform' in request.form:
                log_id = request.form['log_id']
                comment = request.form['comment']
                Comment.create(log_id=log_id, comment=comment)
            if 'statusform' in request.form:
                log_id = request.form['log_id']
                status = request.form['status']
                i = IncomingLog.update(status=status).where(IncomingLog.id == log_id)
                i.execute()

        if 'service' in request.args and 'extension' in request.args:
            service_name = str(request.args['service'])
            extension = str(request.args['extension'])

            reports = []
            try:
                for i in IncomingLog.select().where(IncomingLog.org == org_id, IncomingLog.service == service_name, IncomingLog.extension == extension).order_by(IncomingLog.id.desc()):
                    item = []
                    item.append(i.incoming_number)
                    item.append(i.call_start_time)
                    item.append(i.generalized_data_incoming.data)
                    item.append(i.id)
                    item.append(i.comment_set)
                    item.append(i.status)
                    org_name = i.org.name
                    reports.append(item)
                return render_template(
                    'report.html',
                    title='Report',
                    output=reports,
                    org_name=org_name,
                    to=extension,
                    org_id=org_id,
                    services=services,
                    service_name=service_name
                )
            except:
                flash('No reports available for this service!')
                return redirect(url_for('get_report', org_id=org_id))
        else:
            return render_template(
                'report.html',
                title='Report',
                org_id=org_id,
                services=services,
                org_name=org_name
            )
    else:
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
