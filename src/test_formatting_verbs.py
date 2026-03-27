import pytest
from formatting_verbs import interp_str_verbs, S_VERB

# these tests use mock endpoints to test for
# nested resources, as one might find in a REST API.

# Constants
BASE_URL = "https://example.com"
API_URL = f"{BASE_URL}/api"
PATH_PARAM = f"/{S_VERB}"

TEST_URL_BUDGETS = f"{API_URL}/budgets"
TEST_URL_BUDGET = TEST_URL_BUDGETS + PATH_PARAM

TEST_URL_BUDGET_GROUPS = f"{TEST_URL_BUDGET}/groups"
TEST_URL_BUDGET_GROUP = TEST_URL_BUDGET_GROUPS + PATH_PARAM


def test_verb_interp_with_no_operands_throws_err():
    with pytest.raises(ValueError, match="no operands"):
        interp_str_verbs(TEST_URL_BUDGET)


def test_verb_interp_with_too_many_operands_throws_err():
    with pytest.raises(ValueError, match="reads arg"):
        interp_str_verbs(TEST_URL_BUDGET_GROUPS, "budget_id", "group_id")


def test_verb_interp_returns_expected_string():
    interpolated = interp_str_verbs(
        TEST_URL_BUDGET_GROUP,
        "budget_id",
        "group_id",
    )
    expected = "https://example.com/api/budgets/budget_id/groups/group_id"
    assert interpolated == expected
