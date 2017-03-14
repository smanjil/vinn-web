
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import IncomingLog, User, Service, Comment
from sqlalchemy import desc
from config import app, db

@app.route('/')
def index():
    return render_template('main.html',
                           title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    try:
        user = User.query.filter(User.username == username,
                                    User.password == password)[0]
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
        service = Service.query.filter(Service.org_id == org_id)
        services = [[items.service_types.name, items.extension] for items in service]

        i = IncomingLog.query.filter(IncomingLog.org_id == org_id)
        org_name = i[0].org_ids.name

        if request.method == 'POST':
            if 'commentform' in request.form:
                log_id = request.form['log_id']
                comment = request.form['comment']
                cmnt = Comment(log_id=log_id, comment=comment)
                db.session.add(cmnt)
                db.session.commit()
            if 'status' in request.form:
                log_id = request.form['log_id']
                status = request.form['status']
                i = IncomingLog.query.filter(IncomingLog.id == log_id)
                i[0].status = status

        if 'service' in request.args and 'extension' in request.args:
            service_name = str(request.args['service'])
            extension = str(request.args['extension'])
            reports = []
            try:
                for i in IncomingLog.query.filter(IncomingLog.org_id == org_id, IncomingLog.service == service_name, IncomingLog.extension == extension).order_by(desc(IncomingLog.id)):
                    item = []
                    item.append(i.incoming_number)
                    item.append(i.call_start_time)
                    item.append(i.generalized_data_incomings.data)
                    item.append(i.id)
                    item.append(i.comments)
                    item.append(i.status)
                    org_name = i.org_ids.name
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
    app.run(debug=True, host='0.0.0.0')
