import re
import shutil
import subprocess
from dataclasses import dataclass
from sysconfig import get_platform

from mashumaro.mixins.json import DataClassJSONMixin
from mashumaro.mixins.toml import DataClassTOMLMixin
from packaging.version import InvalidVersion, Version


def get_username_email_from_git() -> tuple[str, str]:
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


@dataclass
class RingInfo(DataClassTOMLMixin, DataClassJSONMixin):
    """Confrom mojo core-metadata"""

    name: str
    version: str
    metadata_version: str = "0.1"
    # Below are optional
    dynamic: list[str] | None = None
    platforms: list[str] | None = None
    supported_platforms: list[str] | None = None
    summary: str = ""
    description: str = ""
    description_content_type: str = "text/markdown"
    keywords: list[str] | None = None
    home_page: str = ""
    download_url: str = ""
    author: str = get_username_email_from_git()[0]
    author_email: str = get_username_email_from_git()[1]
    maintainer: str = get_username_email_from_git()[0]
    maintainer_email: str = get_username_email_from_git()[1]
    license: str = ""
    classifiers: list[str] | None = None
    requires_dist: list[str] | None = None
    requires_mojo: str = ""
    requires_external: list[str] | None = None
    project_urls: dict[str, str] | None = None
    provides_extra: list[str] | None = None
    provides_dist: list[str] | None = None
    obsoletes_dist: list[str] | None = None
    file_name: str = ""


def ring_info(
    name: str,
    version: str,
    metadata_version: str = "0.1",
    # Below are optional
    dynamic: list[str] | None = None,
    platforms: list[str] | None = None,
    supported_platforms: list[str] | None = None,
    summary: str = "",
    description: str = "",
    description_content_type: str = "text/markdown",
    keywords: list[str] | None = None,
    home_page: str = "",
    download_url: str = "",
    author: str = get_username_email_from_git()[0],
    author_email: str = get_username_email_from_git()[1],
    maintainer: str = get_username_email_from_git()[0],
    maintainer_email: str = get_username_email_from_git()[1],
    license: str = "",
    classifiers: list[str] | None = None,
    requires_dist: list[str] | None = None,
    requires_mojo: str = "",
    requires_external: list[str] | None = None,
    project_urls: dict[str, str] | None = None,
    provides_extra: list[str] | None = None,
    provides_dist: list[str] | None = None,
    obsoletes_dist: list[str] | None = None,
    file_name: str = "",
    use_get_platform=True,
    create_filename=True,
    format="toml",
):
    """
    Generates the JSON representation of the ring information.
    It is the public API for initing RingInfo.


    Returns:
        str: The JSON representation of the ring information.
    """
    # TODO: check classifiers using https://pypi.org/classifiers/
    if use_get_platform:
        if platforms is None:
            platforms = [get_platform()]
        if supported_platforms is None:
            supported_platforms = [get_platform()]

    if create_filename and not file_name:
        file_name = ring_file_name(name=name, version=version, platforms=platforms)

    assert is_valid_name(name), f"Name does not conform PEP 508."
    if author_email:
        assert is_valid_email(author_email), f"Email format does not follow RFC 5322."
    if maintainer_email:
        assert is_valid_email(
            maintainer_email
        ), f"Email format does not follow RFC 5322."
    if version:
        assert is_valid_version(version), f"Name does not conform PEP 440."

    ring_info = RingInfo(
        name=name,
        version=version,
        metadata_version=metadata_version,
        dynamic=dynamic,
        platforms=platforms,
        supported_platforms=supported_platforms,
        summary=summary,
        description=description,
        description_content_type=description_content_type,
        keywords=keywords,
        home_page=home_page,
        download_url=download_url,
        author=author,
        author_email=author_email,
        maintainer=maintainer,
        maintainer_email=maintainer_email,
        license=license,
        classifiers=classifiers,
        requires_dist=requires_dist,
        requires_mojo=requires_mojo,
        requires_external=requires_external,
        project_urls=project_urls,
        provides_extra=provides_extra,
        provides_dist=provides_dist,
        obsoletes_dist=obsoletes_dist,
        file_name=file_name,
    )
    if format.lower() == "toml":
        return ring_info.to_toml()
    elif format.lower() == "json":
        return ring_info.to_json()


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


def ring_file_name(name, version, platforms):
    # TODO: reference: https://github.com/pypa/wheel/blob/main/src/wheel/vendored/packaging/tags.py
    return "-".join([name, version, *platforms]) + ".ring"
