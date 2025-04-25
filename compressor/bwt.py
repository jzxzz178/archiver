def bwt_encode(text: str) -> tuple[str, int]:
    text += '\0'
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    rotations_sorted = sorted(rotations)
    last_column = ''.join(row[-1] for row in rotations_sorted)
    original_index = rotations_sorted.index(text)
    return last_column, original_index


def bwt_decode(bwt: str, original_index: int) -> str:
    n = len(bwt)    

    # 1) Подсчёт Occ и total_count
    total_count = {}
    occ = [0] * n
    for i, ch in enumerate(bwt):
        occ[i] = total_count.get(ch, 0)
        total_count[ch] = occ[i] + 1

    # 2) Кумаулятивные C[c]
    C = {}
    cum = 0
    for ch in sorted(total_count):
        C[ch] = cum
        cum += total_count[ch]

    # 3) Восстановление через LF-mapping
    res = []
    ptr = original_index
    for _ in range(n):
        ch = bwt[ptr]
        res.append(ch)
        ptr = C[ch] + occ[ptr]

    # 4) Собираем строку и убираем делимитер '\0'
    return ''.join(reversed(res)).rstrip('\0')
