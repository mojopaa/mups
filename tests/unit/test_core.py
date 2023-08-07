import shutil

import pytest

from mups.core import (
    RingInfo,
    get_username_email_from_git,
    is_email,
    is_valid_name,
    is_valid_version,
    ring_info,
    ring_file_name,
)


def test_is_valid_name():
    assert is_valid_name("abc-123") == True
    assert is_valid_name("abc-") == False
    assert is_valid_name("Abc-123") == True
    assert is_valid_name("-abc-") == False


def test_is_valid_version():
    assert is_valid_version("1.2.3") == True
    assert is_valid_version("1.2.3a1") == True
    assert is_valid_version("1.2.3.dev1") == True
    assert is_valid_version(".2.3") == False
    assert is_valid_version("1.2.3.alpha") == True
    assert is_valid_version("23230123") == True
    assert is_valid_version("2023-01-23") == False
    assert is_valid_version("2023.01.23") == True


def test_is_email():
    assert is_email("sometest@gmail.com") == True
    assert is_email("some+test@gmail.com") == True
    assert is_email("stuart.sillitoe@prodirectsport.net") == True
    assert is_email("_valid@mail.com") == True
    assert is_email("also+valid@domain.com") == True
    assert is_email("invalíd@mail.com") == False
    assert is_email('invalid%$£"@domain.com') == False
    assert is_email("invalid£@domain.com") == False
    assert is_email("valid%$@domain.com") == True
    assert is_email('invali"d@domain.com') == False


def test_RingInfo():
    r = RingInfo(name="test", version="1")
    git = shutil.which("git")
    if git:
        assert r.author
        assert r.author_email


def test_get_username_email_from_git():
    git = shutil.which("git")
    if git:
        assert type(get_username_email_from_git()[0]) == str
        assert type(get_username_email_from_git()[1]) == str
    else:
        assert get_username_email_from_git() == ("", "")


def test_ring_info():
    assert ring_info("test", "1")
    assert ring_info("test", "1", format="json")

    r = RingInfo(name="test", version="1")
    assert RingInfo.from_toml(r.to_toml()) == r

    with pytest.raises(AssertionError):
        ring_info("*test", "1")  # Wrong name

    with pytest.raises(AssertionError):
        ring_info("test", "*1")  # Wrong version


def test_ring_file_name():
    assert ring_file_name("test", "1") == "test-1.ring"
    assert ring_file_name("test", "1", ["mac"]) == "test-1-mac.ring"
    assert ring_file_name("test", "1", "mac") == "test-1-mac.ring"
