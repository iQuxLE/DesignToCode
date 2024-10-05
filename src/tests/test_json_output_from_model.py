from DesignToCode.util.util import parse_new_and_compared_description_seperately


def test_parse_function_valid_input():
    # Input string containing a valid JSON code block
    test_input = """
    Here is the updated description:

    ```json
    {
        "new_description": "This is the new description.",
        "comparison_of_descriptions": "The new description has been updated with more details."
    }
    ```

    Please review the changes.
    """
    expected_new_description = "This is the new description."
    expected_comparison = "The new description has been updated with more details."

    # Call the function
    new_desc, comparison = parse_new_and_compared_description_seperately(test_input)

    # Assertions to verify the outputs
    assert new_desc == expected_new_description, "The new description does not match the expected output."
    assert comparison == expected_comparison, "The comparison of descriptions does not match the expected output."



