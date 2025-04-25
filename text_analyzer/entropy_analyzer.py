import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import math
from collections import Counter
from pathlib import Path

from main import compress_file

def block_entropy(data: bytes) -> float:
    N = len(data)
    freq = Counter(data)
    H = 0.0
    for cnt in freq.values():
        p = cnt / N
        H -= p * math.log2(p)
    return H


block_sizes = [2<<10, 4<<10, 8<<10, 16<<10, 32<<10, 64<<10, 128<<10, 256<<10, 512<<10, 1<<20]
results = []

with open('text_analyzer/Crime and Punishment by Fyodor Dostoyevsky 2.txt', 'rb') as f:
    text = f.read()

with open('text_analyzer/analysis_results.txt', 'w', encoding='utf-8') as out:
    for B in block_sizes:
        entropies = []
        for i in range(0, len(text), B):
            block = text[i:i+B]
            entropies.append(block_entropy(block))
        avg_H = sum(entropies) / len(entropies)
        results.append((B, avg_H))

    out.write("Размер блока (KB)  Средн. энтропия\n")
    for B, H in results:
        out.write(f"{B>>10:6d} KB           {H:.4f} бит/симв\n")

    for B, H in results:    
        out.write("\nРазмер блока (KB)  Размер сжатого файла (KB)\n")
        input_file = 'text_analyzer/Crime and Punishment by Fyodor Dostoyevsky 2.txt'
        output_file = f'compressed_{B>>10}kb.json'
        
        t1 = time.time()
        compress_file(input_file, output_file, B)
        compression_time = time.time() - t1
        out.write(f"Время сжатия: {compression_time:.3f} сек.\n")
        compressed_size = os.path.getsize(output_file) >> 10
        
        out.write(f"{B>>10:6d} KB           {compressed_size:6d} KB\n")
        
        Path(output_file).unlink()

