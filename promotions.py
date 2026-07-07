"""
Cart promotion engine.

Cart item:  {"id": str, "title": str, "quantity": int, "unitPriceCents": int, "tags": list[str]}
Promotions:
    {"type": "percentage", "tag": str, "percentOff": float}
    {"type": "fixed_cart", "amountOffCents": int}
"""


def apply_promotions(cart: list[dict], promotions: list[dict]) -> dict:
    percent_promos = [p for p in promotions if p["type"] == "percentage"]
    fixed_promos = [p for p in promotions if p["type"] == "fixed_cart"]

    line_results = []

    for item in cart:
        original = item["unitPriceCents"] * item["quantity"]
        current = original

        for promo in percent_promos:
            if promo["tag"] in item.get("tags", []):
                discount = int(current * promo["percentOff"] / 100)
                current -= discount

        line_results.append({
            "id": item["id"],
            "title": item["title"],
            "original_cents": original,
            "discounted_cents": current,
            "line_discount_cents": original - current,
        })

    original_subtotal = sum(r["original_cents"] for r in line_results)
    after_line_discount = sum(r["discounted_cents"] for r in line_results)

    fixed_discount = sum(p["amountOffCents"] for p in fixed_promos)
    final_total = max(0, after_line_discount - fixed_discount)

    return {
        "original_subtotal_cents": original_subtotal,
        "total_discount_cents": original_subtotal - final_total,
        "final_total_cents": final_total,
        "lines": line_results,
    }
