from promotions import apply_promotions

TSHIRT = {"id": "1", "title": "T-shirt", "quantity": 2, "unitPriceCents": 2500, "tags": ["apparel"]}
MUG    = {"id": "2", "title": "Mug",     "quantity": 1, "unitPriceCents": 1500, "tags": ["home"]}


def test_normal_case():
    result = apply_promotions([TSHIRT, MUG], [
        {"type": "percentage", "tag": "apparel", "percentOff": 10},
        {"type": "fixed_cart", "amountOffCents": 1000},
    ])
    assert result["original_subtotal_cents"] == 6500
    assert result["final_total_cents"] == 5000        # 6500 - 500 line - 1000 fixed
    assert result["total_discount_cents"] == 1500
    assert result["lines"][0]["line_discount_cents"] == 500   # 10% of 5000
    assert result["lines"][1]["line_discount_cents"] == 0


def test_multiple_percentage_promos_sequential():
    # Two percent promos on same tag: 20% then 10% of the reduced price.
    # 1000 -> -200 -> 800 -> -80 -> 720  (not 700 if applied simultaneously)
    item = {"id": "1", "title": "Hat", "quantity": 1, "unitPriceCents": 1000, "tags": ["apparel"]}
    result = apply_promotions([item], [
        {"type": "percentage", "tag": "apparel", "percentOff": 20},
        {"type": "percentage", "tag": "apparel", "percentOff": 10},
    ])
    assert result["lines"][0]["discounted_cents"] == 720
    assert result["final_total_cents"] == 720


def test_non_matching_promotion():
    # "home" promo should not affect apparel item.
    result = apply_promotions([TSHIRT], [
        {"type": "percentage", "tag": "home", "percentOff": 50},
    ])
    assert result["lines"][0]["line_discount_cents"] == 0
    assert result["final_total_cents"] == 5000


def test_fixed_cart_discount_exceeds_total():
    # Fixed discount larger than total should floor at 0.
    result = apply_promotions([MUG], [
        {"type": "fixed_cart", "amountOffCents": 9999},
    ])
    assert result["final_total_cents"] == 0
    assert result["total_discount_cents"] == 1500     # capped at what was actually there


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS  {name}")
