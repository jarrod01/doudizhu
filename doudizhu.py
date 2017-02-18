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
    patterns = {'two_jokers': 0, 'fours': {}, 'threes': {}, 'twos': {}, 'ones': {}, 'four_two_ones': [], 'four_two_twos': [],
                'three_twos': [], 'three_ones': [], 'straights': [], 'straights_double': [],
                'straights_triple': [], 'st_with_twos': [], 'st_with_ones': []} #字典的底层value都是牌的序号格式为{牌: 牌的序号}
    """
    单、对、三带、炸弹的格式为{牌: 牌的序号}
    顺子（单顺/双顺/飞机）的格式[{牌：序，牌：序……}，{牌：序，牌：序……}],用列表表示多个顺子或者多个飞机
    四带二、三带二、三带一、飞机带翅膀的格式为[({牌：序}，{牌，序}，{牌，序})，({牌：序}，{牌，序}，{牌，序})]
    """
    nums = [int(i/10) for i in in_cards]
    if nums.count(14) == 2:
        patterns['two_jokers'] = 1
    """找到单、对、三带、炸弹、顺子、双顺、飞机"""
    i = 0
    straights = {'count': 0, 'sn': 0, 'cards': [{}]} #存储多个顺子，格式为{牌: 牌的序号},sn为顺子的序号
    straights_double = {'count': 0, 'sn': 0, 'cards': [{}]}
    straights_triple = {'count': 0, 'sn': 0, 'cards': [{}]}
    while i < len(nums):
        c = nums.count(nums[i])
        num_now = nums[i]
        if straights['count'] == 0:
            t = nums[i]
            straights['count'] += 1
            straights['cards'][straights['sn']][nums[i]] = i
        else:
            if nums[i] == t+straights['count']:
                straights['count'] += 1
                straights['cards'][straights['sn']][nums[i]] = i
            else:
                if straights['count'] >= 5:
                    straights['sn'] += 1
                    straights['cards'].append({})
                else:
                    straights['cards'][straights['sn']] = {}
                straights['count'] = 1
                t = nums[i]
                straights['cards'][straights['sn']][nums[i]] = i
        if c >= 2:
            if straights_double['count'] == 0:
                t2 = nums[i]
                straights_double['count'] += 1
                straights_double['cards'][straights_double['sn']][nums[i]] = [i, i+1]
            else:
                if nums[i] == t2 + straights_double['count']:
                    straights_double['count'] += 1
                    straights_double['cards'][straights_double['sn']][nums[i]] = [i, i+1]
                else:
                    if straights_double['count'] >= 3:
                        straights_double['sn'] += 1
                        straights_double['cards'].append({})

                    else:
                        straights_double['cards'][straights_double['sn']] = {}
                    straights_double['count'] = 1
                    t2 = nums[i]
                    straights_double['cards'][straights_double['sn']][nums[i]] = [i, i+1]
        if c >= 3:
            if straights_triple['count'] == 0:
                t3 = nums[i]
                straights_triple['count'] += 1
                straights_triple['cards'][straights_triple['sn']][nums[i]] = [i, i+1, i+2]
            else:
                if nums[i] == t3 + straights_triple['count']:
                    straights_triple['count'] += 1
                    straights_triple['cards'][straights_triple['sn']][nums[i]] = [i, i+1, i+2]
                else:
                    if straights_triple['count'] >= 2:
                        straights_triple['sn'] += 1
                        straights_triple['cards'].append({})

                    else:
                        straights_triple['cards'][straights_triple['sn']] = {}
                    straights_triple['count'] = 1
                    t3 = nums[i]
                    straights_triple['cards'][straights_triple['sn']][nums[i]] = [i, i+1, i+2]
        if c == 1:
            patterns['ones'][nums[i]] = i
            i += 1
        elif c == 2:
            patterns['ones'][nums[i]] = i
            if nums[i] == 14:
                i += 2
                continue
            patterns['twos'][nums[i]] = [i, i+1]
            i += 2
        elif c == 3:
            patterns['threes'][nums[i]] = [i, i+1, i+2]
            patterns['twos'][nums[i]] = [i, i + 1]
            patterns['ones'][nums[i]] = i
            i += 3
        elif c == 4:
            patterns['fours'][nums[i]] = [i, i+1, i+2, i+3]
            patterns['threes'][nums[i]] = [i, i + 1, i + 2]
            patterns['twos'][nums[i]] = [i, i + 1]
            patterns['ones'][nums[i]] = i
            i += 4
    for cards in straights['cards']:
        if 14 in cards.keys():
            cards.pop(14)
        if 13 in cards.keys():
            cards.pop(13)
        if len(cards) >= 5:
            patterns['straights'].append(cards)
    for cards in straights_double['cards']:
        if 14 in cards.keys():
            cards.pop(14)
        if 13 in cards.keys():
            cards.pop(13)
        if len(cards) >= 3:
            patterns['straights_double'].append(cards)
    for cards in straights_triple['cards']:
        if 13 in cards.keys():
            cards.pop(13)
        if len(cards) >= 2:
            patterns['straights_triple'].append(cards)
    """找到四带二"""
    if patterns['fours'] and len(patterns['ones']) > 1:
        for f in patterns['fours'].keys():
            tmp = list(patterns['ones'].keys())
            if f in tmp:
                tmp.remove(f)
            if len(tmp) < 2:
                continue
            i = 0
            while i < len(tmp)-1:
                j = i + 1
                while j < len(tmp):
                    patterns['four_two_ones'].append(({f: patterns['fours'][f]},
                                                  {tmp[i]: patterns['ones'][tmp[i]]},
                                                  {tmp[j]: patterns['ones'][tmp[j]]}))
                    j += 1
                i += 1
    if patterns['fours'] and len(patterns['twos']) > 1:
        for f in patterns['fours'].keys():
            tmp = list(patterns['twos'].keys())
            if f in tmp:
                tmp.remove(f)
            if len(tmp) < 2:
                continue
            i = 0
            while i < len(tmp)-1:
                j = i + 1
                while j < len(tmp):
                    patterns['four_two_twos'].append(({f: patterns['fours'][f]},
                                                  {tmp[i]: patterns['twos'][tmp[i]]},
                                                  {tmp[j]: patterns['twos'][tmp[j]]}))
                    j += 1
                i += 1
    """找到三带二"""
    if patterns['threes'] and len(patterns['ones']) > 0:
        for f in patterns['threes'].keys():
            tmp = list(patterns['ones'].keys())
            if f in tmp:
                tmp.remove(f)
            if len(tmp) < 1:
                continue
            i = 0
            while i < len(tmp):
                patterns['three_ones'].append(({f: patterns['threes'][f]},
                                              {tmp[i]: patterns['ones'][tmp[i]]}))
                i += 1
    if patterns['threes'] and len(patterns['twos']) > 0:
        for f in patterns['threes'].keys():
            tmp = list(patterns['twos'].keys())
            if f in tmp:
                tmp.remove(f)
            if len(tmp) < 1:
                continue
            i = 0
            while i < len(tmp):
                patterns['three_twos'].append(({f: patterns['threes'][f]},
                                              {tmp[i]: patterns['twos'][tmp[i]]}))
                i += 1
    """找到飞机带翅膀"""
    if patterns['straights_triple'] and len(patterns['ones']) > 1:
        for st in patterns['straights_triple']:
            tmp = list(patterns['ones'].keys())
            st_keys = list(st.keys())
            for st_key in st_keys:
                if st_key in tmp:
                    tmp.remove(st_key)
            if len(tmp) < len(st):
                continue
            i = 0
            while i < len(tmp) - 1:
                j = i + 1
                while j < len(tmp):
                    patterns['st_with_ones'].append((st,
                                                      {tmp[i]: patterns['ones'][tmp[i]]},
                                                      {tmp[j]: patterns['ones'][tmp[j]]}))
                    j += 1
                i += 1
    if patterns['straights_triple'] and len(patterns['twos']) > 1:
        for st in patterns['straights_triple']:
            tmp = list(patterns['twos'].keys())
            st_keys = list(st.keys())
            for st_key in st_keys:
                if st_key in tmp:
                    tmp.remove(st_key)
            if len(tmp) < len(st):
                continue
            i = 0
            while i < len(tmp) - 1:
                j = i + 1
                while j < len(tmp):
                    patterns['st_with_twos'].append((st,
                                                      {tmp[i]: patterns['twos'][tmp[i]]},
                                                      {tmp[j]: patterns['twos'][tmp[j]]}))
                    j += 1
                i += 1
    """缺少连续3个三带带翅膀的情况"""
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
        nums = list(patterns['ones'].keys())
    elif n == 2:
        if patterns['two_jokers']:
            result = 'two_jokers'
            nums = [14]
        elif patterns['twos']:
            result = 'twos'
            nums = list(patterns['twos'].keys())
        else:
            validate = False
    elif n == 3:
        if patterns['threes']:
            result = 'threes'
            nums = list(patterns['threes'].keys())
        else:
            validate = False
    elif n == 4:
        if patterns['fours']:
            result = 'fours'
            nums = list(patterns['fours'].keys())
        elif patterns['three_ones']:
            result = 'three_ones'
            for p in patterns['three_ones'][0]:
                nums.append(list(p.keys()))
        else:
            validate = False
    elif n == 5:
        if patterns['three_twos']:
            result = 'three_twos'
            for p in patterns['three_twos'][0]:
                nums.append(list(p.keys())[0])
        elif patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = list(patterns['straights'][0].keys())
            nums.sort()
        else:
            validate = False
    elif n == 6:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = list(patterns['straights'][0].keys())
            nums.sort()
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = list(patterns['straights_double'][0].keys())
            nums.sort()
        elif patterns['straights_triple'] and len(patterns['straights_triple'][0]) == n/3:
            result = 'straights_triple'
            nums = list(patterns['straights_triple'][0].keys())
            nums.sort()
        elif patterns['four_two_ones']:
            result = 'four_two_ones'
            for p in patterns['four_two_ones'][0]:
                nums.append(list(p.keys())[0])
        else:
            validate = False
    elif n == 8:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = list(patterns['straights'][0].keys())
            nums.sort()
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = list(patterns['straights_double'][0].keys())
            nums.sort()
        elif patterns['four_two_twos']:
            result = 'four_two_twos'
            for p in patterns['four_two_ones'][0]:
                nums.append(list(p.keys())[0])
        elif patterns['st_with_ones']:
            result = 'st_with_ones'
            for p in patterns['st_with_ones'][0]:
                nums.append(list(p.keys())[0])
        else:
            validate = False
    elif n == 10:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = list(patterns['straights'][0].keys())
            nums.sort()
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = list(patterns['straights_double'][0].keys())
            nums.sort()
        elif patterns['st_with_twos']:
            result = 'st_with_twos'
            for p in patterns['st_with_twos'][0]:
                nums.append(list(p.keys())[0])
        else:
            validate = False
    elif n >= 12 and n % 2 ==0:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = list(patterns['straights'][0].keys())
            nums.sort()
        elif patterns['straights_double'] and len(patterns['straights_double'][0]) == n/2:
            result = 'straights_double'
            nums = list(patterns['straights_double'][0].keys())
            nums.sort()
        elif patterns['straights_triple'] and n %3 == 0 and len(patterns['straights_triple'][0]) == n/3:
            result = 'straights_triple'
            nums = list(patterns['straights_triple'][0].keys())
            nums.sort()
        else:
            validate = False
    elif n >= 7 and n % 2 ==1:
        if patterns['straights'] and len(patterns['straights'][0]) == n:
            result = 'straights'
            nums = list(patterns['straights'][0].keys())
            nums.sort()
        elif patterns['straights_triple'] and n %3 == 0 and len(patterns['straights_triple'][0]) == n/3:
            result = 'straights_triple'
            nums = list(patterns['straights_triple'][0].keys())
            nums.sort()
        elif patterns['st_with_twos'] and n == 15:
            result = 'st_with_twos'
            for p in patterns['st_with_twos'][0]:
                nums.append(list(p.keys())[0])
        else:
            validate = False
    else:
        validate = False
    return {'validate': validate, 'result': result, 'nums': nums}

def strategy(cards, in_cards):
    pass

if __name__ == '__main__':
    # cards = poker_distribute()
    tmp_cards = [12,11,14,23,23,23,33,32,31,54,65,85]
    tmp_cards.sort()
    print(tmp_cards)
    patterns = pattern_spot(tmp_cards)
    print(json.dumps(patterns))
    # with open('patterns', 'w', encoding='utf-8') as f:
    #     for p in patterns:
    #         s = p + ': ' + json.dumps(patterns[p]) + '\n'
    #         f.write(s)
