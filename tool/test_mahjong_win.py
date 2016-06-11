# coding:utf8
import copy


MAH_OPERATOR_NONE = 0               # 不操作
MAH_OPERATOR_CHOW = 1               # 吃
MAH_OPERATOR_PONG = 2               # 碰
MAH_OPERATOR_KONG_LIGHT = 3         # 明杠
MAH_OPERATOR_KONG_DARK = 4          # 暗杠
MAH_OPERATOR_WIN = 5                # 胡
MAH_OPERATOR_DRAWN = 6              # 自摸


MAH_CONFIG = dict()     # {card: {pre_list: [], cur_list: [], next_list: []}, ...}


def _initialize_mahjong():

    def _gen_card(base):
        return [base + _card for _card in xrange(0, 4)]

    name_config = {1: 'Wang', 2: 'Tiao', 3: 'Tong'}
    begin = 1
    end = 108
    per_count = 36
    max_index = end / 4 - 1

    for index, i in enumerate(xrange(begin, end + 1, 4)):
        pre_list = _gen_card((index - 1) * 4 + 1) if index > 0 else []
        cur_list = _gen_card(index * 4 + 1)
        next_list = _gen_card((index + 1) * 4 + 1) if index < max_index else []
        card_index = index % 9 + 1
        card_type = i / per_count + 1
        name = '{}{}'.format(card_index, name_config.get(card_type, 'unknown'))
        for c in range(i, i + 4):
            MAH_CONFIG[c] = {
                'pre_list': pre_list,
                'cur_list': cur_list,
                'next_list': next_list,
                'name': name,
                'card_index': card_index,
                'card_type': card_type
            }


_initialize_mahjong()


def check_mahjong_win(card_id, cards):
    card_list = [card_id] + cards
    card_list.sort()
    print '[game] check_mahjong_win card_list: {}'.format(card_list)
    # 统计
    all_card_gather = dict()

    for card_id in card_list:
        conf = MAH_CONFIG[card_id]
        card_gather = all_card_gather.setdefault(conf['card_type'], dict())
        card_gather[conf['card_index']] = card_gather.get(conf['card_index'], 0) + 1
    print 'all_card_gather content -----------------------------: '
    for _id, info in all_card_gather.items():
        print '_id: {}, info: {}'.format(_id, info)
    door_list = []
    for card_type, info in all_card_gather.items():
        l = [[_id, _count, card_type] for _id, _count in info.items() if _count >= 2]
        if l:
            door_list.extend(l)
    print '[game] check_mahjong_win all_card_gather: {}'.format(all_card_gather)
    print '[game] check_mahjong_win door_list: {}'.format(door_list)

    if not door_list:
        return False

    def _pre_treatment(_gather):
        def _match(match_index, match_count, _g):
            next_1_count = _g.get(match_index + 1, 0)
            next_2_count = _g.get(match_index + 2, 0)
            min_next_count = min(next_1_count, next_2_count)
            if min_next_count > 0:
                min_count = min(min_next_count, match_count)
                _g[match_index] -= min_count
                _g[match_index + 1] -= min_count
                _g[match_index + 2] -= min_count

        for _card_index, _card_count in _gather.iteritems():
            if _card_count <= 0:
                continue
            if _card_count <= 3:
                print '\npre _pre_treatment _card_index: {}, _card_count: {}, _gather: {}'.format(
                    _card_index, _card_count, _gather
                )
                _match(_card_index, _card_count, _gather)
                print 'now _pre_treatment _card_index: {}, _card_count: {}, _gather: {}\n'.format(
                    _card_index, _card_count, _gather
                )
            elif _card_count == 4:
                _gather[_card_index] = 1
                _match(_card_index, 1, _gather)

    for door_id, _, door_card_type in door_list:
        print '\n[game] check_mahjong_win door_id: {}'.format(door_id)
        all_gather = copy.deepcopy(all_card_gather)
        win_flag = True
        for _type, _card_gather in all_gather.items():
            print 'all_gather: {}'.format(all_gather)
            print '-------------------------------------------------_type: {}, _card_gather: {}'.format(
                _type, _card_gather
            )
            if _type == door_card_type and door_id in _card_gather:
                _card_gather[door_id] -= 2
            print '====================\n[game] check_mahjong_win _pre_treatment pre _gather: {}'.format(_card_gather)
            _pre_treatment(_card_gather)
            print '[game] check_mahjong_win _pre_treatment now _gather: {}\n'.format(_card_gather)
            for _c in _card_gather.values():
                if _c > 0:
                    win_flag = False
                    break
            if not win_flag:
                break
        print '[game] check_mahjong_win all_gather now: {}'.format(all_gather)
        if win_flag:
            print '[game] check_mahjong_win +++++++++++++++++ door_id: {} WIN +++++++++++++++'.format(
                    door_id)
            return True
    return False


test_card_list = [1, 5, 9, 13, 17, 21, 25, 26, 37, 41, 45, 53, 57]
test_card_id = 61

test_un_card_list = [1, 5, 9, 13, 17, 21, 25, 26, 37, 41, 45, 53, 57]
test_un_card_id = 28


if check_mahjong_win(test_card_id, test_card_list):
    print 'the result is win'
else:
    print 'the result is lose'



