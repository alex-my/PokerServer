# coding:utf8


def reloads():
    import app.auth.action.account
    import app.auth.action.send

    import app.auth.service.account
    import app.auth.service.forward

    reload(app.auth.action.account)
    reload(app.auth.action.send)

    reload(app.auth.service.account)
    reload(app.auth.service.forward)
