mod = 33

def build_cur_freq(text: str) -> dict[str: float]:
    cur_freq = dict()
    for i in freq:
        cur_freq[i] = 0
    cnt = 0
    for i in text:
        if i.isalpha():
            cur_freq[i] += 1
            cnt += 1

    for i in cur_freq:
        cur_freq[i] = cur_freq[i] * 100 / cnt
    return cur_freq

def build_matches(cur_freq: dict[str: float], freq: dict[str: float], eps: float) -> dict[str: list[int]]:
    matches = dict()
    for i in cur_freq:
        matches[i] = []
        for j in freq:
            if abs(cur_freq[i] - freq[j]) <= eps:
                value1 = ord(i)
                value2 = ord(j)
                matches[i].append((value1 - value2 + mod) % mod)
    return matches

def find_key(matches: dict[str: list[str]], possible: list[list[str]], text: str) -> str:
    id = 0
    l = len(possible)
    for i in range(len(text)):
        if not text[i].isalpha():
            continue
        cur_m = matches[text[i]]
        for j in possible[id]:
            if j not in cur_m:
                possible[id].remove(j)
        if len(possible[id]) == 0:
            return ""
        id = (id + 1) % l
    res = [possible[i][0] for i in range(l)]
    return ''.join(map(str, res))

def check(key: str, text: str) -> str:
    res = []
    id = 0
    for i in range(len(text)):
        if not text[i].isalpha():
            continue
        # print(ord(text[i]))
        if ord(text[i]) - int(key[id]) < ord('А'):
            res.append(chr(ord(text[i]) - int(key[id]) + mod))
        else:
            res.append(chr(ord(text[i]) - int(key[id])))
        id = (id + 1) % len(key)
    return ''.join(res)


freq = {
    'А': 7.64,
    'Б': 2.01,
    'В': 4.38,
    'Г': 1.72,
    'Д': 3.09,
    'Е': 8.75,
    'Ё': 0.20,
    'Ж': 1.01,
    'З': 1.48,
    'И': 7.09,
    'Й': 1.21,
    'К': 3.30,
    'Л': 4.96,
    'М': 3.17,
    'Н': 6.78,
    'О': 11.18,
    'П': 2.47,
    'Р': 4.23,
    'С': 4.97,
    'Т': 6.09,
    'У': 2.22,
    'Ф': 0.21,
    'Х': 0.95,
    'Ц': 0.39,
    'Ч': 1.40,
    'Ш': 0.72,
    'Щ': 0.30,
    'Ъ': 0.02,
    'Ы': 2.36,
    'Ь': 1.84,
    'Э': 0.36,
    'Ю': 0.47,
    'Я': 1.96
}

text = "пйозжжю кёчоцй, е ъит уёиыегфп мбшксёч иёлзтг, е хпчлйе, рг шбшсрауысц хсыдгш, шпегрллфе езб кргймбуйха. тзщгбк, цдзхдк з тйехоья сёънбб шбцф, иыо пимкодксёч сфтъа, цтсуёо, уыф, тщйсйянцб бмеры плучзрпф нзф к сщлм, а ехчсфк — члзъстшьс, рюйнгёугй, елюсётъым пчмфецй ъзфпзёт в нонуэбъом ннррё. ... йох хил о озчгоств тцвзубёуоц нзенсфаънюз, рбиблоърдё хсцифынтшгря, тсысетаиз еъя чуцллщь."
text = text.upper()

cur_freq = build_cur_freq(text)

eps = [5]
length = [i for i in range(1, 11)]

for e in eps:
    matches = build_matches(cur_freq, freq, e)
    print(f"eps = {e}", matches)
    for l in length:
        possible = [[i for i in range(0, 10)] for _ in range(l)]
        key = find_key(matches, possible, text)
        print(f"eps = {e}, length = {l}, key = {key}")
        if len(key):
            print(check(key, text))
# print(chr(ord('А')))
# print(check("01717990", text))