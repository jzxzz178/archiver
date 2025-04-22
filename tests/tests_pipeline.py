from tests.tests import test_bwt_identity, test_bwt_mtf_pipeline, test_mtf_identity, test_zle_identity, test_zle_empty, test_zle_no_zeros

def test_all():
    test_bwt_identity()
    test_mtf_identity()
    test_bwt_mtf_pipeline()
    test_zle_identity()
    test_zle_empty()
    test_zle_no_zeros()

if __name__ == '__main__':
    test_all()
