from tests.tests import test_bwt_identity, test_bwt_mtf_pipeline, test_mtf_identity

def test_all():
    test_bwt_identity()
    test_mtf_identity()
    test_bwt_mtf_pipeline()

if __name__ == '__main__':
    test_all()
