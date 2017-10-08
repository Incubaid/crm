from flask import request, jsonify
from werkzeug.exceptions import abort

from flask_graphql import GraphQLView

from crm import app


@app.route('/api', methods=["POST"])
def api():
    data = request.json
    query = data.get('query', None)
    if query:
        try:
            execresult = app.graphql_schema.execute(query)
            if execresult.errors:
                # TODO: in case of errors do we return
                return jsonify(error=execresult.errors)
            return jsonify(execresult.data)
        except Exception as ex:
            return jsonify(error=str(ex))
    abort(401)


app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=app.graphql_schema, graphiql=True))
