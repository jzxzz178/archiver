from typing import List
from fractions import Fraction
import bisect

def arithmetic_encode(data: List[int]) -> bytes:
    # sumbols - по сути локальный словарь для блока символов. 
    # он нужен, так как после zle у нас могут встречаться числа (кол-ва нулей),
    # выбивающиеся из изначального словаря
    symbols = sorted(set(data))
    sym2idx = { sym: idx for idx, sym in enumerate(symbols) }

    # частоты
    freq = [0] * len(symbols)
    for x in data:
        freq[sym2idx[x]] += 1
    total = len(data)

    # кумулятивные частоты
    cdf = [0]
    for f in freq:
        cdf.append(cdf[-1] + f)

    CodeValueBits = 32
    MAX_RANGE = (1 << CodeValueBits) - 1
    Half = 1 << (CodeValueBits - 1)
    Quarter = Half >> 1

    low, high = 0, MAX_RANGE
    underflow = 0
    bits_out: List[int] = []

    def output_bit(bit: int):
        bits_out.append(bit)

    # основной цикл
    for x in data:
        idx = sym2idx[x]
        range_width = high - low + 1
        high = low + (range_width * cdf[idx+1] // total) - 1
        low  = low + (range_width * cdf[idx]   // total)

        while True:
            if high < Half:
                output_bit(0)
                for _ in range(underflow):
                    output_bit(1)
                underflow = 0
                low  <<= 1
                high = (high << 1) | 1
            elif low >= Half:
                output_bit(1)
                for _ in range(underflow):
                    output_bit(0)
                underflow = 0
                low  = (low - Half) << 1
                high = ((high - Half) << 1) | 1
            elif low >= Quarter and high < 3 * Quarter:
                underflow += 1
                low  = (low - Quarter) << 1
                high = ((high - Quarter) << 1) | 1
            else:
                break

    underflow += 1
    if low < Quarter:
        output_bit(0)
        for _ in range(underflow):
            output_bit(1)
    else:
        output_bit(1)
        for _ in range(underflow):
            output_bit(0)

    out = bytearray()
    out += len(symbols).to_bytes(4, 'big')

    for s in symbols:
        out += int(s).to_bytes(4, 'big', signed=True)

    for f in freq:
        out += f.to_bytes(4, 'big')

    bit_len = len(bits_out)
    out += bit_len.to_bytes(4, 'big')
    # выравниваем поток бит до 8
    while len(bits_out) % 8 != 0:
        bits_out.append(0)

    byte = 0
    for i, b in enumerate(bits_out):
        byte = (byte << 1) | b
        if i & 7 == 7:
            out.append(byte)
            byte = 0
    return bytes(out)


def arithmetic_decode(encoded: bytes, length: int) -> List[int]:
    offset = 0
    sym_count = int.from_bytes(encoded[offset:offset+4], 'big')
    offset += 4
    symbols = []
    for _ in range(sym_count):
        s = int.from_bytes(encoded[offset:offset+4], 'big', signed=True)
        symbols.append(s)
        offset += 4

    freq = []
    for _ in range(sym_count):
        f = int.from_bytes(encoded[offset:offset+4], 'big')
        freq.append(f)
        offset += 4
    total = sum(freq)

    cdf = [0]
    for f in freq:
        cdf.append(cdf[-1] + f)

    bit_len = int.from_bytes(encoded[offset:offset+4], 'big')
    offset += 4

    data_bytes = encoded[offset:]
    byte_pos = 0
    bit_offset = 0
    bit_count = 0  # сколько уже прочитано бит
    def read_bit() -> int:
        nonlocal byte_pos, bit_offset, bit_count

        if bit_count >= bit_len:
            bit_count += 1
            return 0

        if byte_pos < len(data_bytes):
            b = (data_bytes[byte_pos] >> (7 - bit_offset)) & 1
        else:
            b = 0
        bit_offset += 1
        bit_count += 1
        if bit_offset == 8:
            bit_offset = 0
            byte_pos += 1
        return b

    CodeValueBits = 32
    MAX_RANGE = (1 << CodeValueBits) - 1
    Half = 1 << (CodeValueBits - 1)
    Quarter = Half >> 1

    code_value = 0
    for _ in range(CodeValueBits):
        code_value = (code_value << 1) | read_bit()

    low, high = 0, MAX_RANGE
    result: List[int] = []

    # основной цикл
    for _ in range(length):
        range_width = high - low + 1
        value = ((code_value - low + 1) * total - 1) // range_width

        j = bisect.bisect_right(cdf, value) - 1
        result.append(symbols[j])

        high = low + (range_width * cdf[j+1] // total) - 1
        low  = low + (range_width * cdf[j]   // total)

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
            code_value = (code_value << 1) | read_bit()

    return result