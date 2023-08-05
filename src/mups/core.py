import re
from dataclasses import dataclass

from serde import serde
from serde.json import to_json
from packaging.version import Version, InvalidVersion
from sysconfig import get_platform


@serde
@dataclass
class RingInfo:
    name: str
    version: str
    platform: str = ""  # TODO: standardize
    author: str = ""
    author_email: str = ""
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