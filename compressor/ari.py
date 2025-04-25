from typing import List

# === Арифметическое кодирование с динамическим алфавитом ===

def arithmetic_encode(data: List[int]) -> bytes:
    """
    Кодируем список целых чисел (включая маркер и длины пробегов) с динамическим алфавитом.
    Возвращает байты: сериализованные symbols, freq, bit_len и битовый поток.
    """
    # 1. Выделяем уникальные символы и строим карту "символ -> индекс"
    symbols = sorted(set(data))
    sym2idx = { sym: idx for idx, sym in enumerate(symbols) }

    # 2. Считаем частоты по индексам
    freq = [0] * len(symbols)
    for x in data:
        freq[sym2idx[x]] += 1
    total = len(data)

    # 3. Строим кумулятивные частоты
    cdf = [0]
    for f in freq:
        cdf.append(cdf[-1] + f)

    # 4. Параметры кодера (32-битный диапазон)
    CodeValueBits = 32
    MAX_RANGE = (1 << CodeValueBits) - 1
    Half = 1 << (CodeValueBits - 1)
    Quarter = Half >> 1

    low, high = 0, MAX_RANGE
    underflow = 0
    bits_out: List[int] = []

    def output_bit(bit: int):
        bits_out.append(bit)

    # 5. Основной цикл кодирования по индексам
    for x in data:
        idx = sym2idx[x]
        range_width = high - low + 1
        high = low + (range_width * cdf[idx+1] // total) - 1
        low  = low + (range_width * cdf[idx]   // total)

        # нормализация
        while True:
            if high < Half:
                output_bit(0)
                for _ in range(underflow): output_bit(1)
                underflow = 0
                low  <<= 1
                high = (high << 1) | 1
            elif low >= Half:
                output_bit(1)
                for _ in range(underflow): output_bit(0)
                underflow = 0
                low  = (low - Half) << 1
                high = ((high - Half) << 1) | 1
            elif low >= Quarter and high < 3 * Quarter:
                underflow += 1
                low  = (low - Quarter) << 1
                high = ((high - Quarter) << 1) | 1
            else:
                break

    # 6. Завершающие биты
    underflow += 1
    if low < Quarter:
        output_bit(0)
        for _ in range(underflow): output_bit(1)
    else:
        output_bit(1)
        for _ in range(underflow): output_bit(0)

    # 7. Сериализация: symbols, freq, bit_len и биты
    out = bytearray()
    # a) Сохраняем symbols (каждый как 4-байтное целое)
    out += len(symbols).to_bytes(4, 'big')
    for s in symbols:
        out += int(s).to_bytes(4, 'big', signed=True)
    # b) Сохраняем частоты
    for f in freq:
        out += f.to_bytes(4, 'big')
    # c) Длина битового потока
    bit_len = len(bits_out)
    out += bit_len.to_bytes(4, 'big')
    # d) Выравниваем поток бит до 8
    while len(bits_out) % 8 != 0:
        bits_out.append(0)
    # e) Упаковываем биты в байты
    byte = 0
    for i, b in enumerate(bits_out):
        byte = (byte << 1) | b
        if i & 7 == 7:
            out.append(byte)
            byte = 0
    return bytes(out)


def arithmetic_decode(encoded: bytes, length: int) -> List[int]:
    """
    Декодируем байтовое представление ARI с динамическим алфавитом.
    length — количество символов в исходном zle_out.
    """
    # 1. Читаем symbols
    offset = 0
    sym_count = int.from_bytes(encoded[offset:offset+4], 'big')
    offset += 4
    symbols = []
    for _ in range(sym_count):
        s = int.from_bytes(encoded[offset:offset+4], 'big', signed=True)
        symbols.append(s)
        offset += 4
    # 2. Читаем freq
    freq = []
    for _ in range(sym_count):
        f = int.from_bytes(encoded[offset:offset+4], 'big')
        freq.append(f)
        offset += 4
    total = sum(freq)
    # 3. Строим cdf
    cdf = [0]
    for f in freq:
        cdf.append(cdf[-1] + f)
    # 4. Длина битового потока
    bit_len = int.from_bytes(encoded[offset:offset+4], 'big')
    offset += 4
    # 5. Извлекаем биты
    bits = []
    for b in encoded[offset:]:
        for i in range(8):
            bits.append((b >> (7-i)) & 1)
    bits = bits[:bit_len]

    # Параметры (32 бита)
    CodeValueBits = 32
    MAX_RANGE = (1 << CodeValueBits) - 1
    Half = 1 << (CodeValueBits - 1)
    Quarter = Half >> 1

    # 6. Инициализация code_value
    code_value = 0
    bit_pos = 0
    for _ in range(CodeValueBits):
        code_value = (code_value << 1) | (bits[bit_pos] if bit_pos < bit_len else 0)
        bit_pos += 1

    low, high = 0, MAX_RANGE
    result: List[int] = []

    # 7. Основной цикл декодирования
    for _ in range(length):
        range_width = high - low + 1
        value = ((code_value - low + 1) * total - 1) // range_width
        # поиск индекса j
        j = next(i for i in range(len(freq)) if cdf[i] <= value < cdf[i+1])
        result.append(symbols[j])
        # уточнение интервала
        high = low + (range_width * cdf[j+1] // total) - 1
        low  = low + (range_width * cdf[j]   // total)
        # нормализация
        while True:
            if high < Half:
                pass
            elif low >= Half:
                code_value -= Half
                low  -= Half
                high -= Half
            elif low >= Quarter and high < 3*Quarter:
                code_value -= Quarter
                low  -= Quarter
                high -= Quarter
            else:
                break
            low  <<= 1
            high = (high << 1) | 1
            next_bit = bits[bit_pos] if bit_pos < bit_len else 0
            code_value = (code_value << 1) | next_bit
            bit_pos += 1

    return result
