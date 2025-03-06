import pytest
from tests import client


@pytest.mark.health
def test_check_health():
    """Checks if Aora is up and running"""

    get_response = client.get("/health")
    assert get_response.status_code == 200
    assert get_response.json()["status"] == "Active"
