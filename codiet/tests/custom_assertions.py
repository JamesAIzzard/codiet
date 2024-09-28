def assertDictValuesIdentical(dict1, dict2):
    if len(dict1) != len(dict2):
        raise AssertionError(f"Dict lengths are not equal: {len(dict1)} != {len(dict2)}")
    for key, value in dict1.items():
        if key not in dict2:
            raise AssertionError(f"Key {key} not found in second dict")
        if dict2[key] is not value:
            raise AssertionError(f"Values for key {key} are not identical: {dict2[key]} is not {value}")