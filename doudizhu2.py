from random import randint
import json

def poker_distribute():
    pokers = []
    for i in range(1, 14):
        for j in range(1, 5):
            pokers.append(i*10+j)
    pokers += [141, 142]
    player = {0: [], 1: [], 2: [], 3: []}
    for i in range(0, 51):
        t = randint(0, len(pokers)-1)
        player[i%3].append(pokers[t])
        pokers.remove(pokers[t])
    player[3] = pokers
    for p in player:
        player[p].sort()
        print(str(p) + ': ' + ''.join(str(player[p])))
    return player

def pattern_spot(in_cards):
    patterns = {'two_jokers': 0, 'fours': [], 'threes': [], 'twos': [], 'ones': [], 'four_two_ones': [], 'four_two_twos': [],
                'three_twos': [], 'three_ones': [], 'straights': [], 'straights_double': [],
                'straights_triple': [], 'st_with_twos': [], 'st_with_ones': [], 'st3_with_twos': [], 'st3_with_ones': [],
                'st4_with_twos': [], 'st4_with_ones': []} #字典的底层value都是牌的序号格式为{牌: 牌的序号}
    nums = [int(i/10) for i in in_cards]
    if nums.count(14) == 2:
        patterns['two_jokers'] = 1
    """找到单、对、三带、炸弹、顺子、双顺、飞机"""
    i = 0
    straights = {'count': 0, 'sn': 0, 'cards': [[]]} #存储多个顺子，格式为{牌: 牌的序号},sn为顺子的序号
    straights_double = {'count': 0, 'sn': 0, 'cards': [[]]}
    straights_triple = {'count': 0, 'sn': 0, 'cards': [[]]}
    while i < len(nums):
        c = nums.count(nums[i])
        num_now = nums[i]
        if straights['count'] == 0:
            t = nums[i]
            straights['count'] += 1
            straights['cards'][straights['sn']].append(nums[i])
        else:
            if nums[i] == t+straights['count']:
                straights['count'] += 1
                straights['cards'][straights['sn']].append(nums[i])
            else:
                if straights['count'] >= 5:
                    straights['sn'] += 1
                    straights['cards'].append([])
                else:
                    straights['cards'][straights['sn']] = []
                straights['count'] = 1
                t = nums[i]
                straights['cards'][straights['sn']].append(nums[i])
        if c >= 2:
            if straights_double['count'] == 0:
                t2 = nums[i]
                straights_double['count'] += 1
                straights_double['cards'][straights_double['sn']].append(nums[i])
            else:
                if nums[i] == t2 + straights_double['count']:
                    straights_double['count'] += 1
                    straights_double['cards'][straights_double['sn']].append(nums[i])
                else:
                    if straights_double['count'] >= 3:
                        straights_double['sn'] += 1
                        straights_double['cards'].append([])

                    else:
                        straights_double['cards'][straights_double['sn']] = []
                    straights_double['count'] = 1
                    t2 = nums[i]
                    straights_double['cards'][straights_double['sn']].append(nums[i])
        if c >= 3:
            if straights_triple['count'] == 0:
                t3 = nums[i]
                straights_triple['count'] += 1
                straights_triple['cards'][straights_triple['sn']].append(nums[i])
            else:
                if nums[i] == t3 + straights_triple['count']:
                    straights_triple['count'] += 1
                    straights_triple['cards'][straights_triple['sn']].append(nums[i])
                else:
                    if straights_triple['count'] >= 2:
                        straights_triple['sn'] += 1
                        straights_triple['cards'].append({})

                    else:
                        straights_triple['cards'][straights_triple['sn']] = []
                    straights_triple['count'] = 1
                    t3 = nums[i]
                    straights_triple['cards'][straights_triple['sn']].append(nums[i])
        if c == 1:
            patterns['ones'].append(nums[i])
            i += 1
        elif c == 2:
            patterns['ones'].append(nums[i])
            if nums[i] == 14:
                i += 2
                continue
            patterns['twos'].append(nums[i])
            i += 2
        elif c == 3:
            patterns['threes'].append(nums[i])
            patterns['twos'].append(nums[i])
            patterns['ones'].append(nums[i])
            i += 3
        elif c == 4:
            patterns['fours'].append(nums[i])
            patterns['threes'].append(nums[i])
            patterns['twos'].append(nums[i])
            patterns['ones'].append(nums[i])
            i += 4
        else:
            print('可能有人作弊，牌数不对')
            break
    for cards in straights['cards']:
        if 14 in cards:
            cards.remove(14)
        if 13 in cards:
            cards.remove(13)
        if len(cards) >= 5:
            patterns['straights'].append(cards)
    for cards in straights_double['cards']:
        if 14 in cards:
            cards.remove(14)
        if 13 in cards:
            cards.remove(13)
        if len(cards) >= 3:
            patterns['straights_double'].append(cards)
    for cards in straights_triple['cards']:
        if 13 in cards:
            cards.remove(13)
        if len(cards) >= 2:
            patterns['straights_triple'].append(cards)
    """找到四带二"""
    if patterns['fours']:
        for f in patterns['fours']:
            tmp = patterns['ones'].copy()
            if len(tmp) < 2:
                continue
            if f in tmp:
                tmp.remove(f)
            i = 0
            while i < len(tmp)-1:
                j = i + 1
                while j < len(tmp):
                    patterns['four_two_ones'].append((f, tmp[i], tmp[j]))
                    j += 1
                i += 1
            for n in patterns['twos']:
                if n == f:
                    continue
                patterns['four_two_ones'].append((f, n, n))
    if patterns['fours'] and len(patterns['twos']) > 1:
        for f in patterns['fours']:
            tmp = patterns['twos'].copy()
            if f in tmp:
                tmp.remove(f)
            if len(tmp) < 2:
                continue
            i = 0
            while i < len(tmp)-1:
                j = i + 1
                while j < len(tmp):
                    patterns['four_two_twos'].append((f, tmp[i], tmp[j]))
                    j += 1
                i += 1
    """找到三带一"""
    if patterns['threes']:
        for f in patterns['threes']:
            tmp = patterns['ones'].copy()
            if len(tmp) < 1:
                continue
            i = 0
            while i < len(tmp):
                if tmp[i] == f:    #判断所带的数字是否和三带的数字一样
                    i += 1
                    continue
                patterns['three_ones'].append((f, tmp[i]))
                i += 1
    if patterns['threes'] and len(patterns['twos']) > 0:
        for f in patterns['threes']:
            tmp = patterns['twos'].copy()
            if f in tmp:
                tmp.remove(f)
            if len(tmp) < 1:
                continue
            i = 0
            while i < len(tmp):
                patterns['three_twos'].append((f, tmp[i]))
                i += 1
    """找到飞机带翅膀"""
    for striple in patterns['straights_triple']:
        with_num = ['ones', 'twos']
        for s in with_num:
            threes_with = 'three_' + s
            st_with = 'st_with_' + s
            st3_with = 'st3_with_' + s
            st4_with = 'st4_with_' + s
            i = 0
            while i < len(striple) - 1:
                j = i + 1
                tmp_list = [striple[i], striple[j]]
                attach_list = [tw[1] for tw in patterns[threes_with] if
                               tw[0] in tmp_list and tw[1] not in tmp_list]
                attach_list = list(set(attach_list))
                if s == 'ones':
                    for n in patterns['twos']:
                        if n != striple[i] and n != striple[j]:
                            patterns[st_with].append((striple[i], striple[j], n, n))
                if len(attach_list) < 2:
                    i += 1
                    continue
                ii = 0
                while ii < len(attach_list) - 1:
                    jj = ii + 1
                    while jj < len(attach_list):
                        if attach_list[ii] != attach_list[jj]:
                            patterns[st_with].append((striple[i], striple[j], attach_list[ii], attach_list[jj]))
                        jj += 1
                    ii += 1

                i += 1
            #三个飞机的情况
            if len(striple) > 2:
                i = 0
                while i < len(striple) - 2:
                    j = i + 1
                    k = j + 1
                    tmp_list2 = [striple[i], striple[j], striple[k]]
                    attach_list2 = [tw[1] for tw in patterns[threes_with] if
                                    tw[0] in tmp_list2 and tw[1] not in tmp_list2]
                    attach_list2 = list(set(attach_list2))
                    if s == 'ones':
                        for n in patterns['threes']:
                            if n not in striple:
                                patterns[st3_with].append((striple[i], striple[j], striple[k], n, n, n))
                        for n in patterns['twos']:
                            if n in tmp_list2:
                                continue
                            for n2 in patterns['ones']:
                                if n2 in tmp_list2 or n == n2:
                                    continue
                                patterns[st3_with].append((striple[i], striple[j], striple[k], n, n, n2))
                    if len(attach_list2) < 3:
                        i += 1
                        continue
                    ii = 0
                    while ii < len(attach_list2) - 2:
                        jj = ii + 1
                        while jj < len(attach_list2) - 1:
                            kk = jj + 1
                            while kk < len(attach_list2):
                                if [attach_list2[ii] != attach_list2[jj] != attach_list2[kk]] != attach_list2[ii]:
                                    patterns[st3_with].append(
                                        (striple[i], striple[j], striple[k], attach_list2[ii], attach_list2[jj],
                                         attach_list2[kk]))
                                kk += 1
                            jj += 1
                        ii += 1

                    i += 1
    """其实少写了一种四个三带的飞机带四个的极端情况"""
    return patterns

#验证所出的牌是否合理
def cards_validate(cards):
    n = len(cards)
    patterns = pattern_spot(cards)
    validate = True
    result = ''
    nums = []
    if n == 1:
        result = 'ones'
        nums = patterns['ones']
    elif n == 2:
        if patterns['two_jokers']:
            result = 'two_jokers'
            nums = [14]
        elif patterns['twos']:
            result = 'twos'
            nums = patterns['twos']
        else:
            validate = False
    elif n == 3:
        if patterns['threes']:
            result = 'threes'
            nums = patterns['threes']
        else:
            validate = False
    elif n == 4:
        if patterns['fours']:
            result = 'fours'
            nums = patterns['fours']
        elif patterns['three_ones']:
            result = 'three_ones'
            nums = patterns['three_ones'][0]
        else:
            validate = False
    elif n == 5:
        if patterns['three_twos']:
            result = 'three_twos'
            nums = patterns['three_twos'][0]
        elif patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = patterns['straights'][0]
        else:
            validate = False
    elif n == 6:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = patterns['straights'][0]
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = patterns['straights_double'][0]
        elif patterns['straights_triple'] and len(patterns['straights_triple'][0]) == n/3:
            result = 'straights_triple'
            nums = patterns['straights_triple'][0]
        elif patterns['four_two_ones']:
            result = 'four_two_ones'
            nums = patterns['four_two_ones'][0]
        else:
            validate = False
    elif n == 8:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = patterns['straights'][0]
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = patterns['straights_double'][0]
        elif patterns['four_two_twos']:
            result = 'four_two_twos'
            nums = patterns['four_two_twos'][0]
        elif patterns['st_with_ones']:
            result = 'st_with_ones'
            nums = patterns['st_with_ones'][0]
        else:
            validate = False
    elif n == 10:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = patterns['straights'][0]
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = patterns['straights_double'][0]
        elif patterns['st_with_twos']:
            result = 'st_with_twos'
            nums = patterns['st_with_twos'][0]
        else:
            validate = False
    elif n >= 12 and n % 2 ==0:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = patterns['straights'][0]
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = patterns['straights_double'][0]
        elif patterns['straights_triple'] and n %3 == 0 and len(patterns['straights_triple'][0]) == n/3:
            result = 'straights_triple'
            nums = patterns['straights_triple'][0]
        elif patterns['st3_with_ones'] and n == 12:
            result = 'st3_with_ones'
            nums = patterns['st3_with_ones'][0]
        else:
            validate = False
    elif n >= 7 and n % 2 ==1:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = patterns['straights'][0]
        elif patterns['straights_triple'] and n %3 == 0 and len(patterns['straights_triple'][0]) == n/3:
            result = 'straights_triple'
            nums = patterns['straights_triple'][0]
        elif patterns['st3_with_twos'] and n == 15:
            result = 'st3_with_twos'
            nums = patterns['st3_with_twos'][0]
        else:
            validate = False
    else:
        validate = False
    return {'validate': validate, 'result': result, 'nums': nums}


def strategy(cards, in_result):
    in_pattern = in_result['result']
    in_nums = in_result['nums'][0]
    ln = len(in_nums)
    patterns = pattern_spot(cards)
    nums = [int(i/10) for i in cards]
    bigger = False
    if not in_result['validate']:
        print("亲，打错牌了吧！")
        return False
    if len(cards) == 0:
        print('无牌可打了!')
        return False
    if in_pattern == 'two_jokers':
        return 'pass'
    elif in_pattern == 'fours' or in_pattern == 'four_two_ones' or in_pattern == 'four_two_twos':
        if patterns['fours']:
            for n in patterns['fours']:
                if n > in_nums:
                    return [{n: nums.index(n)}, {n: nums.index(n)+ 1}, {n: nums.index(n) + 2}, {n: nums.index(n) + 3}]
    elif in_pattern == 'ones':
        tmp = patterns['ones']
        for n in tmp:
            if n in patterns['twos']:
                tmp.remove(n)
        if tmp:
            for n in tmp:
                if n > in_nums:
                    return [{n: nums.index(n)}]
        for n in patterns['ones']:
            if n > in_nums:
                return [{n: nums.index(n)}]
    elif in_pattern == 'twos':
        if patterns['twos']:
            tmp = patterns['twos']
            for n in tmp:
                if n in patterns['threes']:
                    tmp.remove(n)
            if tmp:
                for n in tmp:
                    if n > in_nums:
                        return [{n: nums.index(n)}, {n: nums.index(n) + 1}]
            for n in patterns['twos']:
                if n > in_nums:
                    return [{n: nums.index(n)}, {n: nums.index(n) + 1}]
    elif in_pattern == 'threes':
        if patterns['threes']:
            tmp = patterns['threes']
            for n in tmp:
                if n in patterns['fours']:
                    tmp.remove(n)
            if tmp:
                for n in tmp:
                    if n > in_nums:
                        return [{n: nums.index(n)}, {n: nums.index(n) + 1}, {n: nums.index(n) + 2}]
            for n in patterns['threes']:
                if n > in_nums:
                    return [{n: nums.index(n)}, {n: nums.index(n) + 1}, {n: nums.index(n) + 2}]
    else:
        if patterns[in_pattern]:
            for to in patterns[in_pattern]:
                n = to[0]
                if in_pattern == 'straights':
                    if len(to) >= ln:
                        if n > in_nums:
                            result = []
                            for i in range(ln):
                                result.append({to[i], nums.index(to[i])})
                            return result
                        elif in_nums + ln -1 < to[-1]:
                            result = []
                            for i in range(ln):
                                result.append({in_nums + 1, nums.index(in_nums + 1)})
                            return result
                elif in_pattern == 'straights_double':
                    if len(to) >= ln:
                        if n > in_nums:
                            result = []
                            for i in range(ln):
                                result.append({to[i], nums.index(to[i])})
                                result.append({to[i], nums.index(to[i]) + 1})
                            return result
                        elif in_nums + ln -1 < to[-1]:
                            result = []
                            for i in range(ln):
                                result.append({in_nums + 1, nums.index(in_nums + 1)})
                                result.append({in_nums + 1, nums.index(in_nums + 1) + 1})
                            return result
                elif in_pattern == 'straights_triple':
                    if len(to) >= ln:
                        if n > in_nums:
                            result = []
                            for i in range(ln):
                                result.append({to[i], nums.index(to[i])})
                                result.append({to[i], nums.index(to[i]) + 1})
                                result.append({to[i], nums.index(to[i]) + 2})
                            return result
                        elif in_nums + ln -1 < to[-1]:
                            result = []
                            for i in range(ln):
                                result.append({in_nums + 1, nums.index(in_nums + 1)})
                                result.append({in_nums + 1, nums.index(in_nums + 1) + 1})
                                result.append({in_nums + 1, nums.index(in_nums + 1) + 2})
                            return result
                if n > in_nums:
                    if in_pattern == 'threes_ones':
                        return [{n: nums.index(n)}, {n: nums.index(n)+ 1},
                                {n: nums.index(n) + 2}, {to[1]: nums.index(to[1])}]
                    elif in_pattern == 'three_twos':
                        return [{n: nums.index(n)}, {n: nums.index(n)+ 1}, {n: nums.index(n) + 2},
                            {to[1]: nums.index(to[1])}, {to[1]: nums.index(to[1]) + 1}]
                    elif in_pattern == 'st_with_ones':
                        n1 = to[2]
                        n2 = to[3]
                        return [{n: nums.index(n)}, {n: nums.index(n)+ 1}, {n: nums.index(n) + 2},
                                {n + 1: nums.index(n+1)}, {n+1: nums.index(n+1) + 1}, {n+1: nums.index(n+1) + 2},
                                {n1: nums.index(n1)}, {n2: nums.index(n2)}]
                    elif in_pattern == 'st_with_ones':
                        n1 = to[2]
                        n2 = to[3]
                        return [{n: nums.index(n)}, {n: nums.index(n)+ 1}, {n: nums.index(n) + 2},
                                {n + 1: nums.index(n+1)}, {n+1: nums.index(n+1) + 1}, {n+1: nums.index(n+1) + 2},
                                {n1: nums.index(n1)}, {n1: nums.index(n1)+1},
                                {n2: nums.index(n2)}, {n2: nums.index(n2)+1}]
                    elif in_pattern == 'st3_with_ones':
                        n1 = to[3]
                        n2 = to[4]
                        n3 = to[5]
                        return [{n: nums.index(n)}, {n: nums.index(n)+ 1}, {n: nums.index(n) + 2},
                                {n + 1: nums.index(n+1)}, {n+1: nums.index(n+1) + 1}, {n+1: nums.index(n+1) + 2},
                                {n + 2: nums.index(n + 2)}, {n + 2: nums.index(n + 2) + 1},
                                {n + 2: nums.index(n + 2) + 2},
                                {n1: nums.index(n1)}, {n2: nums.index(n2)}, {n3: nums.index(n3)}]
                    elif in_pattern == 'st3_with_twos':
                        n1 = to[3]
                        n2 = to[4]
                        n3 = to[5]
                        return [{n: nums.index(n)}, {n: nums.index(n)+ 1}, {n: nums.index(n) + 2},
                                {n + 1: nums.index(n+1)}, {n+1: nums.index(n+1) + 1}, {n+1: nums.index(n+1) + 2},
                                {n + 2: nums.index(n + 2)}, {n + 2: nums.index(n + 2) + 1},
                                {n + 2: nums.index(n + 2) + 2},
                                {n1: nums.index(n1)}, {n1: nums.index(n1)+1},
                                {n2: nums.index(n2)}, {n2: nums.index(n2)+1},
                                {n3: nums.index(n3)}, {n3: nums.index(n3)+1}]

    if patterns['fours'] and in_pattern != 'fours':
        n = patterns['fours'][0]
        return [{n: nums.index(n)}, {n: nums.index(n) + 1}, {n: nums.index(n) + 2}, {n: nums.index(n) + 3}]
    if patterns['two_jokers']:
        return [{14: -2}, {14: -1}]
    else:
        return False

def compare(card_a, card_b):
    a = cards_validate(card_a)
    b = cards_validate(card_b)
    if b['result'] == 'two_jokers':
        return True
    elif b['result'] == 'fours' and a['result'] != 'fours':
        return True
    else:
        return a['nums'][0] < b['nums'][0]

def play(n):
    players_cards = poker_distribute()
    players = [0, 1, 2]
    patterns = []
    scores = []
    for player in players:
        patterns.append(pattern_spot(players_cards[player]))
    if n == 0:
        if patterns[0]['two_jokers']:
            pass
    if n == 1:
        print('1号玩家，您的牌是: ' + ''.join(str(players_cards[players[0]])))
        scores.append(int(input('请叫分(1-3):')))
    elif n == 2:
        print('2号玩家，您的牌是: ' + ''.join(str(players_cards[players[0]])))
        scores.append(int(input('请叫分(1-3):')))




if __name__ == '__main__':
    # cards = poker_distribute()
    tmp_cards = [33]
    tmp_cards.sort()
    patterns = cards_validate(tmp_cards)
    print(json.dumps(patterns))
    with open('patterns', 'w', encoding='utf-8') as f:
        for p in patterns:
            s = p + ': ' + json.dumps(patterns[p]) + '\n'
            f.write(s)
