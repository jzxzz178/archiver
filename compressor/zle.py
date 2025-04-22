ZLE_MARKER = 256

def zle_encode(data: list[int]) -> list[int]:
    """Заменяет серии нулей на маркер и длину"""
    output = []
    i = 0
    while i < len(data):
        if data[i] == 0:
            count = 0
            while i < len(data) and data[i] == 0:
                count += 1
                i += 1
            output.extend([ZLE_MARKER, count])
        else:
            output.append(data[i])
            i += 1
    return output


def zle_decode(data: list[int]) -> list[int]:
    """Восстанавливает нули по маркеру и длине"""
    output = []
    i = 0
    while i < len(data):
        if data[i] == ZLE_MARKER:
            count = data[i + 1]
            output.extend([0] * count)
            i += 2
        else:
            output.append(data[i])
            i += 1
    return output
