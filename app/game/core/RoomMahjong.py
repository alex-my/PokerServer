# coding:utf8
from app.game.core.Room import Room
from app.game.action import send
from app.util.defines import status
from app.util.common import func


class RoomMahjong(Room):

    def __init__(self):
        super(RoomMahjong, self).__init__()

    def dispatch_all_card(self):
        self.random_cards()
        self.room_player_status(status.PLAYER_STATUS_NORMAL)
        execute_account_id = self.execute_account_id
        func.log_info('[game] RoomMahjong dispatch_all_card room_account_id_list: {}'.format(self.room_account_id_list))
        for account_id in self.room_account_id_list:
            player = self.get_player(account_id)
            send.player_dispatch_cards(execute_account_id, player)
            if account_id == execute_account_id:
                card = self.pop_card()
                send.dispatch_mahjong_card(player.dynamic_id, card)

    def pop_card(self):
        return self._cards.pop()

    def is_card_clear(self):
        return len(self._cards) == 0

