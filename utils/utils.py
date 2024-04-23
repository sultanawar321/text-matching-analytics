import sys

sys.path.append("../src/")

from app import TextMatchingFuzzyWuzzy

matcher = TextMatchingFuzzyWuzzy()


def test_preprocess_text():
    """
    This tests the preprocess_text function
    """
    # Test input text
    input_text = "Sample input text"
    # Call the preprocess_text function
    output = matcher.preprocess_text(input_text)
    # Check if the output is a list
    assert isinstance(output, list), "Output is not a list"


def test_fuzzy_wuzyy():
    """
    This tests the fuzzy_wuzyy function
    """
    # Define test input parameters
    features = ["account", "name", "phone number", "address", "postcode"]
    document = ["customer", "account", "issues", "address", "payments"]
    match = 60  # Set a low match threshold for testing purposes
    # Call the function with test inputs
    result = matcher.fuzzy_wuzyy(features, document, match)
    # Define expected output based on the provided test input
    expected_output = {"account", "address"}
    # Assert that the output is a set
    assert isinstance(result, set), "Output is not a set"
    # Assert that the output matches the expected output
    assert result == expected_output, "Output does not match the expected output"


def test_missing_words():
    """
    This tests the missing_words function
    """
    # Define test input parameters
    required_features = ["account", "name", "phone number", "address", "postcode"]
    found_features = ["account", "name"]
    # Call the function with test inputs
    result = matcher.missing_words(found_features, required_features)
    # Define expected output based on the provided test input
    expected_output = {"phone number", "address", "postcode"}
    # Assert that the output matches the expected output
    assert result == expected_output, "Output does not match the expected output"
