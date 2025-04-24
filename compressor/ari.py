from typing import List
from fractions import Fraction

def arithmetic_encode(data: List[int], max_symbol: int) -> bytes:
    """
    Арифметическое кодирование списка целых чисел 0..78.
    Возвращает сжатую последовательность байтов, включающую статическую модель (частоты) и код.
    """
    # Построение статической модели: частоты символов
    MAX_SYMBOL = max_symbol
    freq = [0] * (MAX_SYMBOL + 1)
    for x in data:
        freq[x] += 1
    total = len(data)
    # Если нет данных, возвращаем пустой результат
    if total == 0:
        return bytes()
    # Кумулятивные частоты (cdf[i] = сумма freq[0..i-1])
    cdf = [0] * (len(freq) + 1)
    for i in range(len(freq)):
        cdf[i+1] = cdf[i] + freq[i]

    # Параметры арифметического кодера с фиксированной точностью (32 бита)
    CodeValueBits = 32
    MAX_RANGE = (1 << CodeValueBits) - 1
    Half = 1 << (CodeValueBits - 1)
    Quarter = Half >> 1

    low = 0
    high = MAX_RANGE
    underflow = 0
    bits_out = []

    # Функция для вывода одного бита и всех накопленных «отложенных» битов
    def output_bit(bit: int):
        bits_out.append(bit)

    # Основной цикл: обрабатываем каждый символ из data
    for symbol in data:
        # Текущее «ширина» диапазона + уточнение подинтервала для symbol
        range_width = high - low + 1
        high = low + (range_width * cdf[symbol+1] // total) - 1
        low  = low + (range_width * cdf[symbol]   // total)
        # Нормализация: проверяем совпадающие старшие биты
        while True:
            # Если MSB у low и high = 0 (попадают в первый четверть)
            if high < Half:
                output_bit(0)
                # Выводим все «отложенные» биты как единицы
                for _ in range(underflow):
                    output_bit(1)
                underflow = 0
                low  = low * 2
                high = high * 2 + 1
            # Если MSB = 1 (попадают во вторую половину)
            elif low >= Half:
                output_bit(1)
                for _ in range(underflow):
                    output_bit(0)
                underflow = 0
                low  = (low - Half) * 2
                high = (high - Half) * 2 + 1
            # Случай «переноса» (E3): low/ high попадают в среднюю половину [1/4..3/4)
            elif low >= Quarter and high < 3 * Quarter:
                underflow += 1
                low  = (low - Quarter) * 2
                high = (high - Quarter) * 2 + 1
            else:
                break

    # После обработки всех символов добавляем завершающий бит
    underflow += 1
    if low < Quarter:
        output_bit(0)
        for _ in range(underflow):
            output_bit(1)
    else:
        output_bit(1)
        for _ in range(underflow):
            output_bit(0)

    # Собираем результат: сначала частоты (по 4 байта на частоту), затем длину битового кода и сами биты
    out = bytearray()
    for count in freq:
        out += count.to_bytes(4, 'big')
    bit_len = len(bits_out)
    out += bit_len.to_bytes(4, 'big')
    # Добавляем биты, упакованные в байты (MSB первого бита)
    # Дополним до кратности 8 нулями (размер файла может быть больше, важна длина бит)
    while len(bits_out) % 8 != 0:
        bits_out.append(0)
    byte = 0
    for i, b in enumerate(bits_out):
        byte = (byte << 1) | b
        if (i % 8) == 7:
            out.append(byte)
            byte = 0
    return bytes(out)

def arithmetic_decode(encoded: bytes, length: int) -> List[int]:
    """
    Декодирование байтового представления, возвращает исходный список int той же длины.
    Предполагается, что в encoded сохранены частоты (статическая модель) и закодированные биты.
    """
    if length == 0:
        return []
    MAX_SYMBOL = 78
    offset = 0
    # Читаем частоты (модель)
    freq = []
    for _ in range(MAX_SYMBOL + 1):
        freq.append(int.from_bytes(encoded[offset:offset+4], 'big'))
        offset += 4
    total = sum(freq)
    # Кумулятивные частоты
    cdf = [0] * (len(freq) + 1)
    for i in range(len(freq)):
        cdf[i+1] = cdf[i] + freq[i]
    # Длина кодовых бит
    bit_len = int.from_bytes(encoded[offset:offset+4], 'big')
    offset += 4
    # Извлекаем сам поток бит
    bits = []
    for b in encoded[offset:]:
        for i in range(8):
            bits.append((b >> (7 - i)) & 1)
    bits = bits[:bit_len]  # обрезаем по реальной длине

    CodeValueBits = 32
    MAX_RANGE = (1 << CodeValueBits) - 1
    Half = 1 << (CodeValueBits - 1)
    Quarter = Half >> 1

    # Инициализация «кода» из первых 32 бит
    code_value = 0
    bit_pos = 0
    for _ in range(CodeValueBits):
        code_value = (code_value << 1) | (bits[bit_pos] if bit_pos < bit_len else 0)
        bit_pos += 1

    low = 0
    high = MAX_RANGE
    result = []

    # Декодируем symbols = length
    for _ in range(length):
        range_width = high - low + 1
        # Определяем «value» для поиска символа
        value = ((code_value - low + 1) * total - 1) // range_width
        # Находим символ s такой, что cdf[s] <= value < cdf[s+1]
        symbol = 0
        for s in range(len(freq)):
            if freq[s] > 0 and cdf[s] <= value < cdf[s+1]:
                symbol = s
                break
        result.append(symbol)
        # Уточняем границы по найденному символу
        high = low + (range_width * cdf[symbol+1] // total) - 1
        low  = low + (range_width * cdf[symbol]   // total)
        # Нормализация: аналогична кодеру (сдвиг и чтение следующих битов)
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
            low  = low * 2
            high = high * 2 + 1
            # Сдвигаем следующий бит в code_value
            next_bit = bits[bit_pos] if bit_pos < bit_len else 0
            code_value = (code_value << 1) | next_bit
            bit_pos += 1

    return result
