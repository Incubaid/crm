from flask import request, jsonify
from crm import app
from crm.schema import schema


@app.route('/api', methods=["POST"])
def api():
    data = request.json
    query = data.get('query', None)
    if query:
        try:
            execresult = schema.execute(query)
            if execresult.errors:
                # TODO: in case of errors do we return
                return jsonify(error=execresult.errors)
            return jsonify(execresult.data)
        except Exception as ex:
            return jsonify(error=str(ex))
    abort(401)
