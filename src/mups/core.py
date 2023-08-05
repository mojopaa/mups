import re
import shutil
import subprocess
from dataclasses import dataclass
from sysconfig import get_platform

from packaging.version import InvalidVersion, Version
from serde import serde
from serde.json import to_json


def get_user_email_from_git() -> tuple[str, str]:
    """Get username and email from git config.
    Return empty if not configured or git is not found.
    """
    git = shutil.which("git")
    if not git:
        return "", ""
    try:
        username = subprocess.check_output(
            [git, "config", "user.name"], text=True, encoding="utf-8"
        ).strip()
    except subprocess.CalledProcessError:
        username = ""
    try:
        email = subprocess.check_output(
            [git, "config", "user.email"], text=True, encoding="utf-8"
        ).strip()
    except subprocess.CalledProcessError:
        email = ""
    return username, email


@serde
@dataclass
class RingInfo:
    """Mostly used in MojoPI"""
    name: str
    version: str
    platform: str = get_platform()
    author: str = get_user_email_from_git()[0]
    author_email: str = get_user_email_from_git()[1]
    requires_dist: list[str] | None = None
    requires_mojo: str = ""
    file_name: str = ""


# Follow https://peps.python.org/pep-0508/#names
PACKAGE_NAME_RE = r"([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$"


def is_valid_name(pkg_name: str) -> bool:
    return bool(re.match(PACKAGE_NAME_RE, pkg_name, re.IGNORECASE))


# Follow
def is_valid_version(v: str) -> bool:
    try:
        Version(v)
        return True
    except InvalidVersion:
        return False


# get_platform()
# https://docs.python.org/3/library/sysconfig.html#sysconfig.get_platform

# Examples of returned values:

# linux-i586
# linux-alpha (?)
# solaris-2.6-sun4u

# Windows will return one of:

# win-amd64 (64bit Windows on AMD64, aka x86_64, Intel64, and EM64T)
# win32 (all others - specifically, sys.platform is returned)

# macOS can return:

# macosx-10.6-ppc
# macosx-10.4-ppc64
# macosx-10.3-i386
# macosx-10.4-fat

# For other non-POSIX platforms, currently just returns sys.platform.


# Follow RFC 5322
EMAIL_RE = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'


def is_valid_email(email: str) -> bool:
    return bool(re.match(EMAIL_RE, email))
