def build_suffix_array(s: str) -> list[int]:
    n = len(s)
    rank = [ord(c) for c in s]
    sa   = list(range(n))
    tmp  = [0]*n
    k = 1

    while True:
        sa.sort(key=lambda i: (rank[i], rank[i+k] if i+k<n else -1))
        tmp[sa[0]] = 0
        for j in range(1, n):
            prev, cur = sa[j-1], sa[j]
            prev_key = (rank[prev], rank[prev+k] if prev+k<n else -1)
            cur_key  = (rank[cur],  rank[cur+k]  if cur+k<n  else -1)
            tmp[cur] = tmp[prev] + (prev_key < cur_key)
        rank, tmp = tmp, rank
        if rank[sa[-1]] == n-1:
            break
        k <<= 1

    return sa

def bwt_encode(text: str) -> tuple[str, int]:
    s = text + '\0'
    sa = build_suffix_array(s)
    last = []
    orig_idx = None
    for pos in sa:
        if pos == 0:
            last.append(s[-1])  # суффикс, начинающийся в 0, получает последний символ
            orig_idx = len(last)-1
        else:
            last.append(s[pos-1])
    return ''.join(last), orig_idx


def bwt_decode(bwt: str, original_index: int) -> str:
    n = len(bwt)    

    total_count = {}
    occ = [0] * n
    for i, ch in enumerate(bwt):
        occ[i] = total_count.get(ch, 0)
        total_count[ch] = occ[i] + 1

    C = {}
    cum = 0
    for ch in sorted(total_count):
        C[ch] = cum
        cum += total_count[ch]

    res = []
    ptr = original_index
    for _ in range(n):
        ch = bwt[ptr]
        res.append(ch)
        ptr = C[ch] + occ[ptr]

    return ''.join(reversed(res)).rstrip('\0')
