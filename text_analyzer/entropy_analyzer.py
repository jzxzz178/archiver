import math
from collections import Counter

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

for B in block_sizes:
    entropies = []
    for i in range(0, len(text), B):
        block = text[i:i+B]
        entropies.append(block_entropy(block))
    avg_H = sum(entropies) / len(entropies)
    results.append((B, avg_H))

print("Размер блока (KB)  Средн. энтропия")
for B, H in results:
    print(f"{B>>10:6d} KB           {H:.4f} бит/симв")



