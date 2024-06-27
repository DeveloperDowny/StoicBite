import pytest
import requests
from collections import Counter
import time

@pytest.mark.parametrize("num_requests", [10])
def test_daily_stoic_queue_behavior(num_requests):
    responses = []
    c = 0
    for _ in range(num_requests):
        response = requests.get("http://localhost:5000/daily_stoic")
        responses.append(response.json())
        if c % 2 == 0:
            time.sleep(1)
        c += 1

    quote_counts = Counter(response['quote'] for response in responses)
    unique_quotes = len(quote_counts)
    max_count = max(quote_counts.values())

    assert unique_quotes >= 3, "Should have at least 3 unique quotes"
    assert max_count <= 5, "No quote should appear more than 5 times"

# Run with: pytest test_daily_stoic.py