from compressor import bwt_encode, bwt_decode, mtf_encode, mtf_decode, zle_encode, zle_decode

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

