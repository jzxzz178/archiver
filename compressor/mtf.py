def mtf_encode(text: str, alphabet: list) -> list[int]:
    table = alphabet.copy()
    output = []
    for ch in text:
        idx = table.index(ch)
        output.append(idx)
        table.insert(0, table.pop(idx))
    return output


def mtf_decode(indices: list[int], alphabet: list) -> str:
    table = alphabet.copy()
    output = []
    for idx in indices:
        ch = table[idx]
        output.append(ch)
        table.insert(0, table.pop(idx))
    return ''.join(output)
