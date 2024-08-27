import routes


def register_blueprints(app):
    app.register_blueprint(routes.auth)
    app.register_blueprint(routes.users)
    app.register_blueprint(routes.service)
    app.register_blueprint(routes.appointment)
    app.register_blueprint(routes.invoice)
    app.register_blueprint(routes.employees)
