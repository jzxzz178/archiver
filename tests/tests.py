from compressor import bwt_encode, bwt_decode, mtf_encode, mtf_decode

def test_mtf_identity():
    alphabet = list("abcde")
    text = "abcdeabcde"
    encoded = mtf_encode(text, alphabet)
    decoded = mtf_decode(encoded, alphabet)
    assert decoded == text, f"MTF fail: {decoded} != {text}"
    print("MTF identity test passed.")

def test_bwt_mtf_pipeline():
    text = "banana"
    alphabet = list("!#()*,-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz \n\0")

    bwted, idx = bwt_encode(text)
    mtf_encoded = mtf_encode(bwted, alphabet)
    mtf_decoded = mtf_decode(mtf_encoded, alphabet)
    recovered = bwt_decode(mtf_decoded, idx)

    assert recovered == text, f"Pipeline fail: {recovered} != {text}"
    print("BWT+MTF pipeline test passed.")

def test_bwt_identity():
    text = "banana"
    encoded, idx = bwt_encode(text)
    decoded = bwt_decode(encoded, idx)
    assert decoded == text, f"BWT fail: {decoded} != {text}"
    print("BWT identity test passed.")