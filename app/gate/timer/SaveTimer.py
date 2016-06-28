# coding:utf8
from app.gate.timer.TimeBase import ITimer
from app.gate.core.UserManager import UserManager
from app.util.common import func


class SaveTimer(ITimer):

    def do(self):
        interval = 30 * 60
        self.start(interval)
        func.log_info('[gate] SaveTimer check do, next: {}'.format(interval))
        all_users = UserManager().get_all_users()
        for account_id, user in all_users.iteritems():
            try:
                user.user_save()
            except Exception as e:
                func.log_error('[gate] SaveTimer account_id: {}, failed: {}'.format(
                    account_id, e.message
                ))
