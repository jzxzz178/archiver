import argparse
import json
import base64
from pathlib import Path
from typing import List

from compressor.bwt import bwt_encode, bwt_decode
from compressor.mtf import mtf_encode, mtf_decode
from compressor.zle import zle_encode, zle_decode
from compressor.ari import arithmetic_encode, arithmetic_decode

BLOCK_SIZE = 4096
def get_alphabet_from_text(text: str) -> List[str]:
    unique_chars = sorted(set(text))
    unique_chars.append('\0')
    return unique_chars


def compress_file(input_path: str, output_path: str):
    text = Path(input_path).read_text(encoding="utf-8")
    alphabet = get_alphabet_from_text(text)
    zle_marker = len(alphabet)
    blocks = []
    for i in range(0, len(text), BLOCK_SIZE):
        block = text[i:i + BLOCK_SIZE]
        bwt_out, bwt_index = bwt_encode(block)
        mtf_out = mtf_encode(bwt_out, alphabet)
        zle_out = zle_encode(mtf_out, marker=zle_marker)
        code_bytes = arithmetic_encode(zle_out, zle_marker)
        code_b64 = base64.b64encode(code_bytes).decode('ascii')
        blocks.append({
            "code": code_b64,
            "length": len(zle_out),
            "bwt_index": bwt_index
        })

    result = {
        "alphabet": [ord(c) for c in alphabet],
        "marker": zle_marker,
        "blocks": blocks
    }
    Path(output_path).write_text(json.dumps(result), encoding="utf-8")
    print(f"✅ Сжатие завершено. Результат сохранён в {output_path}")


def decompress_file(input_path: str, output_path: str):
    archive = json.loads(Path(input_path).read_text(encoding="utf-8"))
    alphabet = [chr(c) for c in archive["alphabet"]]
    zle_marker = archive["marker"]
    text_out = []

    for block in archive["blocks"]:
        code_bytes = base64.b64decode(block["code"])
        length = block["length"]
        bwt_index = block["bwt_index"]

        zle_out = arithmetic_decode(code_bytes, length, zle_marker)
        mtf_decoded = mtf_decode(zle_decode(zle_out, marker=zle_marker), alphabet)
        text_out.append(bwt_decode(mtf_decoded, bwt_index))

    Path(output_path).write_text("".join(text_out), encoding="utf-8")
    print(f"✅ Декодирование завершено. Восстановленный текст записан в {output_path}")


def main():
    parser = argparse.ArgumentParser(description="CLI архиватор на основе BWT + MTF + ZLE + ARI")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Режим: compress или decompress")
    parser.add_argument("input", help="Путь к входному файлу")
    parser.add_argument("output", help="Путь к выходному файлу")
    args = parser.parse_args()

    if args.mode == "compress":
        compress_file(args.input, args.output)
    else:
        decompress_file(args.input, args.output)


if __name__ == "__main__":
    main()
