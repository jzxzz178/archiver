from compressor.bwt import bwt_encode, bwt_decode
from compressor.mtf import mtf_encode, mtf_decode

ALPHABET = list("!#()*,-.0123456789:;?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]_abcdefghijklmnopqrstuvwxyz \n\0")

text = "banana"
bwted, idx = bwt_encode(text)
mtf_encoded = mtf_encode(bwted, ALPHABET)
mtf_decoded = mtf_decode(mtf_encoded, ALPHABET)

assert mtf_decoded == bwted
print("MTF encoding:", mtf_encoded)
