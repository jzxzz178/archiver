import argparse
import json
from pathlib import Path
from compressor.ari import ArithmeticCoder
from compressor.bwt import bwt_encode, bwt_decode
from compressor.mtf import mtf_encode, mtf_decode
from compressor.zle import zle_encode, zle_decode

BLOCK_SIZE = 4096
ALPHABET = list("!#()*,-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz \n\0")
ZLE_MARKER = len(ALPHABET)


def compress_file(input_path: str, output_path: str):
    text = Path(input_path).read_text(encoding="utf-8")
    blocks = []
    for i in range(0, len(text), BLOCK_SIZE):
        block = text[i:i + BLOCK_SIZE]
        bwt_out, bwt_index = bwt_encode(block)
        mtf_out = mtf_encode(bwt_out, ALPHABET)
        zle_out = zle_encode(mtf_out, marker=ZLE_MARKER)
        coder = ArithmeticCoder(zle_out)
        code = str(coder.encode())
        blocks.append({
            "code": code,
            "length": len(zle_out),
            "bwt_index": bwt_index
        })

    result = {
        "alphabet": [ord(c) for c in ALPHABET],
        "marker": ZLE_MARKER,
        "blocks": blocks
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f)
    print(f"✅ Сжатие завершено. Результат сохранён в {output_path}")


def decompress_file(input_path: str, output_path: str):
    with open(input_path, "r", encoding="utf-8") as f:
        archive = json.load(f)

    alphabet = [chr(c) for c in archive["alphabet"]]
    marker = archive["marker"]
    text_out = []

    for block in archive["blocks"]:
        code = block["code"]
        length = block["length"]
        bwt_index = block["bwt_index"]
        coder = ArithmeticCoder([])
        coder.freq = {i: 1 for i in range(marker + 1)}
        coder.total = sum(coder.freq.values())
        coder.symbols = sorted(coder.freq.keys())
        coder.cumulative = coder._build_cumulative()
        zle_out = coder.decode(code, length)
        mtf_decoded = mtf_decode(zle_decode(zle_out, marker=marker), alphabet)
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
    elif args.mode == "decompress":
        decompress_file(args.input, args.output)


if __name__ == "__main__":
    main()
