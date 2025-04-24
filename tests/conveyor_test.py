from pathlib import Path
from compressor.bwt import bwt_encode, bwt_decode
from compressor.mtf import mtf_encode, mtf_decode
from compressor.zle import zle_encode, zle_decode
from compressor.ari import arithmetic_encode, arithmetic_decode

def test_full_pipeline():
    text = Path("tests/test.txt").read_text(encoding="utf-8")

    alphabet = sorted(set(text))
    alphabet.append('\0')
    # alphabet = ''.join(alphabet)
    zle_marker = len(alphabet)

    print(f'alphabet: {alphabet}')
    print(f'zle_marker: {zle_marker}')

    # Прямое преобразование
    bwt_out, bwt_index = bwt_encode(text)
    mtf_out = mtf_encode(bwt_out, alphabet)
    zle_out = zle_encode(mtf_out, marker=zle_marker)
    encoded = arithmetic_encode(zle_out, zle_marker)

    print(f'encoded: {encoded}')

    # Обратное преобразование
    decoded = arithmetic_decode(encoded, len(zle_out), zle_marker)
    mtf_decoded = mtf_decode(zle_decode(decoded, marker=zle_marker), alphabet)
    text_out = bwt_decode(mtf_decoded, bwt_index)

    print(f'text_out: {text_out}')

    assert text == text_out, "Ошибка в пайплайне сжатия"
    print("\033[32mПайплайн сжатия прошел успешно\033[0m")