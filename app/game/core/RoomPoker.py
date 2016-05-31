# coding:utf8
from app.game.core.Room import Room
from app.game.action import send
from app.util.defines import status
from app.util.common import func


class RoomPoker(Room):

    def __init__(self):
        super(RoomPoker, self).__init__()

    def dispatch_all_card(self):
        self.random_cards()
        self.room_player_status(status.PLAYER_STATUS_NORMAL)
        execute_account_id = self.execute_account_id
        func.log_info('[game] RoomPoker dispatch_all_card room_account_id_list: {}'.format(self.room_account_id_list))
        for account_id in self.room_account_id_list:
            player = self.get_player(account_id)
            send.player_dispatch_cards(execute_account_id, player)

