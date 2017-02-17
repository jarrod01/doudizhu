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

def pattern_spot(cards):
    patterns = {'two_jokers': 0, 'fours': {}, 'threes': {}, 'twos': {}, 'ones': {}, 'four_twos': [],
                'three_twos': [], 'three_ones': [], 'straights': [], 'straights_double': [],
                'straights_triple': [], 'st_with_twos': [], 'st_with_ones': []} #字典的底层value都是牌的序号格式为{牌: 牌的序号}
    """
    单、对、三带、炸弹的格式为{牌: 牌的序号}
    顺子（单顺/双顺/飞机）的格式[{牌：序，牌：序……}，{牌：序，牌：序……}]
    四带二、三带二、三带一、飞机带翅膀的格式为[({牌：序}，{牌，序}，{牌，序})，({牌：序}，{牌，序}，{牌，序})]
    """
    nums = [int(i/10) for i in cards]
    if nums.count(14) == 2:
        patterns['two_jokers'] = 1
    """找到单、对、三带、炸弹、顺子、双顺、飞机"""
    i = 0
    straights = {'count': 0, 'sn': 0, 'cards': [{}]} #存储多个顺子，格式为{牌: 牌的序号},sn为顺子的序号
    straights_double = {'count': 0, 'sn': 0, 'cards': [{}]}
    straights_triple = {'count': 0, 'sn': 0, 'cards': [{}]}
    while i < len(nums):
        c = nums.count(nums[i])
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
                straights['count'] = 0
        if c >= 2:
            if straights_double['count'] == 0:
                t2 = nums[i]
                straights_double['count'] += 1
                straights_double['cards'][straights_double['sn']][nums[i]] = i
            else:
                if nums[i] == t2 + straights_double['count']:
                    straights_double['count'] += 1
                    straights_double['cards'][straights_double['sn']][nums[i]] = i
                else:
                    if straights_double['count'] >= 3:
                        straights_double['sn'] += 1
                        straights_double['cards'].append({})
                    else:
                        straights_double['cards'][straights_double['sn']] = {}
                    straights_double['count'] = 0
        if c >= 3:
            if straights_triple['count'] == 0:
                t3 = nums[i]
                straights_triple['count'] += 1
                straights_triple['cards'][straights_triple['sn']][nums[i]] = i
            else:
                if nums[i] == t3 + straights_triple['count']:
                    straights_triple['count'] += 1
                    straights_triple['cards'][straights_triple['sn']][nums[i]] = i
                else:
                    if straights_triple['count'] >= 2:
                        straights_triple['sn'] += 1
                        straights_triple['cards'].append({})
                    else:
                        straights_triple['cards'][straights_triple['sn']] = {}
                    straights_triple['count'] = 0
        if c == 1:
            patterns['ones'][nums[i]] = i
            i += 1
        elif c == 2:
            patterns['ones'][nums[i]] = i
            if nums[i] == 14:
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
    if straights['sn'] != 0:
        patterns['straights'] = straights['cards']
    if straights_double['sn'] != 0:
        patterns['straights_double'] = straights_double['cards']
    if straights_triple['sn'] != 0:
        patterns['straights_triple'] = straights_triple['cards']
    """找到四带二"""
    if patterns['fours'] and len(patterns['ones']) > 1:
        for f in patterns['fours'].keys():
            tmp = list(patterns['ones'].keys())
            if f in tmp and (len(tmp) == 2):
                continue
            i = 0
            while i < len(tmp)-1:
                if f == tmp[i] or f == tmp[i+1]:
                    continue
                patterns['four_twos'].append(({f: patterns['fours'][f]},
                                              {tmp[i]: patterns['ones'][tmp[i]]},
                                              {tmp[i + 1]: patterns['ones'][tmp[i + 1]]}))
                i += 1
    if patterns['fours'] and len(patterns['twos']) > 1:
        for f in patterns['fours'].keys():
            tmp = list(patterns['twos'].keys())
            if f in tmp and len(tmp) == 2:
                continue
            i = 0
            while i < len(tmp)-1:
                if f == tmp[i] or f == tmp[i+1]:
                    continue
                patterns['four_twos'].append(({f: patterns['fours'][f]},
                                              {tmp[i]: patterns['twos'][tmp[i]]},
                                              {tmp[i+1]: patterns['twos'][tmp[i+1]]}))
                i += 1
    """找到三带二"""
    if patterns['threes'] and len(patterns['ones']) > 0:
        for f in patterns['threes'].keys():
            tmp = list(patterns['ones'].keys())
            if f in tmp and len(tmp) == 1:
                continue
            i = 0
            while i < len(tmp)-1:
                if f == tmp[i] or f == tmp[i+1]:
                    continue
                patterns['three_ones'].append(({f: patterns['threes'][f]},
                                              {tmp[i]: patterns['ones'][tmp[i]]},
                                              {tmp[i + 1]: patterns['ones'][tmp[i + 1]]}))
                i += 1
    if patterns['threes'] and len(patterns['twos']) > 0:
        for f in patterns['threes'].keys():
            tmp = list(patterns['twos'].keys())
            if f in tmp and len(tmp) == 1:
                continue
            i = 0
            while i < len(tmp)-1:
                if f == tmp[i] or f == tmp[i+1]:
                    continue
                patterns['three_twos'].append(({f: patterns['threes'][f]},
                                              {tmp[i]: patterns['twos'][tmp[i]]},
                                              {tmp[i+1]: patterns['twos'][tmp[i+1]]}))
                i += 1
    return patterns



if __name__ == '__main__':
    cards = poker_distribute()
    tmp_cards = [11, 21, 31, 32, 33, 34, 41, 42, 43, 51, 54, 82, 83, 84, 93, 101, 112, 124, 134]
    pattern = pattern_spot(tmp_cards)
    with open('patterns', 'w', encoding='utf-8') as f:
        json.dump(pattern, f, ensure_ascii=False)