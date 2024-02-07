import flask

from . import types
from . import logic

crud = {
    types.User: ['CREATE', 'READ', 'UPDATE', 'DELETE'],
}

class Service(object):
    # Service layer
    def __init__(self):
        self.logic = logic.Logic()
        self.flask = flask.Flask(__name__)

        for Type, allowOperations in crud.items():
            methods = {{
                'CREATE': 'POST',
                'READ': 'GET',
                'UPDATE': 'POST',
                'DELETE': 'DELETE',
                }[o]:True for o in allowOperations}.keys()
            self.flask.add_url_rule(
                "/%s/<int:pkv>" % Type.__table__.name,
                methods=methods,
                endpoint='%s/pkv' % Type.__table__.name,
                view_func=lambda pkv : self.handleCRUD(Type, pkv, allowOperations),
            )
            self.flask.add_url_rule(
                "/%s" % Type.__table__.name,
                methods=methods,
                endpoint=Type.__table__.name,
                view_func=lambda : self.handleCRUD(Type, None, allowOperations),
            )

        @self.flask.route("/")
        def hello():
            return "You have reached Jeremy's API Server"

        @self.flask.route("/findUsersByName", methods=['GET'])
        def findUsersByName():
            if 'name' not in flask.request.args:
                flask.abort(400)
            return flask.jsonify([{c.name:getattr(record, c.name) for c in record.__table__.columns} for record in self.logic.findUsersByName(flask.request.args['name'])])

    def run(self):
        return self.flask.run()

    def finalize(self):
        self.logic.finalize()

    # Generic CRUD
    def get(self, type, pkVal):
        record = self.logic.get(type, pkVal)
        if record is None:
            flask.abort(404)
        return flask.jsonify({c.name:getattr(record, c.name) for c in record.__table__.columns})

    def post(self, type, pkVal=None):
        for key, val in flask.request.form.items():
            if key not in type.__table__.columns:
                flask.abort(400)

        print(pkVal)
        if not pkVal:
            record = type(**flask.request.form)
        else:
            record = self.logic.get(type, pkVal)
            if record is None:
                flask.abort(404)
            for key, val in flask.request.form.items():
                setattr(record, key, val)

        return self.logic.createOrUpdate(record)

    def delete(self, type, pkVal):
        record = self.logic.get(type, pkVal)
        if record is None:
            flask.abort(404)
        return self.logic.delete(type, pkVal)

    def handleCRUD(
        self,
        type,
        pkVal=None,
        operationsAllowed=None,
    ):
        if flask.request.method == 'POST' and pkVal is None and 'CREATE' in operationsAllowed:
            self.post(type)
            resp = flask.jsonify(success=True)
            resp.status_code = 201
            return resp
        elif flask.request.method == 'GET' and pkVal is not None and 'READ' in operationsAllowed:
            return self.get(type, pkVal)
        elif flask.request.method == 'POST' and pkVal is not None and 'UPDATE' in operationsAllowed:
            self.post(type, pkVal)
            resp = flask.jsonify(success=True)
            resp.status_code = 204
            return resp
        elif flask.request.method == 'DELETE' and pkVal is not None and 'DELETE' in operationsAllowed:
            self.delete(type, pkVal)
            resp = flask.jsonify(success=True)
            resp.status_code = 204
            return resp
        else:
            resp = flask.jsonify(success=False)
            resp.status_code = 405
            return resp
