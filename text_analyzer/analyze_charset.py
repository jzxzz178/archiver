from collections import Counter

def analyze_file_charset(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    char_counts = Counter(text)

    all_chars = sorted(char_counts)
    min_code = min(ord(c) for c in all_chars)
    max_code = max(ord(c) for c in all_chars)

    print(f"Total unique characters: {len(all_chars)}")
    print(f"Character range: {repr(all_chars[0])} ({min_code}) → {repr(all_chars[-1])} ({max_code})")
    print("\nMost common characters:")
    for ch, count in char_counts.most_common(10):
        print(f"  {repr(ch)} : {count} times")

    print("\nFull sorted charset:")
    alphabet = ''.join(all_chars)
    print(alphabet)

    print(f"len(alphabet): {len(alphabet)}")

if __name__ == '__main__':
    analyze_file_charset('text_analyzer/Crime and Punishment by Fyodor Dostoyevsky 2.txt')
