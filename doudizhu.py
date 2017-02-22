from random import randint
import json, time

def poker_distribute():
    pokers = []
    for i in range(1, 14):
        for j in range(1, 5):
            pokers.append(i*10+j) #以最后一位代表花色，前一位或两位代表数字
    pokers += [141, 142]
    player = {0: [], 1: [], 2: [], 3: []}
    for i in range(0, 51):
        t = randint(0, len(pokers)-1)
        player[i%3].append(pokers[t])
        pokers.remove(pokers[t])
    player[3] = pokers
    for p in player:
        player[p].sort()
        #print(str(p + 1) + ': ' + print_cards(player[p]))
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
                        straights_triple['cards'].append([])

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
            print('可能有人作弊，牌数不对, 一共' + str(c) + '张' + str(nums[i]))
            #break
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
    if in_result['nums'][0] != 0:
        ln = len(in_result['nums'])
    patterns = pattern_spot(cards)
    def st3_with_twos(patterns):
        n = patterns[0]
        n1 = patterns[3]
        n2 = patterns[4]
        n3 = patterns[5]
        return [n, n, n, n+1, n+1, n+1, n+2, n+2, n+2, n1, n1, n2, n2, n3, n3]
    def st3_with_ones(patterns):
        n = patterns[0]
        n1 = patterns[3]
        n2 = patterns[4]
        n3 = patterns[5]
        return [n, n, n, n+1, n+1, n+1, n+2, n+2, n+2, n1, n2, n3]
    def st_with_twos(patterns):
        n = patterns[0]
        n1 = patterns[2]
        n2 = patterns[3]
        return [n, n, n, n+1, n+1, n+1, n1, n1, n2, n2]
    def st_with_ones(patterns):
        n = patterns[0]
        n1 = patterns[2]
        n2 = patterns[3]
        return [n, n, n, n+1, n+1, n+1, n1, n2]
    def three_twos(patterns):
        n = patterns[0]
        n1 = patterns[1]
        return [n, n, n, n1, n1]
    def three_ones(patterns):
        n = patterns[0]
        n1 = patterns[1]
        return [n, n, n, n1]
    """当第一个出牌的时候或者对方大不了自己出牌的时候的策略"""
    if in_result['nums'][0] == 0 and in_result['result'] == 'null':
        if patterns['st3_with_twos']:
            return st3_with_twos(patterns['st3_with_twos'][0])
        if patterns['st3_with_ones']:
            return st3_with_ones(patterns['st3_with_ones'][0])
        if patterns['st_with_twos']:
            return st_with_twos(patterns['st_with_twos'][0])
        if patterns['st_with_ones']:
            return st_with_ones(patterns['st_with_ones'][0])
        if patterns['straights_triple']:
            result = []
            tmp = patterns['straights_triple'][0]
            for i in range(len(tmp)):
                result += [tmp[i]]*3
            return result
        if patterns['straights_double']:
            result = []
            tmp = patterns['straights_double'][0]
            for i in range(len(tmp)):
                result += [tmp[i]] * 2
            return result
        if patterns['straights']:
            result = []
            tmp = patterns['straights'][0]
            for i in range(len(tmp)):
                result.append(tmp[i])
            return result
        if patterns['three_twos']:
            return three_twos(patterns['three_twos'][0])
        if patterns['three_ones']:
            return three_ones(patterns['three_ones'][0])
        if patterns['fours'] and len(cards) == 4:
            n = cards[0]
            return [n] * 4
        if patterns['threes']:
            for i in range(len(patterns['threes'])):
                n = patterns['threes'][i]
                if n not in patterns['fours']:
                    return [n] * 3
        if patterns['twos']:
            for i in range(len(patterns['twos'])):
                n = patterns['twos'][i]
                if n not in patterns['threes']:
                    return [n] * 2
        if patterns['two_jokers'] and len(cards) == 2:
            return [14, 14]
        if patterns['ones']:
            for i in range(len(patterns['ones'])):
                n = patterns['ones'][i]
                if n not in patterns['twos']:
                    return [n]
    if len(cards) == 0:
        print('无牌可打了!')
        return []
    if in_pattern == 'two_jokers':
        return []
    elif in_pattern == 'fours':
        if patterns['fours']:
            for n in patterns['fours']:
                if n > in_nums:
                    return [n] * 4
    elif in_pattern == 'four_two_ones' or in_pattern == 'four_two_twos':
        if patterns['fours']:
            n = patterns['fours']
            return [n] * 4
    #当出单的时候尽量不破坏对子，以下同理
    elif in_pattern == 'ones':
        tmp = patterns['ones'].copy()
        for n in patterns['ones']:
            if n in patterns['twos']:
                tmp.remove(n)
        if tmp:
            for n in tmp:
                if n > in_nums:
                    return [n]
        for n in patterns['ones']:
            if n > in_nums:
                return [n]
    elif in_pattern == 'twos':
        if patterns['twos']:
            tmp = patterns['twos'].copy()
            for n in patterns['twos']:
                if n in patterns['threes']:
                    tmp.remove(n)
            if tmp:
                for n in tmp:
                    if n > in_nums:
                        return [n, n]
            for n in patterns['twos']:
                if n > in_nums:
                    return [n, n]
    elif in_pattern == 'threes':
        if patterns['threes']:
            tmp = patterns['threes'].copy()
            for n in patterns['threes']:
                if n in patterns['fours']:
                    tmp.remove(n)
            if tmp:
                for n in tmp:
                    if n > in_nums:
                        return [n] * 3
            for n in patterns['threes']:
                if n > in_nums:
                    return [n] * 3
    else:
        if patterns[in_pattern]:
            for to in patterns[in_pattern]:
                n = to[0]
                # 根据情况判断链子，如果第一个数大于对方的第一个数字，就取第一个，否则如果对方最后一个数字
                # 小于我方最后一个数字，则取对方第一个数字加1
                if in_pattern == 'straights':
                    if len(to) >= ln:
                        if n > in_nums:
                            result = []
                            for i in range(ln):
                                result.append(to[i])
                            return result
                        elif in_nums + ln -1 < to[-1]:
                            result = []
                            for i in range(1, ln+1):
                                result.append(in_nums + i)
                            return result
                elif in_pattern == 'straights_double':
                    if len(to) >= ln:
                        if n > in_nums:
                            result = []
                            for i in range(ln):
                                result += [to[i]] * 2
                            return result
                        elif in_nums + ln -1 < to[-1]:
                            result = []
                            for i in range(1, ln+1):
                                result += [in_nums + 1] * 2
                            return result
                elif in_pattern == 'straights_triple':
                    if len(to) >= ln:
                        if n > in_nums:
                            result = []
                            for i in range(ln):
                                result += [to[i]] * 3
                            return result
                        elif in_nums + ln -1 < to[-1]:
                            result = []
                            for i in range(1, ln + 1):
                                result += [in_nums + 1] * 3
                            return result
                if n > in_nums:
                    if in_pattern == 'three_ones':
                        return three_ones(to)
                    elif in_pattern == 'three_twos':
                        return three_twos(to)
                    elif in_pattern == 'st_with_ones':
                        return st_with_ones(to)
                    elif in_pattern == 'st_with_twos':
                        return st_with_twos(to)
                    elif in_pattern == 'st3_with_ones':
                        return st3_with_ones(to)
                    elif in_pattern == 'st3_with_twos':
                        return st3_with_twos(to)
    if patterns['fours'] and in_pattern != 'fours':
        n = patterns['fours'][0]
        return [n] * 4
    if patterns['two_jokers']:
        return [14, 14]
    else:
        return []

def compare(a, b):
    if a['nums'] == [0] and a['result'] == 'null':
        return True
    if not ( b['validate'] and a['validate']):
        return False
    if b['result'] == 'two_jokers':
        return True
    elif b['result'] == 'fours' and a['result'] != 'fours' and a['result'] != 'two_jokers':
        return True
    elif a['result'] == b['result']:
        return a['nums'][0] < b['nums'][0]
    else:
        return False

def rearrange(cards, nums):
    if not nums:
        return []
    nums = list(nums)
    tmp = [int(i/10) for i in cards]
    out_cards = []
    for i in range(len(cards)):
        if tmp[i] in nums:
            out_cards.append(cards[i])
            nums.remove(tmp[i])
    return out_cards

def print_cards(cards):
    colors = ['♥', '♠', '♦', '♣']
    new_cards = []
    for card in cards:
        n = int(card / 10)
        f = card % 10
        if n < 9:
            new_cards.append(str(n + 2) + colors[f - 1])
        elif n == 9:
            new_cards.append('J' + colors[f - 1])
        elif n == 10:
            new_cards.append('Q' + colors[f - 1])
        elif n == 11:
            new_cards.append('K' + colors[f - 1])
        elif n == 12:
            new_cards.append('A' + colors[f - 1])
        elif n == 13:
            new_cards.append('2' + colors[f - 1])
        elif n == 14 and f == 1:
            new_cards.append('JokerI')
        elif n == 14 and f == 2:
            new_cards.append('JokerII')
    s = ' '.join(new_cards)
    return s


def play(n):
    players_cards = poker_distribute()
    patterns = []
    scores = []
    person = []
    for i in range(3):
        if i < n:
            person.append(1)
        else:
            person.append(0)
        players_cards[i].sort()
        patterns.append(pattern_spot(players_cards[i]))
    # 开始叫分
    for i in range(3):
        if person[i]:
            print(str(i+1) + '号玩家，您的牌是: ')
            print(print_cards(players_cards[i]))
            scores.append(int(input('请叫分(1-3分):')))
        else:
            if patterns[i]['two_jokers'] or patterns[i]['fours']:
                scores.append(3)
            elif 14 in patterns[i]['ones']:
                scores.append(2)
            else:
                scores.append(1)
    print('底牌是： ' + print_cards(players_cards[3]))
    dizhu = scores.index(max(scores))
    players_cards[dizhu] += players_cards[3]
    players_cards[dizhu].sort()
    print('地主是' + str(dizhu+1) + '号玩家！')
    finished = False
    pass_me = [1, 1, 1]
    i = dizhu
    can_pass = False
    while not finished:
        i = i % 3
        # 如果上家和下家都没有出牌，则将对比的last_result初始化
        if pass_me[(i - 1) % 3] and pass_me[(i - 2) % 3]:
            last_result = {'validate': True, 'nums': [0], 'result': 'null'}
            can_pass = False
        else:
            can_pass = True
        # 机器先算出来可不可以大过
        out_nums = strategy(players_cards[i], last_result)
        if not out_nums:
            pass_me[i] = 1
            if person[i]:
                print('\n' + str(i + 1) + '号玩家，您的牌是： ' + print_cards(players_cards[i]) + '\n没有牌能够大过上家， 5秒后下家出牌！')
                time.sleep(5)
            else:
                time.sleep(randint(1, 2)) #机器假装思考
        else:
            pass_me[i] = 0 #先把pass设为0，如果用户选择pass再设为1
            if person[i]:
                print('\n' + str(i + 1) + '号玩家，您的牌是： ' + print_cards(players_cards[i]))
                s = input('请出牌，输入牌，以空格分割， 如果不出请按回车：')
                s = s.strip()
                s = s.split(' ')
                try:
                    out_nums = []
                    for n in s:
                        if n == 'J' or n == 'j' or n == '11':
                            out_nums.append(9)
                        elif n == 'Q' or n == 'q' or n == '12':
                            out_nums.append(10)
                        elif n == 'K' or n == 'k' or n == '13':
                            out_nums.append(11)
                        elif n == 'A' or n == 'a' or n == '1':
                            out_nums.append(12)
                        elif n == '2':
                            out_nums.append(13)
                        elif 'joker' in n.lower() or n == '14':
                            out_nums.append(14)
                        elif n in ['3', '4', '5', '6', '7', '8', '9', '10']:
                            out_nums.append(int(n) - 2)
                    if not out_nums:
                        pass_me[i] = 1
                except:
                    print('输入有误，请重新输入：')
                    continue
            else:
                time.sleep(randint(1, 3)) #机器假装思考
        out_cards = rearrange(players_cards[i], out_nums)
        #检测是否可以pass
        if not can_pass and pass_me[i]:
            print(str(i + 1) + '号玩家，您不能跳过出牌！')
            continue
        if pass_me[i]:
            print(str(i + 1) + '号玩家过！')
        else:
            out_result = cards_validate(out_cards)
            bigger = compare(last_result, out_result)
            if bigger and out_result['validate']:
                print(str(i+1) + '号玩家出的牌是' + print_cards(out_cards))
                for card in out_cards:
                    players_cards[i].remove(card)
                last_result = out_result
                if len(players_cards[i]) == 0:
                    print(str(i + 1) + '号玩家胜！')
                    finished = True
            elif not out_result['validate']:
                print('牌不合法')
                continue
            else:
                print('您出的牌比上家小，或者牌型和上家不一样！')
                continue
        i += 1

if __name__ == '__main__':
    play(0)
    # cards = [12, 13, 22, 24, 25]
    # tmp_cards = [11, 23, 24, 31, 53, 61, 62, 63, 73, 94, 101, 104, 112, 131, 133, 141, 142]
    # tmp_cards.sort()
    # cards = rearrange(tmp_cards, [1,1,2,10])
    # print(tmp_cards)
    #patterns = pattern_spot(tmp_cards)
    # print(json.dumps(patterns))
    # with open('patterns', 'w', encoding='utf-8') as f:
    #     for p in patterns:
    #         s = p + ': ' + json.dumps(patterns[p]) + '\n'
    #         f.write(s)
    # a = {'validate': True, 'nums': [0], 'result': 'null'}
    # result = strategy(tmp_cards, a)
    # print(result)
    # b = {'validate': True, 'nums': [13, 2], 'result': 'three_ones'}
    # result = compare(a, b)
    # if result:
    #     print('a < b')
    # else:
    #     print('a > b')
