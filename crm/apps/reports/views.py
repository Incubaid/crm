from flask import render_template

from crm import app


@app.route('/reports', methods=["GET"])
def reports():
    return render_template('reports/reports.html'), 200

