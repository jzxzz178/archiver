import argparse
import json
import base64
import os
from pathlib import Path
import time
from typing import List

from compressor.bwt import bwt_encode, bwt_decode
from compressor.mtf import mtf_encode, mtf_decode
from compressor.zle import zle_encode, zle_decode
from compressor.ari import arithmetic_encode, arithmetic_decode

BLOCK_SIZE = 1024 * 1024 # 1MB

def get_alphabet_from_text(text: str) -> List[str]:
    unique_chars = sorted(set(text))
    unique_chars.append('\0')
    # print(f"алфавит: {len(unique_chars)} символов")
    return unique_chars


def compress_file(input_path: str, output_path: str, block_size: int = BLOCK_SIZE):
    text = Path(input_path).read_text(encoding="utf-8")
    alphabet = get_alphabet_from_text(text)
    zle_marker = len(alphabet)
    blocks = []
    
    bwt_times = []
    mtf_times = []
    zle_times = []
    ari_times = []
    
    for i in range(0, len(text), block_size):
        block = text[i:i + block_size]
        
        t1 = time.time()
        bwt_out, bwt_index = bwt_encode(block)
        bwt_times.append(time.time() - t1)
        
        t2 = time.time()
        mtf_out = mtf_encode(bwt_out, alphabet)
        mtf_times.append(time.time() - t2)
        
        t3 = time.time()
        zle_out = zle_encode(mtf_out, marker=zle_marker)
        zle_times.append(time.time() - t3)
        
        t4 = time.time()
        code_bytes = arithmetic_encode(zle_out)
        ari_times.append(time.time() - t4)
        
        code_b64 = base64.b64encode(code_bytes).decode('ascii')
        blocks.append({
            "code": code_b64,
            "length": len(zle_out),
            "bwt_index": bwt_index
        })

    print(f"\033[34mСреднее время BWT кодирования: {sum(bwt_times)/len(bwt_times):.3f} сек.\033[0m")
    print(f"\033[34mСреднее время MTF кодирования: {sum(mtf_times)/len(mtf_times):.3f} сек.\033[0m")
    print(f"\033[34mСреднее время ZLE кодирования: {sum(zle_times)/len(zle_times):.3f} сек.\033[0m")
    print(f"\033[34mСреднее время арифметического кодирования: {sum(ari_times)/len(ari_times):.3f} сек.\033[0m")

    result = {
        "alphabet": [ord(c) for c in alphabet],
        "marker": zle_marker,
        "blocks": blocks
    }
    Path(output_path).write_text(json.dumps(result), encoding="utf-8")
    compressed_size = os.path.getsize(output_path) >> 10
    print(f"\033[32mСжатие завершено. Результат сохранён в {output_path}\033[0m")
    print(f"\033[33mРазмер сжатого файла: {compressed_size} KB\033[0m")


def decompress_file(input_path: str, output_path: str):
    archive = json.loads(Path(input_path).read_text(encoding="utf-8"))
    alphabet = [chr(c) for c in archive["alphabet"]]
    zle_marker = archive["marker"]
    text_out = []

    ari_times = []
    zle_times = []
    mtf_times = []
    bwt_times = []

    for block in archive["blocks"]:
        code_bytes = base64.b64decode(block["code"])
        length = block["length"]
        bwt_index = block["bwt_index"]

        t1 = time.time()
        zle_out = arithmetic_decode(code_bytes, length)
        ari_times.append(time.time() - t1)

        t2 = time.time()
        zle_decoded = zle_decode(zle_out, marker=zle_marker)
        zle_times.append(time.time() - t2)

        t3 = time.time()
        mtf_decoded = mtf_decode(zle_decoded, alphabet)
        mtf_times.append(time.time() - t3)

        t4 = time.time()
        text_out.append(bwt_decode(mtf_decoded, bwt_index))
        bwt_times.append(time.time() - t4)

    print(f"\033[34mСреднее время арифметического декодирования: {sum(ari_times)/len(ari_times):.3f} сек.\033[0m")
    print(f"\033[34mСреднее время ZLE декодирования: {sum(zle_times)/len(zle_times):.3f} сек.\033[0m")
    print(f"\033[34mСреднее время MTF декодирования: {sum(mtf_times)/len(mtf_times):.3f} сек.\033[0m")
    print(f"\033[34mСреднее время BWT декодирования: {sum(bwt_times)/len(bwt_times):.3f} сек.\033[0m")

    Path(output_path).write_text("".join(text_out), encoding="utf-8")
    print(f"\033[32mДекодирование завершено. Восстановленный текст записан в {output_path}\033[0m")


def main():
    parser = argparse.ArgumentParser(description="CLI архиватор на основе BWT + MTF + ZLE + ARI")
    parser.add_argument("mode", choices=["compress", "decompress"], help="Режим: compress или decompress")
    parser.add_argument("input", help="Путь к входному файлу")
    parser.add_argument("output", help="Путь к выходному файлу")
    args = parser.parse_args()

    start_time = time.time()
    if args.mode == "compress":
        compress_file(args.input, args.output)
    else:
        decompress_file(args.input, args.output)
    end_time = time.time()
    print(f"\033[34mВремя выполнения: {end_time - start_time:.2f} сек.\033[0m")


if __name__ == "__main__":
    main()
