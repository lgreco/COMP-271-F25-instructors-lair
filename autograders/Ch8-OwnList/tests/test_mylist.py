# test_my_list.py
# Final Autograder for the MyList assignment.
# This version includes checks for unnecessary resizing.

import pytest
# The autograder will import the student's implementation from a file named MyList.py

@pytest.fixture
def empty_list(MyList_class):
    """Provides a fresh, empty MyList instance for each test."""
    return MyList_class()

# --- Test Cases (Total Points: 10.0) ---

# --- Test Group 1: Structural and Initial State (1.0 Point) ---

@pytest.mark.points(0.5)
def test_initial_state(empty_list):
    """Test 1 (0.5 pts): Check initial length (0) and default maximum size (4)."""
    assert len(empty_list) == 0, "Initial length should be 0."
    assert empty_list._maximum_size == 4, "__init__ must set the correct default maximum size (4)."
    assert len(empty_list._data) == 4, "The underlying data list should be initialized to the maximum size."

@pytest.mark.points(0.5)
def test_custom_initial_state(MyList_class):
    """Test 2 (0.5 pts): Check initialization with a custom maximum size."""
    custom_list = MyList_class(10)
    assert len(custom_list) == 0, "Custom initialized list length should be 0."
    assert custom_list._maximum_size == 10, "Custom __init__ argument for maximum_size was ignored."
    assert len(custom_list._data) == 10, "The underlying data list should be initialized to the custom maximum size."

# --- Test Group 2: __len__ and __str__ (1.5 Points) ---

@pytest.mark.points(0.5)
def test_len_after_operations(empty_list):
    """Test 3 (0.5 pts): Check __len__ after append, pop, remove."""
    try:
        empty_list.append(1)
        assert len(empty_list) == 1, "Length did not update after append."
        empty_list.pop()
        assert len(empty_list) == 0, "Length did not update after pop."
        empty_list.append(1)
        empty_list.append(2)
        empty_list.remove(0)
        assert len(empty_list) == 1, "Length did not update after remove."
    except (IndexError, ValueError):
        pytest.fail("A valid operation (like pop on a non-empty list) should not raise an IndexError.")

# Total 1.0 pt (0.25 pts per parameter set)
@pytest.mark.points(0.25)
@pytest.mark.parametrize(
    "elements_to_add",
    [ [], [10, 20, 30], ['a', 'b'], [5, None, 10] ]
)
def test_str_content_and_order(empty_list, elements_to_add):
    """
    Test 4 (1.0 pts total): Check if __str__ correctly represents the list's content.
    """
    test_list = empty_list
    for el in elements_to_add:
        test_list.append(el)
    output_str = str(test_list)
    expected_none_count = elements_to_add.count(None)
    assert output_str.count("None") == expected_none_count, \
        "__str__ should not print unused 'None' slots from the internal array."
    last_find_index = -1
    for element in elements_to_add:
        str_element = str(element)
        assert str_element in output_str, f"Element '{str_element}' was not found in the __str__ output: '{output_str}'"
        current_find_index = output_str.find(str_element, last_find_index + 1)
        assert current_find_index > last_find_index, "Elements in __str__ output are out of order."
        last_find_index = current_find_index

# --- Test Group 3: Resizing (Memory Management) (2.5 Points) ---

@pytest.mark.points(0.5)
def test_no_unnecessary_resizing(empty_list):
    """Test 5 (0.5 pts): Check that the list does NOT resize if it is not at capacity."""
    test_list = empty_list # Initial capacity is 4
    initial_capacity = test_list._maximum_size
    initial_data_len = len(test_list._data)

    test_list.append(1)
    test_list.append(2)

    assert test_list._maximum_size == initial_capacity, "List should not resize when it is not full."
    assert len(test_list._data) == initial_data_len, "Underlying _data list should not change size when not at capacity."


@pytest.mark.points(1.0)
def test_resizing(MyList_class):
    """Test 6 (1.0 pts): Check if the list correctly doubles its size and underlying data list length when full."""
    test_list = MyList_class(2)
    test_list.append(10)
    test_list.append(20)
    test_list.append(30) # This should trigger the resize

    assert test_list._maximum_size == 4, "The _maximum_size attribute failed to double (from 2 to 4)."
    assert len(test_list._data) == 4, "The underlying _data list failed to double in length (from 2 to 4)."
    assert len(test_list) == 3, "Length is incorrect after resize."
    assert test_list._data[:len(test_list)] == [10, 20, 30], "Data integrity failed after resize."

@pytest.mark.points(1.0)
def test_multiple_resizing(MyList_class):
    """Test 7 (1.0 pts): Check for multiple consecutive resizes and underlying data list length."""
    test_list = MyList_class(2)
    # Force 2 -> 4 resize
    for i in range(3):
        test_list.append(i)
    assert test_list._maximum_size == 4, "List failed on the first resize (2->4)."
    assert len(test_list._data) == 4, "Underlying _data list failed to resize (2->4)."

    # Force 4 -> 8 resize
    for i in range(3, 5):
        test_list.append(i)
    assert test_list._maximum_size == 8, "List failed on the second resize (4->8)."
    assert len(test_list._data) == 8, "Underlying _data list failed to resize (4->8)."
    assert len(test_list) == 5, "Length is incorrect after two resizes."
    assert test_list._data[:len(test_list)] == [0, 1, 2, 3, 4], "Data integrity failed after second resize."

# --- Test Group 4: Mutator Methods (append, insert, remove, pop) (5.0 Points) ---

@pytest.mark.points(0.5)
def test_append_correctness(empty_list):
    """Test 8 (0.5 pts): Verify elements are appended correctly to the end."""
    empty_list.append(100)
    empty_list.append(200)
    assert empty_list._data[:len(empty_list)] == [100, 200], "Append failed to place elements correctly."

@pytest.mark.points(0.5)
def test_pop_correctness(empty_list):
    """Test 9 (0.5 pts): Verify pop removes and returns the last element from a non-empty list."""
    empty_list.append(1)
    empty_list.append(2)
    popped = empty_list.pop()
    assert popped == 2, "Pop did not return the last element (2)."
    assert empty_list._data[:len(empty_list)] == [1], "Pop failed to update the list state."

# Total 1.5 pts (0.3 pts per parameter set)
@pytest.mark.points(0.3)
@pytest.mark.parametrize(
    "initial_elements, insert_index, value, expected_list, should_resize",
    [
        ([], 0, 100, [100], False),
        ([1, 2], 2, 300, [1, 2, 300], False),
        ([1, 2], 0, 0, [0, 1, 2], False),
        ([1, 2, 3], 1, 20, [1, 20, 2, 3], False),
        ([1,2,3,4], 2, 99, [1, 2, 99, 3, 4], True) # This case forces a resize
    ],
)
def test_insert_valid_indices(MyList_class, initial_elements, insert_index, value, expected_list, should_resize):
    """Test 10 (1.5 pts total): Verify insert works, including cases that trigger a resize."""
    test_list = MyList_class()
    for item in initial_elements:
        test_list.append(item)

    test_list.insert(insert_index, value)

    assert len(test_list) == len(expected_list), "Insert failed to update length correctly."
    assert test_list._data[:len(test_list)] == expected_list, "Insert failed to shift/insert elements correctly."
    if should_resize:
        assert len(test_list._data) == 8, "Insert failed to resize the underlying _data list correctly."

# Total 1.0 pt (0.5 pts per parameter set)
@pytest.mark.points(0.5)
@pytest.mark.parametrize(
    "remove_index, expected_return, expected_list",
    [ (1, 20, [10, 30, 40]), (0, 10, [20, 30, 40]) ]
)
def test_remove_valid_indices(MyList_class, remove_index, expected_return, expected_list):
    """Test 11 (1.0 pts total): Verify remove correctly returns the element and shifts data."""
    test_list = MyList_class()
    for item in [10, 20, 30, 40]:
        test_list.append(item)
    removed = test_list.remove(remove_index)
    assert removed == expected_return, f"Remove at index {remove_index} returned wrong value."
    assert test_list._data[:len(test_list)] == expected_list, f"Remove at index {remove_index} failed to shift elements."

@pytest.mark.points(0.5)
def test_pop_on_empty(empty_list):
    """Test 12 (0.5 pts): Check pop on empty list returns None OR raises IndexError."""
    try:
        result = empty_list.pop()
        assert result is None, "Pop on an empty list should return None if it doesn't raise an error."
    except (IndexError, ValueError):
        pass
    except Exception as e:
        pytest.fail(f"Pop on an empty list raised an unexpected exception: {e}")

@pytest.mark.points(0.5)
def test_remove_on_empty_or_invalid(empty_list):
    """Test 13 (0.5 pts): Check remove on invalid index returns None OR raises IndexError."""
    try:
        result = empty_list.remove(0)
        assert result is None, "Remove(0) on an empty list should return None if no error is raised."
    except (IndexError, ValueError):
        pass
    except Exception as e:
        pytest.fail(f"Remove(0) on an empty list raised an unexpected exception: {e}")

    empty_list.append(10)
    try:
        result = empty_list.remove(1)
        assert result is None, "Remove on an out-of-bounds index should return None if no error is raised."
    except (IndexError, ValueError):
        pass
    except Exception as e:
        pytest.fail(f"Remove on out-of-bounds index raised an unexpected exception: {e}")

@pytest.mark.points(0.5)
def test_insert_invalid_indices(empty_list):
    """Test 14 (0.5 pts): Check that insert on invalid indices does nothing OR raises IndexError."""
    test_list = empty_list
    test_list.append(10)
    test_list.append(20)
    original_contents = test_list._data[:len(test_list)]

    try:
        test_list.insert(3, 99)
        assert test_list._data[:len(test_list)] == original_contents, "Insert with index > actual_size should not change the list if it doesn't raise an error."

        test_list.insert(-1, 99)
        assert test_list._data[:len(test_list)] == original_contents, "Insert with negative index should not change the list if it doesn't raise an error."
    except (IndexError, ValueError):
        pass
    except Exception as e:
        pytest.fail(f"Insert on an invalid index raised an unexpected exception: {e}")