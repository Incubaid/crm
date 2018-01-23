from flask_admin import BaseView, Admin


from crm import app


class ReportsAdminView(BaseView):
    def __init__(self, *args, **kwargs):
        self._default_view = True
        super(ReportsAdminView, self).__init__(*args, **kwargs)
        self.admin = app.admin


@app.route('/reports', methods=["GET"])
def reports():
    return ReportsAdminView().render('reports/reports.html'), 200
