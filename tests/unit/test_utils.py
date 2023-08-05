from mups.utils import normalize_name


def test_normalize_name():
    assert normalize_name("as_df") == "as-df"
