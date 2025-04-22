def bwt_encode(text: str) -> tuple[str, int]:
    """Преобразует строку text с помощью BWT и возвращает
    (BWT-строку, индекс исходной строки в отсортированной матрице)"""
    text += '\0'
    rotations = [text[i:] + text[:i] for i in range(len(text))]
    rotations_sorted = sorted(rotations)
    last_column = ''.join(row[-1] for row in rotations_sorted)
    original_index = rotations_sorted.index(text)
    return last_column, original_index


def bwt_decode(bwt: str, index: int) -> str:
    """Восстанавливает строку из BWT и индекса"""
    n = len(bwt)
    table = [''] * n
    for _ in range(n):
        table = sorted(bwt[i] + table[i] for i in range(n))
    result = table[index]
    return result.rstrip('\0')
