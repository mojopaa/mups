from dataclasses import dataclass

from serde import serde
from serde.json import to_json


@serde
@dataclass
class RingInfo:
    name: str
    version: str
    platform: str = ""  # TODO: standardize
    author: str = ""
    author_email: str = ""
    requires_dist: str = ""
    requires_mojo: str = ""
    file_name: str = ""
