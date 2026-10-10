from specsense.matcher import match_products


def test_match_products_filters_budget_and_ranks_well():
    products = [
        {
            'product_id': 'P1',
            'product_name': 'Acer Aspire',
            'category': 'laptop',
            'price': 29000,
            'weight_kg': 1.3,
            'ram_gb': 16,
            'storage_gb': 512,
            'battery_ah': 55,
            'processor': 'Intel i5',
            'description': 'Lightweight laptop for coding and travel.'
        },
        {
            'product_id': 'P2',
            'product_name': 'Heavy Laptop',
            'category': 'laptop',
            'price': 25000,
            'weight_kg': 2.4,
            'ram_gb': 8,
            'storage_gb': 256,
            'battery_ah': 42,
            'processor': 'Intel i3',
            'description': 'Basic laptop.'
        },
    ]

    results = match_products(products, {
        'category': 'laptop',
        'budget': 30000,
        'soft_preferences': ['lightweight', 'coding', 'battery life']
    })

    assert len(results) == 2
    assert results[0]['product_id'] == 'P1'
    assert results[0]['matched_hard_constraints']
