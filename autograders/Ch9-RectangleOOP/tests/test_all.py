import pytest

@pytest.mark.points(1)
def test_default_width(student_module):
    rect = student_module.Rectangle()
    ## check if rect object has a getWidth or get_width method
    if hasattr(rect, 'getWidth'):
        assert rect.getWidth() == pytest.approx(1.0), "Default width should be 1.0"
    elif hasattr(rect, 'get_width'):
        assert rect.get_width() == pytest.approx(1.0), "Default width should be 1.0"
    elif hasattr(rect, 'width'):
        assert rect.width == pytest.approx(1.0), "Default width should be 1.0"
    else: 
        pytest.fail("Rectangle class must have a public attribute width, or a getWidth or a get_width method")

@pytest.mark.points(1)
def test_default_height(student_module):
    rect = student_module.Rectangle()
    if hasattr(rect, 'getHeight'):
        assert rect.getHeight() == pytest.approx(2.0), "Default height should be 2.0"
    elif hasattr(rect, 'get_height'):
        assert rect.get_height() == pytest.approx(2.0), "Default height should be 2.0"
    elif hasattr(rect, 'height'):
        assert rect.height == pytest.approx(2.0), "Default height should be 2.0"
    else:
        pytest.fail("Rectangle class must have a public height attribute or a getHeight or get_height method")

# similarly for getArea and get_area
@pytest.mark.points(1)
def test_area(student_module):
    rect = student_module.Rectangle(width=2.0, height=4.5)
    if hasattr(rect, 'getArea'):
        assert rect.getArea()==pytest.approx(9.0), "Area should be 9.0"
    elif hasattr(rect, 'get_area'):
        assert rect.get_area()==pytest.approx(9.0), "Area should be 9.0"
    elif hasattr(rect, 'area'):
        assert rect.area()==pytest.approx(9.0), "Area should be 9.0"
    else:
        pytest.fail("Rectangle class must have a getArea or get_area method")

@pytest.mark.points(1)
def test_perimeter(student_module):
    rect = student_module.Rectangle(width=2.0, height=4.5)
    if hasattr(rect, 'getPerimeter'):
        assert rect.getPerimeter()==pytest.approx(13.0), "Perimeter should be 13.0"
    elif hasattr(rect, 'get_perimeter'):
        assert rect.get_perimeter()==pytest.approx(13.0), "Perimeter should be 13.0"
    elif hasattr(rect, 'perimeter'):
        assert rect.perimeter()==pytest.approx(13.0), "Perimeter should be 13.0"
    else:
        pytest.fail("Rectangle class must have a getPerimeter or get_perimeter method")

@pytest.mark.points(0.25)
def test_negative_width(student_module):
    rect = student_module.Rectangle(width=-4.5, height=4.5)
    if hasattr(rect, 'getWidth'):
        assert rect.getWidth()==pytest.approx(1), "Negative width should reset to 1.0"
    elif hasattr(rect, 'get_width'):
        assert rect.get_width()==pytest.approx(1), "Negative width should reset to 1.0"
    elif hasattr(rect, 'width'):
        assert rect.width==pytest.approx(1), "Negative width should reset to 1.0"
    else:
        pytest.fail("Rectangle class must have a getWidth or get_width method")
    
@pytest.mark.points(0.25)
def test_negative_height(student_module):
    rect = student_module.Rectangle(width=1, height=-4.5)
    if hasattr(rect, 'getHeight'):
        assert rect.getHeight()==pytest.approx(2) or rect.getHeight()==pytest.approx(1), "Negative height should reset to 1.0 or 2.0"
    elif hasattr(rect, 'get_height'):
        assert rect.get_height()==pytest.approx(2) or rect.get_height()==pytest.approx(1), "Negative height should reset to 1.0 or 2.0"
    elif hasattr(rect, 'height'):
        assert rect.height==pytest.approx(2) or rect.height==pytest.approx(1), "Negative height should reset to 1.0 or 2.0"
    else:
        pytest.fail("Rectangle class must have a getHeight or get_height method")


@pytest.mark.points(0.25)
def test_zero_height(student_module):
    rect = student_module.Rectangle(width=4.5, height=0)
    if hasattr(rect, 'getHeight'):
        assert rect.getHeight()==pytest.approx(0), "Zero height should be allowed"
    elif hasattr(rect, 'get_height'):
        assert rect.get_height()==pytest.approx(0), "Zero height should be allowed"
    elif hasattr(rect, 'height'):
        assert rect.heightpytest.approx(0), "Zero height should be allowed"
    else:
        pytest.fail("Rectangle class must have a getHeight or get_height method")
    #
    
@pytest.mark.points(0.25)
def test_zero_width(student_module):
    rect = student_module.Rectangle(width=0, height=3.5)
    if hasattr(rect, 'getWidth'):
        assert rect.getWidth()==pytest.approx(0), "Zero width should be allowed"
    elif hasattr(rect, 'get_width'):
        assert rect.get_width()==pytest.approx(0), "Zero width should be allowed"
    elif hasattr(rect, 'width'):
        assert rect.width==pytest.approx(0), "Zero width should be allowed"
    else:       
        pytest.fail("Rectangle class must have a getWidth or get_width method")