# sandbox_planning_tools

## Cart Promotion Engine

`promotions.py` — applies percentage and fixed-cart discounts to a shopping cart.

### Usage

```python
from promotions import apply_promotions

cart = [
    {"id": "1", "title": "T-shirt", "quantity": 2, "unitPriceCents": 2500, "tags": ["apparel"]},
    {"id": "2", "title": "Mug",     "quantity": 1, "unitPriceCents": 1500, "tags": ["home"]},
]

promotions = [
    {"type": "percentage", "tag": "apparel", "percentOff": 10},
    {"type": "fixed_cart", "amountOffCents": 1000},
]

result = apply_promotions(cart, promotions)
# {
#   "original_subtotal_cents": 6500,
#   "total_discount_cents":    1500,
#   "final_total_cents":       5000,
#   "lines": [...]
# }
```

### Promotion types

| Type | Fields | Behavior |
|---|---|---|
| `percentage` | `tag`, `percentOff` | Applied sequentially to matching line items |
| `fixed_cart` | `amountOffCents` | Subtracted from cart total after line discounts; floors at 0 |

### Tests

```bash
python3 test_promotions.py
```
