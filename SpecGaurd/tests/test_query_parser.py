from specsense.query_parser import parse_query


def test_budget_and_category_extraction():
    parsed = parse_query("Need a lightweight laptop under ₹30,000 for coding and long battery life")
    assert parsed['category'] == 'laptop'
    assert parsed['budget'] == 30000
    assert 'lightweight' in parsed['soft_preferences']
    assert 'coding' in parsed['soft_preferences']
    assert 'battery life' in parsed['soft_preferences']


def test_unknown_category_defaults_to_all():
    parsed = parse_query("Looking for something under 25000 with good battery")
    assert parsed['category'] is None
    assert parsed['budget'] == 25000
