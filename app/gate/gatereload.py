# coding:utf8


def reloads():
    import app.gate.service.account
    import app.gate.service.forward
    import app.gate.service.login
    import app.gate.service.room

    import app.gate.action.login
    import app.gate.action.send
    import app.gate.action.room

    reload(app.gate.service.account)
    reload(app.gate.service.forward)
    reload(app.gate.service.login)
    reload(app.gate.service.room)

    reload(app.gate.action.login)
    reload(app.gate.action.send)
    reload(app.gate.action.room)

