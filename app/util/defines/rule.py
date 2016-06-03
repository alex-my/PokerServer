# coding:utf8


GAME_TYPE_PDK = 1               # 跑得快 每人16张版
GAME_TYPE_ZZMJ = 2              # 转转麻将
GAME_TYPE_PDK2 = 3              # 跑得快 每人15张版


rule_configs = {
    GAME_TYPE_PDK: {
        'room_price': {
            10: 0,
            20: 0,
            30: 0
        },
        'player_count': 3,
        'unit_count': 48,        # 48张扑克牌
        'original_count': 16     # 每个玩家初始牌数
    },
    GAME_TYPE_ZZMJ: {
        'room_price': {
            10: 0,
            20: 0,
            40: 0
        },
        'player_count': 4,
        'unit_count': 108,       # 108张麻将牌
        'original_count': 13     # 每个玩家初始牌数
    },
    GAME_TYPE_PDK2: {
        'room_price': {
            10: 0,
            20: 0,
            30: 0
        },
        'player_count': 3,
        'unit_count': 45,        # 48张扑克牌
        'original_count': 15     # 每个玩家初始牌数
    },
}







