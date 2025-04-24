
def zle_encode(data: list[int], marker: int) -> list[int]:
    output = []
    i = 0
    while i < len(data):
        if data[i] == 0:
            count = 0
            while i < len(data) and data[i] == 0:
                count += 1
                i += 1
            output.extend([marker, count])
        else:
            output.append(data[i])
            i += 1
    return output


def zle_decode(data: list[int], marker: int) -> list[int]:
    output = []
    i = 0
    while i < len(data):
        if data[i] == marker:
            count = data[i + 1]
            output.extend([0] * count)
            i += 2
        else:
            output.append(data[i])
            i += 1
    return output
