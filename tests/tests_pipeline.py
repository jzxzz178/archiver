from tests.tests import (
    test_ari_empty, test_ari_large_data, test_bwt_identity, test_bwt_mtf_pipeline, test_mtf_identity,
    test_zle_identity, test_zle_empty, test_zle_no_zeros,
    test_ari_identity
)

def test_all():
    test_bwt_identity()
    test_mtf_identity()
    test_bwt_mtf_pipeline()
    test_zle_identity()
    test_zle_empty()
    test_zle_no_zeros()
    test_ari_identity()
    test_ari_empty()
    test_ari_large_data()

if __name__ == '__main__':
    test_all()
