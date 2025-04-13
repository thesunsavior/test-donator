"""
Example functions demonstrating the use of register_for_donation
with different output types.
"""

from donate_a_pytest.decorators import register_for_donation


@register_for_donation
def process_mixed_data(a, b):
    """
    A function that handles different types of inputs and returns various output types.

    This function demonstrates how the register_for_donation decorator can be used
    with functions that return different types of outputs (not just dictionaries).

    The decorator creates a test function named 'test_process_mixed_data' that will be
    collected by pytest, while also allowing this function to be used normally.

    Args:
        a: First input parameter (any type)
        b: Second input parameter (any type)

    Returns:
        Various types depending on the input types
    """
    # Integer addition
    if isinstance(a, int) and isinstance(b, int):
        return a + b

    # String concatenation with space
    elif isinstance(a, str) and isinstance(b, str):
        return a + " " + b

    # List concatenation
    elif isinstance(a, list) and isinstance(b, list):
        return a + b

    # Dictionary merging
    elif isinstance(a, dict) and isinstance(b, dict):
        return {**a, **b}

    # Boolean OR operation
    elif isinstance(a, bool) or isinstance(b, bool):
        return a or b

    # Default case
    return None


@register_for_donation
def calculate_statistics(data):
    """
    Calculate basic statistics for a list of numbers.

    The decorator creates a test function named 'test_calculate_statistics' that will be
    collected by pytest, while also allowing this function to be used normally.

    Args:
        data: Dictionary containing a "numbers" key with a list of numbers

    Returns:
        Dictionary with statistics (min, max, mean, sum)
    """
    numbers = data["numbers"]

    if not numbers:
        return {"min": None, "max": None, "mean": None, "sum": 0}

    return {
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
        "sum": sum(numbers),
    }


@register_for_donation
def format_name(person):
    """
    Format a person's name based on provided information.

    The decorator creates a test function named 'test_format_name' that will be
    collected by pytest, while also allowing this function to be used normally.

    Args:
        person: Dictionary with person information

    Returns:
        Formatted string (not a dictionary)
    """
    if "title" in person and person["title"]:
        return f"{person['title']} {person['first_name']} {person['last_name']}"

    return f"{person['first_name']} {person['last_name']}"


@register_for_donation
def filter_list(data):
    """
    Filter a list based on criteria.

    The decorator creates a test function named 'test_filter_list' that will be
    collected by pytest, while also allowing this function to be used normally.

    Args:
        data: Dictionary with filter parameters

    Returns:
        List of filtered items (not a dictionary)
    """
    items = data["items"]
    min_value = data.get("min_value", float("-inf"))
    max_value = data.get("max_value", float("inf"))

    return [item for item in items if min_value <= item <= max_value]


if __name__ == "__main__":
    # Example usage of the functions
    # This demonstrates that the original functions are still usable

    # Example of process_mixed_data
    print("Integer addition:", process_mixed_data(5, 3))
    print("String concatenation:", process_mixed_data("Hello", "World"))
    print("List concatenation:", process_mixed_data([1, 2], [3, 4]))

    # Example of calculate_statistics
    stats = calculate_statistics({"numbers": [1, 2, 3, 4, 5]})
    print("Statistics:", stats)

    # Example of format_name
    name1 = format_name({"first_name": "John", "last_name": "Doe"})
    name2 = format_name({"title": "Dr.", "first_name": "Jane", "last_name": "Smith"})
    print("Names:", name1, "and", name2)

    # Example of filter_list
    filtered = filter_list(
        {"items": [1, 5, 10, 15, 20], "min_value": 5, "max_value": 15}
    )
    print("Filtered list:", filtered)
