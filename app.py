
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import json
from models import IncomingLog
app = Flask(__name__)


@app.route('/reportraw')
def testreport():
    reports = []
    for i in IncomingLog.select().where(IncomingLog.extension==3001):
        item = []
        item.append(i.incoming_number)
        item.append(i.call_start_time)
        item.append(i.generalized_data_incoming_id.data)
        org_name = i.org.name
        to = i.extension
        reports.append(item)
    print '\n\n', reports, '\n\n'
    return render_template(
        'test_report.html',
        title='Report',
        output=reports,
        org_name=org_name,
        to=to
    )


@app.route('/')
def index():
    return render_template(
        'report.html',
        title='Report'
    )


@app.route('/report', methods=['GET'])
def get_report():
    output = {
        'vboard': {
            'vboard1': False,
            'vboard2': True
        },
        'vsurvey': {
            'status': True,
            'question1': 'file1',
            'dtmf': '1',
            'question2': 'file2'
        }
    }
    return json.dumps(output)

if __name__ == "__main__":
    app.run(debug=True)
