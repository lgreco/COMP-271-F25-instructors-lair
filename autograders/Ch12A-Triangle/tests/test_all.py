"""
First draw the requested UML Diagram using inheritance. Then, implement your code and test it.  Be certain the code and UML diagram match.

Turn in here:

    A pic of your UML diagram (use paper and take a pic with your phone; show both classes)
    A .py file of your code.
    A screenshot of your code running with the textbook Run button (showing your output) AFTER you pass the Automatic Check.

To calculate the area of a triangle, given three side (not necessarily a right triangle) use Heron's Formula (the reference in the textbook is incorrect):

Given the lengths of the three sides, say a, b, c

Calculate the semi-perimeter which is the sum of the lengths of the three sides divided by 2  s = (a+b+c)/2

Calculate the area as the square root of the quantity s*(s-a)*(s-b)*(s-c)

12.1 (The Triangle class) Design a class named  that extends the GeometricObject class.
The Triangle class contains:
    Three float data fields named side1, side2, and side3 are used to denote the three sides of the triangle.
    A constructor creates a triangle with the specified side1, side2, and side3 with default values 1.0
    The accessor methods for all three data fields
    A method named getArea returns the area of this triangle.
    A method named getPerimeter returns the perimeter of this triangle.
    A method named __str__ returns a string description for the triangle..

Draw the UML diagrams for the classes  and  Implement the  class.
Write a test program that prompts the user to enter the three sides of the triangle, a color, and  or  to indicate whether the triangle is filled.
The program should create a  object with these sides and set the  and  properties using the input.
The program should display the triangle’s area, perimeter, color, and  or  to indicate whether the triangle is filled or not.

"""
import inspect
import pytest


def required_init_args(cls):
    """Return list of required parameters for cls.__init__ (excluding self)."""
    sig = inspect.signature(cls.__init__)
    required = []
    all_params = []
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if param.default is inspect.Parameter.empty:
            required.append(name)
        all_params.append(name)
    return required, all_params


def get_side(triangle, i: int) -> float:
    if hasattr(triangle, f'get_side{i}'):
        return getattr(triangle, f'get_side{i}')()
    elif hasattr(triangle, f'side{i}'):
        if callable(getattr(triangle, f'side{i}')):
            return getattr(triangle, f'side{i}')()
        else:
            return getattr(triangle, f"side{i}")
    elif hasattr(triangle, f'getSide{i}'):
        return getattr(triangle, f'getSide{i}')()

def get_attribute(tri, attr_name):
    if attr_name == 'filled':
        if hasattr(tri, 'isFilled'):
            attr_name = 'isFilled'
        elif hasattr(tri, 'is_filled'):
            attr_name = 'is_filled'
        else:
            attr_name = None
    else:
        if hasattr(tri, f'get_{attr_name}'):
            attr_name = f'get_{attr_name}'
        elif hasattr(tri, f'get{attr_name.title()}'):
            attr_name = f'get{attr_name.title()}'
        else:
            print(f"Getter {attr_name} not implemented for {tri}.")
            attr_name = None
    attr = None if attr_name is None else getattr(tri, attr_name)()
    return attr

def init_triangle(student_module, side1, side2, side3):
    """
    Initialize a triangle object
    """
    required_params, all_params = required_init_args(student_module.Triangle)
    if len(all_params) == 3:
        return student_module.Triangle(side1=side1, side2=side2, side3=side3)
    elif len(all_params) == 5:
        return student_module.Triangle(side1=side1, side2=side2, side3=side3, color='mauve', filled=False)
    else:
        raise NotImplementedError(f"Triangle initialization not implemented for {student_module.Triangle}, params: {all_params}.")

@pytest.mark.points(1)
def test_default_values(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    tri = student_module.Triangle()
    assert get_side(tri, 1) == pytest.approx(1), f'Side1 should be 1, got: {get_side(tri, 1)}'
    assert get_side(tri, 2) == pytest.approx(1), f'Side2 should be 1, got: {get_side(tri, 2)}'
    assert get_side(tri, 3) == pytest.approx(1), f'Side3 should be 1, got: {get_side(tri, 3)}'

@pytest.mark.points(1)
def test_area(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    tri = init_triangle(student_module, side1=1.20, side2=2.35, side3=3)
    # tri = student_module.Triangle(side1=1.20, side2=2.35, side3=3)
    ar = 1.3147764484409503
    tri_area = get_attribute(tri, 'area')
    assert tri_area == pytest.approx(ar), f'Area should be 1.314, got: {tri_area}'

@pytest.mark.points(1)
def test_perimeter(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    # tri = student_module.Triangle(side1=1.20, side2=2.35, side3=3)
    tri = init_triangle(student_module, side1=1.20, side2=2.35, side3=3)
    per = sum([1.20, 2.35, 3])
    tri_per = get_attribute(tri, 'perimeter')
    assert tri_per == pytest.approx(per), f'Area should be 1.34, got: {tri_per}'


@pytest.mark.points(1)
def test_str_method(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    # tri = student_module.Triangle(side1=3, side2=4, side3=5)
    tri = init_triangle(student_module, side1=3, side2=4, side3=5)
    s1, s2, s3 = get_side(tri, 1), get_side(tri, 2), get_side(tri, 3)
    assert str(tri).replace(',', '') == f'Triangle: side1 = {s1} side2 = {s2} side3 = {s3}', f'__str__ method returned {str(tri)!r}'


# check the filled and color
@pytest.mark.points(1)
def test_color(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    # tri = student_module.Triangle(side1=3, side2=4, side3=5)
    tri = init_triangle(student_module, side1=3, side2=4, side3=5)
    if hasattr(tri, 'setColor'):
        tri.setColor('lilac')
    elif hasattr(tri, 'set_color'):
        tri.set_color('lilac')
    color = get_attribute(tri, 'color')
    assert color == 'lilac', f'Color should be lilac, got: {color!r}'

@pytest.mark.points(1)
def test_filled(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    tri1 = init_triangle(student_module, side1=3, side2=4, side3=5)
    tri2 = init_triangle(student_module, side1=3, side2=4, side3=5)
    # tri1 = student_module.Triangle(side1=3, side2=4, side3=5)
    # tri2 = student_module.Triangle(side1=3, side2=4, side3=5)

    if hasattr(tri1, 'setFilled'):
        tri1.setFilled(True)
        tri2.setFilled(False)
    elif hasattr(tri2, 'set_filled'):
        tri1.set_filled(True)
        tri2.set_filled(False)
    tri1_isfilled = get_attribute(tri1, 'filled')
    assert tri1_isfilled == True, f'Filled should be True, got: {tri1_isfilled}'

    tri2_isfilled = get_attribute(tri2, "filled")
    assert tri2_isfilled == False, f"Filled should be False, got: {tri2_isfilled}"

@pytest.mark.points(1)
def test_constructor_num_params(student_module, fake_inputs):
    fake_inputs([1, 2, 3, "lilac", "1"])   # these replace 3 calls to input()
    required_params, all_params = required_init_args(student_module.Triangle)

    assert len(all_params) == 3, f'The constructor should have 3 parameters, got: {len(all_params)}.'

