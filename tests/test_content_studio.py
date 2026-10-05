from studio.generator import generate_campaign
from studio.models import Business, Campaign


def test_car_campaign_contains_business_identity_and_cta():
    b = Business("Lagos Auto Hub", "cars", "Lagos", "08012345678", "2015 Toyota Camry", "Clean interior, automatic transmission")
    out = generate_campaign(Campaign(b))
    assert "Lagos Auto Hub" in out.cta
    assert "2015 Toyota Camry" in out.caption
    assert len(out.visual_prompts) == 3


def test_empty_optional_fields_do_not_create_broken_copy():
    b = Business("Test Business", "services")
    out = generate_campaign(Campaign(b))
    assert "None" not in out.caption
    assert out.visual_prompts
