# -*- coding: utf-8 -*-
import re
from collections import Counter
import math

# Русский алфавит с ё
ALPH = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
A2I = {ch:i for i,ch in enumerate(ALPH)}
I2A = {i:ch for i,ch in enumerate(ALPH)}
N = len(ALPH)

# Частоты русских букв (приблизительно; сумма ~1)
RU_FREQ = {
    'о':0.1097, 'е':0.0845, 'а':0.0801, 'и':0.0735, 'н':0.0670, 'т':0.0626, 'с':0.0547,
    'р':0.0473, 'в':0.0454, 'л':0.0440, 'к':0.0349, 'м':0.0321, 'д':0.0298, 'п':0.0281,
    'у':0.0262, 'я':0.0201, 'ы':0.0190, 'ь':0.0174, 'г':0.0169, 'з':0.0165, 'б':0.0159,
    'ч':0.0144, 'й':0.0121, 'х':0.0097, 'ж':0.0094, 'ш':0.0073, 'ю':0.0065, 'ц':0.0048,
    'щ':0.0036, 'э':0.0032, 'ф':0.0026, 'ё':0.0004,
}
# Если какая-то буква выпала — дадим ей маленькую вероятность
DEF_P = 1e-6

CIPH = """ъ угюеж шочйеп, р рэтэшщьк, щксжк ц фудйтф ьжбо, сщеам дхбжыблщчвщр-маибфтамщй янахцпщй ьчеяск ъоьюгфчн х пэыщбпхыгл. йпьэ фкк йдея ч фюмшцвя, ёфщ ншъэьв тксйкщьэ. пк оьцгъ чй ъойфщфька скивжчл мзжбщь р дкгжц бяъроов ащьэдпк, еиая цвчепищэйл ьрэмэ фяхнин шфвавсиичц, щ а спръччя рйнлчмф аярузъчшщръуй ъшщзофцеёсщ сэнжнжлг. ьчшщ еыч хлър шежйпзолшо щнаяу, чюджн, ё юутпшбыщькпёмб ащббвчи, ъдерхвмшбхэ въвлойыр щ трлржмзичж."""

def only_letters(txt):
    return "".join(ch for ch in txt.lower() if ch in A2I)

def split_by_keylen(s, L):
    cols = ['' for _ in range(L)]
    for i,ch in enumerate(s):
        cols[i % L] += ch
    return cols

def index_of_coincidence(s):
    if len(s) < 2: return 0.0
    c = Counter(s)
    n = len(s)
    num = sum(v*(v-1) for v in c.values())
    den = n*(n-1)
    return num/den

def avg_ic_for_len(s, L):
    cols = split_by_keylen(s, L)
    ics = [index_of_coincidence(col) for col in cols if len(col) > 1]
    return sum(ics)/len(ics) if ics else 0.0

def chi2_stat(col_shifted_counts, total):
    # χ² между наблюдаемыми частотами и эталонными RU_FREQ
    chi2 = 0.0
    for ch, p in RU_FREQ.items():
        exp = total * p
        obs = col_shifted_counts.get(ch, 0)
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp
    # штраф за буквы вне RU_FREQ (теоретически не должно быть)
    for ch, obs in col_shifted_counts.items():
        if ch not in RU_FREQ:
            exp = total * DEF_P
            chi2 += (obs - exp) ** 2 / max(exp, 1e-9)
    return chi2

def best_shift_for_column(col):
    # Перебираем сдвиг s: p = (c - s) mod N, выбираем s с минимальным χ²
    counts_by_shift = []
    total = len(col)
    idxs = [A2I[ch] for ch in col]
    best_s, best_val = None, 1e99
    for s in range(N):
        cnt = Counter(I2A[(i - s) % N] for i in idxs)
        val = chi2_stat(cnt, total)
        if val < best_val:
            best_val = val
            best_s = s
    return best_s, best_val

def recover_key(s, max_L=24, top=5):
    # Кандидаты по IC
    ic_list = [(L, avg_ic_for_len(s, L)) for L in range(1, max_L+1)]
    # Для русского IC ~ 0.055–0.065. Сортируем по близости.
    ic_list.sort(key=lambda x: abs(x[1]-0.060))
    candidates = ic_list[:top]

    best = None
    for L, icv in candidates:
        cols = split_by_keylen(s, L)
        shifts = []
        chi_sum = 0.0
        for col in cols:
            sft, chi = best_shift_for_column(col)
            shifts.append(sft)
            chi_sum += chi
        # Чем меньше chi_sum, тем лучше
        key = "".join(I2A[s] for s in shifts)
        if best is None or chi_sum < best[0]:
            best = (chi_sum, L, key, shifts)
    return best

def decrypt_full(text, shifts):
    out = []
    j = 0
    for ch in text.lower():
        if ch in A2I:
            c = A2I[ch]
            s = shifts[j % len(shifts)]
            p = (c - s) % N
            out.append(I2A[p])
            j += 1
        else:
            out.append(ch)
    return "".join(out)

if __name__ == "__main__":
    cleaned = only_letters(CIPH)
    chi_sum, L, key, shifts = recover_key(cleaned, max_L=24, top=8)
    print("Предполагаемая длина ключа:", L)
    print("Ключ (буквы):", key)
    plain = decrypt_full(CIPH, shifts)
    print("\nРасшифрованный текст (фрагмент):\n")
    print(plain)