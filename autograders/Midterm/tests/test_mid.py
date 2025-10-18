import pytest
import inspect
import types
from typing import get_origin, get_args, Union

# --- Agnostic Helper Functions ---
# These helpers now cast list-based pointers to tuples to ensure fair comparison.

def _get_front_pos(q) -> tuple[int, int]:
    """Gets the front pointer's (row, col) position, accommodating tuple and list implementations."""
    if hasattr(q, '_front'):
        return tuple(q._front)  # Cast to tuple to handle both [r, c] and (r, c)
    elif hasattr(q, '_front_row') and hasattr(q, '_front_col'):
        return (q._front_row, q._front_col)
    else:
        pytest.fail("Could not find front pointer attributes (`_front` or `_front_row`/`_front_col`).")

def _get_back_pos(q) -> tuple[int, int]:
    """Gets the back pointer's (row, col) position, accommodating tuple and list implementations."""
    if hasattr(q, '_back'):
        return tuple(q._back)  # Cast to tuple
    elif hasattr(q, '_back_row') and hasattr(q, '_back_col'):
        return (q._back_row, q._back_col)
    else:
        pytest.fail("Could not find back pointer attributes (`_back` or `_back_row`/`_back_col`).")

# --- Rubric: Type Annotations (2.0 points total) ---
METHOD_ANNOTATIONS = {
    'enqueue': {'value': str, 'return': bool},
    'dequeue': {'return': str},
    'peek': {'return': str},
    '__repr__': {'return': str},
    '__bool__': {'return': bool},
    'get_usage': {'return': int},
    'get_capacity': {'return': int},
}
annotations_to_test = [(m, a, t) for m, s in METHOD_ANNOTATIONS.items() for a, t in s.items()]

@pytest.mark.points(2.0 / len(annotations_to_test))
@pytest.mark.parametrize("method_name, arg_name, expected_base_type", annotations_to_test)
def test_method_has_correct_type_annotations(My2DQueue_class, method_name, arg_name, expected_base_type):
    method = getattr(My2DQueue_class, method_name)
    full_spec = inspect.getfullargspec(method)
    assert arg_name in full_spec.annotations, f"Missing annotation for '{arg_name}' in `{method_name}`."
    received_type = full_spec.annotations[arg_name]
    origin_type = get_origin(received_type)
    if origin_type is Union or isinstance(received_type, types.UnionType):
        union_args = get_args(received_type)
        assert expected_base_type in union_args, \
            f"Incorrect annotation for '{arg_name}' in `{method_name}`. Expected: `{expected_base_type}` to be part of the Union. Got: `{received_type}`."
    else:
        assert received_type == expected_base_type, \
            f"Incorrect annotation for '{arg_name}' in `{method_name}`. Expected: `{expected_base_type}`. Got: `{received_type}`."

# --- Rubric: Behavioral and Functional Tests (13.0 points total) ---
@pytest.fixture
def empty_q_2x2(My2DQueue_class): return My2DQueue_class(n=2)
@pytest.fixture
def full_q_2x2(My2DQueue_class):
    q = My2DQueue_class(n=2)
    q.enqueue('Abby'); q.enqueue('Beth'); q.enqueue('Charlie'); q.enqueue('David')
    return q
@pytest.fixture
def q_3x3(My2DQueue_class): return My2DQueue_class(n=3)

@pytest.mark.points(1.0)
def test_required_getters(My2DQueue_class):
    q = My2DQueue_class(n=3)
    assert hasattr(q, 'get_usage'), "The required method `get_usage` is missing."
    assert hasattr(q, 'get_capacity'), "The required method `get_capacity` is missing."
    q.enqueue("Test")
    usage = q.get_usage()
    capacity = q.get_capacity()
    assert usage == 1, f"get_usage() returned incorrect value. Expected: 1. Got: {usage}."
    assert capacity == 9, f"get_capacity() returned incorrect value. Expected: 9. Got: {capacity}."

@pytest.mark.points(1.0)
def test_initial_state_and_peek(My2DQueue_class):
    q = My2DQueue_class(n=4)
    assert q._capacity == 16, f"Initial capacity is incorrect. Expected: 16. Got: {q._capacity}."
    assert q._usage == 0, f"Initial usage is incorrect. Expected: 0. Got: {q._usage}."
    assert q.peek() is None, f"peek() on empty queue failed. Expected: None. Got: {q.peek()}."

@pytest.mark.points(1.0)
def test_enqueue_behavior(empty_q_2x2, full_q_2x2):
    q = empty_q_2x2
    q.enqueue('Abby')
    assert q._usage == 1, f"Usage after one enqueue failed. Expected: 1. Got: {q._usage}."
    assert q.peek() == 'Abby', f"peek() after one enqueue failed. Expected: 'Abby'. Got: {q.peek()}."
    enqueue_result = full_q_2x2.enqueue('Emma')
    assert not enqueue_result, f"enqueue() on full queue should return False. Expected: False. Got: {enqueue_result}."

@pytest.mark.points(1.0)
def test_dequeue_behavior(empty_q_2x2, full_q_2x2):
    dequeue_result = empty_q_2x2.dequeue()
    assert dequeue_result is None, f"dequeue() on empty queue failed. Expected: None. Got: {dequeue_result}."
    item = full_q_2x2.dequeue()
    assert item == 'Abby', f"dequeue() returned wrong item. Expected: 'Abby'. Got: {item}."
    assert full_q_2x2._usage == 3, f"Usage after dequeue failed. Expected: 3. Got: {full_q_2x2._usage}."

@pytest.mark.points(1.25)
def test_2x2_wrap_around_logic(My2DQueue_class):
    q = My2DQueue_class(n=2)
    q.enqueue('Abby'); q.enqueue('Beth'); q.dequeue()
    q.enqueue('Charlie'); q.enqueue('David')
    expected_list = ['Beth', 'Charlie', 'David']
    assert q.list_queue() == expected_list, f"list_queue() after back-wrap failed for n=2. Expected: {expected_list}. Got: {q.list_queue()}."
    q.dequeue(); q.dequeue(); q.dequeue()
    q.enqueue('Emma')
    assert q.peek() == 'Emma', f"peek() after front-wrap failed for n=2. Expected: 'Emma'. Got: {q.peek()}."
    expected_front = (0, 0)
    actual_front = _get_front_pos(q)
    assert actual_front == expected_front, f"Front pointer after wrap is incorrect for n=2. Expected: {expected_front}. Got: {actual_front}."

@pytest.mark.points(1.25)
def test_3x3_wrap_around_logic(q_3x3):
    q = q_3x3
    names = ['Abby', 'Beth', 'Charlie', 'David', 'Emma', 'Frank', 'Grace', 'Heidi', 'Ivan']
    for name in names:
        q.enqueue(name)
    assert q._usage == 9, f"Usage should be 9 after filling 3x3 queue. Got: {q._usage}"
    for _ in range(8):
        q.dequeue()
    assert q.peek() == 'Ivan', f"peek() before final dequeue is wrong. Expected: 'Ivan'. Got: {q.peek()}"
    q.dequeue()
    assert q._usage == 0, "Queue should be empty after all items are dequeued."
    q.enqueue('Judy')
    expected_front = (0, 0)
    actual_front = _get_front_pos(q)
    assert actual_front == expected_front, f"Front pointer after 3x3 wrap is incorrect. Expected: {expected_front}. Got: {actual_front}."
    assert q.peek() == 'Judy', "peek() after 3x3 wrap and re-queue is incorrect."

@pytest.mark.points(1.5)
def test_list_queue_on_wrap(full_q_2x2):
    q = full_q_2x2
    q.dequeue(); q.dequeue()
    q.enqueue('Emma'); q.enqueue('Frank')
    expected_order = ['Charlie', 'David', 'Emma', 'Frank']
    actual_order = q.list_queue()
    assert actual_order == expected_order, f"list_queue() with wrap-around failed. Expected: {expected_order}. Got: {actual_order}."

@pytest.mark.points(0.5)
def test_bool_special_method(empty_q_2x2):
    assert not bool(empty_q_2x2), f"__bool__ on empty queue failed. Expected: False. Got: {bool(empty_q_2x2)}."
    empty_q_2x2.enqueue("Grace")
    assert bool(empty_q_2x2), f"__bool__ on non-empty queue failed. Expected: True. Got: {bool(empty_q_2x2)}."

@pytest.mark.points(0.5)
def test_repr_special_method(empty_q_2x2):
    empty_q_2x2.enqueue("Grace")
    try:
        representation = repr(empty_q_2x2)
        assert isinstance(representation, str), f"__repr__ should return a string. Got: {type(representation)}."
        assert len(representation) > 5, "__repr__ string seems too short or empty."
    except Exception as e:
        pytest.fail(f"Calling repr() on the queue raised an unexpected error: {e.__class__.__name__}: {e}")

# --- Granular Invariant Tests (Now Implementation-Agnostic) ---
@pytest.mark.points(1.0)
@pytest.mark.parametrize("n", [2, 3])
def test_invariant_pointers_equal_on_empty(My2DQueue_class, n):
    q = My2DQueue_class(n=n)
    q.enqueue('Abby'); q.enqueue('Beth')
    q.dequeue(); q.dequeue()
    assert q._usage == 0, f"Test setup for n={n} failed, queue is not empty."
    expected_pos = _get_back_pos(q)
    actual_pos = _get_front_pos(q)
    assert actual_pos == expected_pos, \
        f"Invariant Failed on empty queue (n={n}). Expected front and back pointers to be equal. Expected: {expected_pos}. Got: {actual_pos}."

@pytest.mark.points(0.75)
def test_invariant_pointers_equal_on_full(full_q_2x2):
    q = full_q_2x2
    assert q._usage == q._capacity, "Test setup failed, queue is not full."
    expected_pos = _get_back_pos(q)
    actual_pos = _get_front_pos(q)
    assert actual_pos == expected_pos, \
        f"Invariant Failed on full queue. Expected front and back pointers to be equal. Expected: {expected_pos}. Got: {actual_pos}."

@pytest.mark.points(0.5)
def test_invariant_dequeued_cell_is_none(full_q_2x2):
    row, col = _get_front_pos(full_q_2x2)
    full_q_2x2.dequeue()
    cell_content = full_q_2x2._underlying[row][col]
    assert cell_content is None, f"Invariant Failed. Dequeued cell should be None. Expected: None. Got: {cell_content} at ({row},{col})."

@pytest.mark.points(0.75)
def test_invariant_all_cells_none_when_empty(My2DQueue_class):
    q = My2DQueue_class(n=2)
    q.enqueue('Abby'); q.enqueue('Beth'); q.enqueue('Charlie')
    q.dequeue(); q.dequeue(); q.dequeue()
    assert q._usage == 0, "Test setup failed, queue should be empty."
    for r_idx, row in enumerate(q._underlying):
        for c_idx, cell in enumerate(row):
            assert cell is None, f"Invariant Failed. After emptying, cell was not None. Expected: None. Got: '{cell}' at ({r_idx},{c_idx})."