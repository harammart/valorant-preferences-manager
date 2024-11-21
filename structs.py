from pydantic.dataclasses import dataclass
from typing import List, Optional, Any


@dataclass
class EntitlementsTokenResponse:
    accessToken: Optional[str] = None
    entitlements: Optional[List[Any]] = None
    issuer: Optional[str] = None
    subject: Optional[str] = None
    token: Optional[str] = None

