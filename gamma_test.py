from gamma import gamma_encode_list, gamma_decode


def test_nums():
    nums = [1, 3, 5, 10]
    encoded = gamma_encode_list(nums)
    decoded = gamma_decode(encoded)
    assert nums == decoded
