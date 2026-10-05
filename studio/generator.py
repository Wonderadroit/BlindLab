from __future__ import annotations
import re
from .models import Campaign, ContentPackage


def _clean(value: str) -> str:
    return re.sub(r"\\s+", " ", value or "").strip()


def _title(category: str) -> str:
    c = _clean(category).lower()
    if "car" in c or "auto" in c or "vehicle" in c:
        return "Your next car should look this good."
    if "restaurant" in c or "food" in c:
        return "Good food deserves a better first impression."
    if "fashion" in c or "clothing" in c:
        return "Make your next look impossible to ignore."
    if "real estate" in c or "property" in c:
        return "The property you've been looking for is here."
    return "Give your business the attention it deserves."


def generate_campaign(campaign: Campaign) -> ContentPackage:
    b = campaign.business
    name = _clean(b.name) or "Your Business"
    offer = _clean(b.offer)
    location = _clean(b.location)
    phone = _clean(b.phone)
    desc = _clean(b.description)
    headline = _title(b.category)
    sub = f"{offer}. " if offer else ""
    sub += desc or f"Discover what {name} has to offer."
    place = f" | {location}" if location else ""
    cta = f"Message {name}{place}" + (f" on {phone}" if phone else " to order or enquire.")
    caption = f"{headline}\\n\\n{sub}\\n\\n{cta}"
    status = f"{headline}\\n{sub}\\n\\n{cta}"
    visual_prompts = []
    for i in range(max(1, min(campaign.variants, 5))):
        angle = [
            "premium hero advertisement, cinematic commercial photography",
            "clean social-media product advertisement, realistic natural lighting",
            "high-conversion mobile advertisement, premium editorial photography",
            "luxury campaign advertisement, realistic environment and shallow depth of field",
            "bold promotional advertisement, realistic photography, strong product focus",
        ][i]
        visual_prompts.append(
            f"Create a photorealistic {angle}. Business: {name}. Category: {b.category}. "
            f"Offer: {offer or 'show the core product/service'}. Description: {desc or 'professional presentation'}. "
            "Preserve the real product identity from any supplied reference photo; do not invent logos, prices, contact details, or physical features."
        )
    return ContentPackage(headline, sub, cta, caption, status, visual_prompts)
