from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Business:
    name: str
    category: str
    location: str = ""
    phone: str = ""
    offer: str = ""
    description: str = ""


@dataclass(frozen=True)
class Campaign:
    business: Business
    channel: str = "whatsapp"
    tone: str = "premium"
    audience: str = "local customers"
    variants: int = 3


@dataclass(frozen=True)
class ContentPackage:
    headline: str
    subheadline: str
    cta: str
    caption: str
    status_copy: str
    visual_prompts: list[str] = field(default_factory=list)
