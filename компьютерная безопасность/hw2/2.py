# -*- coding: utf-8 -*-
import math
import re
from collections import Counter, defaultdict

# Русский алфавит (33 буквы, с ё)
ALPH = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
A2I = {ch:i for i,ch in enumerate(ALPH)}
I2A = {i:ch for i,ch in enumerate(ALPH)}
N = len(ALPH)  # 33

# Частоты русских букв (примерно; можете уточнить при желании)
# Нормализованные частоты; важно, чтобы сумма ~1
RU_FREQ = {
    'о':0.1097, 'е':0.0845, 'а':0.0801, 'и':0.0735, 'н':0.0670, 'т':0.0626, 'с':0.0547,
    'р':0.0473, 'в':0.0454, 'л':0.0440, 'к':0.0349, 'м':0.0321, 'д':0.0298, 'п':0.0281,
    'у':0.0262, 'я':0.0201, 'ы':0.0190, 'ь':0.0174, 'г':0.0169, 'з':0.0165, 'б':0.0159,
    'ч':0.0144, 'й':0.0121, 'х':0.0097, 'ж':0.0094, 'ш':0.0073, 'ю':0.0065, 'ц':0.0048,
    'щ':0.0036, 'э':0.0032, 'ф':0.0026, 'ё':0.0004
}

def clean_text(txt):
    # Оставляем только русские буквы в нижнем регистре
    txt = txt.lower()
    txt_letters = re.findall(r"[а-яё]", txt)
    return "".join(txt_letters)

def index_of_coincidence(s):
    if not s: return 0.0
    c = Counter(s)
    n = len(s)
    num = sum(v*(v-1) for v in c.values())
    den = n*(n-1)
    return num/den if den else 0.0

def split_by_keylen(s, keylen):
    cols = [ [] for _ in range(keylen) ]
    for i,ch in enumerate(s):
        cols[i % keylen].append(ch)
    return [ "".join(col) for col in cols ]

def shift_char(ch, k):
    # Расшифровка: p = (c - k) mod N
    return I2A[(A2I[ch] - k) % N]

def score_by_freq(decoded_col):
    # лог-правдоподобие по униграммам
    c = Counter(decoded_col)
    n = len(decoded_col)
    if n == 0: return -1e9
    score = 0.0
    for ch, cnt in c.items():
        p = RU_FREQ.get(ch, 1e-6)
        # многократно сложим лог(p) по количеству появлений
        score += cnt * math.log(p)
    return score

def best_digit_for_column(col):
    # Подбираем k из 0..9, который дает лучший скор
    best_k, best_score = None, -1e18
    for k in range(10):
        decoded = "".join(shift_char(ch, k) for ch in col)
        sc = score_by_freq(decoded)
        if sc > best_score:
            best_score = sc
            best_k = k
    return best_k, best_score

def guess_key_length(s, min_k=1, max_k=20):
    # Оценим IC для разных длин и выберем несколько лучших
    candidates = []
    for klen in range(min_k, max_k+1):
        cols = split_by_keylen(s, klen)
        ic_vals = [ index_of_coincidence(col) for col in cols ]
        avg_ic = sum(ic_vals)/len(ic_vals)
        candidates.append((klen, avg_ic))
    # Отсортируем по близости к русскому IC
    candidates.sort(key=lambda x: abs(x[1]-0.060))  # 0.06 как целевой
    return candidates[:5]  # вернем топ-5 длин

def recover_key_and_plain(s, keylen):
    cols = split_by_keylen(s, keylen)
    digits = []
    for col in cols:
        k, _ = best_digit_for_column(col)
        digits.append(k)
    # Теперь расшифруем весь текст
    plain_letters = []
    for i,ch in enumerate(s):
        k = digits[i % keylen]
        plain_letters.append(shift_char(ch, k))
    return digits, "".join(plain_letters)

def restore_punctuation(original, plain_letters):
    # Вернем пунктуацию/пробелы на места: plain_letters дают буквы по порядку
    res = []
    i = 0
    for ch in original:
        if re.match(r"[А-Яа-яЁё]", ch):
            res.append(plain_letters[i])
            i += 1
        else:
            res.append(ch)  # оставляем символ как есть
    return "".join(res)

if __name__ == "__main__":
    CIPH = """пйозжжю кёчоцй, е ъит уёиыегфп мбшксёч иёлзтг, е хпчлйе, рг шбшсрауысц хсыдгш, шпегрллфе езб кргймбуйха. тзщгбк, цдзхдк з тйехоья сёънбб шбцф, иыо пимкодксёч сфтъа, цтсуёо, уыф, тщйсйянцб бмеры плучзрпф нзф к сщлм, а ехчсфк — члзъстшьс, рюйнгёугй, елюсётъым пчмфецй ъзфпзёт в нонуэбъом ннррё. ... йох хил о озчгоств тцвзубёуоц нзенсфаънюз, рбиблоърдё хсцифынтшгря, тсысетаиз еъя чуцллщь."""
    cleaned = clean_text(CIPH)
    print("Длина очищенного текста:", len(cleaned))
    klen_candidates = guess_key_length(cleaned, 1, 20)
    print("Кандидаты длины ключа (klen, avgIC):", klen_candidates)
    # Возьмем лучший кандидат
    best_klen = 9
    digits, plain_letters = recover_key_and_plain(cleaned, best_klen)
    key_str = "".join(str(d) for d in digits)
    print("Предполагаемая длина ключа:", best_klen)
    print("Ключ (цифры):", key_str)
    # Вернем пунктуацию
    full_plain = restore_punctuation(CIPH, plain_letters)
    print("\nРасшифрованный текст:\n", full_plain)