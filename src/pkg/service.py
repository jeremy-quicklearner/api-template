import flask

from . import types
from . import logic

crud = {
    types.Person: ['CREATE', 'READ', 'UPDATE', 'DELETE'],
    types.Book: ['CREATE', 'READ', 'UPDATE', 'DELETE'],
    types.PersonOwnsBook: ['CREATE', 'DELETE'],
}

flaskApp = flask.Flask(__name__)

for Type, allowOperations in crud.items():
    methods = {{
        'CREATE': 'POST',
        'READ': 'GET',
        'UPDATE': 'POST',
        'DELETE': 'DELETE',
        }[o]:True for o in allowOperations}.keys()
    flaskApp.add_url_rule(
        "/%s/<int:pkv>" % Type.__table__.name,
        methods=methods,
        endpoint='%s/pkv' % Type.__table__.name,
        view_func=lambda pkv, T=Type : handleCRUD(T, pkv, allowOperations),
    )
    flaskApp.add_url_rule(
        "/%s" % Type.__table__.name,
        methods=methods,
        endpoint=Type.__table__.name,
        view_func=lambda T=Type : handleCRUD(T, None, allowOperations),
    )

@flaskApp.route("/")
def hello():
    return "You have reached Jeremy's API Server"

@flaskApp.route("/findBooksByPersonName", methods=["GET"])
def findBooksByPersonName():
    if 'name' not in flask.request.args:
        flask.abort(400)
    return flask.jsonify([
        types.structify(record) for record in logic.findBooksByPersonName(
            flask.request.args['name']
        )
    ])

def run():
    return flaskApp.run()

def finalize():
    logic.finalize()

# Generic CRUD
def get(type, pkVal):
    record = logic.get(type, pkVal)
    if record is None:
        flask.abort(404)
    return flask.jsonify({c.name:getattr(record, c.name) for c in record.__table__.columns})

def post(type, pkVal=None):
    for key, val in flask.request.form.items():
        if key not in type.__table__.columns:
            flask.abort(400, 'Bad parameter name <%s>. Accepted names are %s' % (key, [c.name for c in type.__table__.columns]))

    if not pkVal:
        record = type(**flask.request.form)
    else:
        record = logic.get(type, pkVal)
        if record is None:
            flask.abort(404)
        for key, val in flask.request.form.items():
            setattr(record, key, val)

    return logic.createOrUpdate(record)

def delete(type, pkVal):
    record = logic.get(type, pkVal)
    if record is None:
        flask.abort(404)
    return logic.delete(type, pkVal)

def handleCRUD(
    type,
    pkVal=None,
    operationsAllowed=None,
):
    if flask.request.method == 'POST' and pkVal is None and 'CREATE' in operationsAllowed:
        id = post(type)
        resp = flask.jsonify(id=id, success=True)
        resp.status_code = 201
        return resp
    elif flask.request.method == 'GET' and pkVal is not None and 'READ' in operationsAllowed:
        return get(type, pkVal)
    elif flask.request.method == 'POST' and pkVal is not None and 'UPDATE' in operationsAllowed:
        id = post(type, pkVal)
        resp = flask.jsonify(id=id, success=True)
        resp.status_code = 204
        return resp
    elif flask.request.method == 'DELETE' and pkVal is not None and 'DELETE' in operationsAllowed:
        delete(type, pkVal)
        resp = flask.jsonify(success=True)
        resp.status_code = 204
        return resp
    else:
        resp = flask.jsonify(success=False)
        resp.status_code = 405
        return resp
