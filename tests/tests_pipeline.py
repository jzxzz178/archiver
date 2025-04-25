from tests.conveyor_test import test_full_pipeline
from tests.module_tests import (
    test_ari_empty, test_ari_large_data, test_ari_single_symbol, test_bwt_identity, test_bwt_mtf_pipeline, test_mtf_identity,
    test_zle_identity, test_zle_empty, test_zle_no_zeros,
    test_ari_identity
)

def run_module_tests():
    test_bwt_identity()
    test_mtf_identity()
    test_bwt_mtf_pipeline()
    test_zle_identity()
    test_zle_empty()
    test_zle_no_zeros()
    test_ari_identity()
    test_ari_empty()
    test_ari_large_data()
    test_ari_single_symbol()

def run_conveyor_test():
    test_full_pipeline()

if __name__ == '__main__':
    run_module_tests()
    # run_conveyor_test()
