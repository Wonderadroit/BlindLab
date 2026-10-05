from __future__ import annotations
import argparse, json
from pathlib import Path
from .generator import generate_campaign
from .models import Business, Campaign


def main() -> None:
    p = argparse.ArgumentParser(description="BlindLab Business Content Studio")
    p.add_argument("--name", required=True)
    p.add_argument("--category", required=True)
    p.add_argument("--location", default="")
    p.add_argument("--phone", default="")
    p.add_argument("--offer", default="")
    p.add_argument("--description", default="")
    p.add_argument("--channel", default="whatsapp")
    p.add_argument("--tone", default="premium")
    p.add_argument("--audience", default="local customers")
    p.add_argument("--variants", type=int, default=3)
    p.add_argument("--output", default="artifacts/content-package.json")
    args = p.parse_args()
    campaign = Campaign(Business(args.name, args.category, args.location, args.phone, args.offer, args.description), args.channel, args.tone, args.audience, args.variants)
    package = generate_campaign(campaign)
    data = {"business": vars(campaign.business), "campaign": {"channel": campaign.channel, "tone": campaign.tone, "audience": campaign.audience, "variants": campaign.variants}, "content": vars(package)}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out)
