from compressor import bwt_encode, bwt_decode, mtf_encode, mtf_decode, zle_encode, zle_decode
from compressor.ari import ArithmeticCoder
from colorama import init, Fore, Style

def test_mtf_identity():
    alphabet = list("abcde")
    text = "abcdeabcde"
    encoded = mtf_encode(text, alphabet)
    decoded = mtf_decode(encoded, alphabet)
    assert decoded == text, f"MTF fail: {decoded} != {text}"
    print("\033[32mMTF identity test passed.\033[0m")

def test_bwt_mtf_pipeline():
    text = "banana"
    alphabet = list("!#()*,-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz \n\0")

    bwted, idx = bwt_encode(text)
    mtf_encoded = mtf_encode(bwted, alphabet)
    mtf_decoded = mtf_decode(mtf_encoded, alphabet)
    recovered = bwt_decode(mtf_decoded, idx)

    assert recovered == text, f"Pipeline fail: {recovered} != {text}"
    print("\033[32mBWT+MTF pipeline test passed.\033[0m")

def test_bwt_identity():
    text = "banana"
    encoded, idx = bwt_encode(text)
    decoded = bwt_decode(encoded, idx)
    assert decoded == text, f"BWT fail: {decoded} != {text}"
    print("\033[32mBWT identity test passed.\033[0m")

def test_zle_identity():
    data = [1, 2, 3, 0, 0, 0, 4, 5, 6, 0, 0, 0, 7, 8, 9]
    encoded = zle_encode(data)
    decoded = zle_decode(encoded)
    assert decoded == data, f"ZLE fail: {decoded} != {data}"
    print("\033[32mZLE identity test passed.\033[0m")

def test_zle_empty():
    data = []
    encoded = zle_encode(data)
    decoded = zle_decode(encoded)
    assert decoded == data, f"ZLE empty fail: {decoded} != {data}"
    print("\033[32mZLE empty test passed.\033[0m")

def test_zle_no_zeros():
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    encoded = zle_encode(data)
    decoded = zle_decode(encoded)
    assert decoded == data, f"ZLE no zeros fail: {decoded} != {data}"
    print("\033[32mZLE no zeros test passed.\033[0m")

def test_ari_identity():
    data = [1, 1, 0, 2, 0, 0, 0, 3, 1, 1]
    coder = ArithmeticCoder(data)
    code = coder.encode()
    decoded = coder.decode(code, len(data))
    try:
        assert decoded == data, f"ARI fail: {decoded} != {data}"
        print(f"{Fore.GREEN}ARI identity test passed.{Style.RESET_ALL}")
    except AssertionError as e:
        print(f"{Fore.RED}ARI identity test failed: {e}{Style.RESET_ALL}")

def test_ari_empty():
    data = []
    coder = ArithmeticCoder(data)
    code = coder.encode()
    decoded = coder.decode(code, len(data))
    try:
        assert decoded == data, f"ARI empty fail: {decoded} != {data}"
        print(f"{Fore.GREEN}ARI empty test passed.{Style.RESET_ALL}")
    except AssertionError as e:
        print(f"{Fore.RED}ARI empty test failed: {e}{Style.RESET_ALL}")

def test_ari_single_symbol():
    data = [1, 1, 1, 1, 1]
    coder = ArithmeticCoder(data)
    code = coder.encode()
    decoded = coder.decode(code, len(data))
    try:
        assert decoded == data, f"ARI single symbol fail: {decoded} != {data}"
        print(f"{Fore.GREEN}ARI single symbol test passed.{Style.RESET_ALL}")
    except AssertionError as e:
        print(f"{Fore.RED}ARI single symbol test failed: {e}{Style.RESET_ALL}")

def test_ari_large_data():
    data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] * 10
    coder = ArithmeticCoder(data)
    code = coder.encode()
    decoded = coder.decode(code, len(data))
    try:
        assert decoded == data, f"ARI large data fail: {decoded} != {data}"
        print(f"{Fore.GREEN}ARI large data test passed.{Style.RESET_ALL}")
    except AssertionError as e:
        print(f"{Fore.RED}ARI large data test failed: {e}{Style.RESET_ALL}")

