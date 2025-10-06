"""Assignment Instructions

First, read the UML diagram attached here "Inheritance Mystery".
Second, record what you think will be printed when the test code shown runs.
Third, implement the four classes shown in the UML diagram and use the test code
Be sure to carefully match the UML diagram for each method (implement exactly what is shown in the UML diagram).
The comments give the code for each method.

For methods with more than one line, keep them in the order shown in the UML.
Finally, go back to your text document.
Don't change what you wrote before, but ADD comments to explain what is different
and why (to the best of your understanding - it may be difficult).

DON'T worry if your initial answers are different than the program when it runs.
Just note the differences and try to explain them.
You will get full points for a complete and good analysis.

Turn in:
    Your original text document with added analysis (as Word or pdf file)
    Your four Python classes as .py files.

Expected Output:
    Element 0
    Arya-a

    Oberyn

    Oberyn-b
    Arya-a
    Arya-b
    Done

    Element 1
    Arya-a

    Arya

    Arya-a
    Arya-b
    Done

    Element 2
    Brienne-a

    Oberyn

    Oberyn-b
    Brienne-a
    Arya-b
    Done

    Element 3
    Arya-a
    Tyrion-a

    Arya

    Arya-a
    Tyrion-a
    Arya-b
    Done
"""

## check for the 4 files: Arya.py, Brienne.py, Oberyn.py, Tyrion.py
## run their code and check the STDOUT

# check if there are 4 files

import pytest

# --- Structural Tests (Checking Existence and Callability) ---
EXPECTED_STR = {
    'arya': 'Arya',      # Explicitly defined
    'oberyn': 'Oberyn',  # Explicitly defined
    # Brienne and Tyrion inherit. Since Arya's __str__ returns 'Arya', they will too.
    'brienne': 'Oberyn',
    'tyrion': 'Arya',
}


def get_expected_a_output(char_name):
    """Calculate the expected print output for the a() method based on MRO."""
    char_name = char_name.lower()
    if char_name == 'arya':
        return 'Arya-a\n' # Arya.a() prints 'Arya-a'
    if char_name == 'brienne':
        return 'Brienne-a\n' # Brienne.a() prints 'Brienne-a'
    if char_name == 'oberyn':
        # Oberyn inherits Arya.a()
        return 'Arya-a\n' # Arya.a() prints 'Arya-a'
    if char_name == 'tyrion':
        # Tyrion.a() calls super().a(), then prints 'Tyrion-a'
        # super().a() (Arya.a()) prints 'Arya-a'
        return 'Arya-a\n' + 'Tyrion-a\n'
    return "" # Should not happen

def get_expected_b_output(char_name):
    """Calculate the expected print output for the b() method based on MRO."""
    char_name = char_name.lower()
    if char_name == 'arya':
        # Arya.b() calls self.a() (Arya.a()), then prints 'Arya-b'
        # self.a() (Arya.a()) prints 'Arya-a'
        return 'Arya-a\n' + 'Arya-b\n'
    if char_name == 'brienne':
        # Brienne inherits Oberyn.b()
        # Oberyn.b() prints 'Oberyn-b', then calls super().b() which is Arya.b()
        # Arya.b() calls self.a() that prints `Brienne-a`, then print('Arya-b')
        return 'Oberyn-b\n' + 'Brienne-a\n' + 'Arya-b\n'
    if char_name == 'tyrion':
        # Tyrion inherits Arya.b()
        # Tyrion.b() calls self.a() (Tyrion.a()), then prints 'Arya-b'
        # self.a() (Tyrion.a()) calls super().a() ('Arya-a'), then prints 'Tyrion-a' [cite: 19, 8]
        a_output = get_expected_a_output('tyrion')
        return a_output + 'Arya-b\n'
    if char_name == 'oberyn':
        # Oberyn.b() prints 'Oberyn-b', then calls super().b()
        # super().b() (Arya.b()) calls self.a() (Oberyn.a()), then prints 'Arya-b'
        # self.a() (Oberyn.a()) prints 'Arya-a'
        return 'Oberyn-b\n' + 'Arya-a\n' + 'Arya-b\n'
    return "" # Should not happen


# --- Test Functions ---
@pytest.mark.points(1)
def test_all_files_present(student_modules):
    """
    Check if the student modules contain separate files for Oberyn, Arya, Tyrion, and Brienne
    """
    assert len(student_modules) == 4, f'Expected 4 separate .py files, found {student_modules.keys()!r}'


@pytest.mark.points(0.25)
def test_class_instantiation(character_instance, character_name):
    """Test 1: Ensures the class can be created without crashing."""
    assert character_instance is not None

@pytest.mark.points(0.125)
@pytest.mark.parametrize("method_name", ["a", "b"])
def test_method_exists_and_is_callable(character_class, character_name, method_name):
    """Test 2: Check if required methods exist and are callable."""
    assert hasattr(character_class, method_name), f"Class {character_name} is missing the required method '{method_name}()'."
    instance = character_class()
    method_attr = getattr(instance, method_name)
    assert callable(method_attr), f"Attribute '{method_name}' in class {character_name} is not callable."


@pytest.mark.points(0.5)
def test_a_method_output(character_instance, character_name, capsys):
    """Test 3: Checks the print output of the a() method, handling polymorphism."""

    # Act: Call the method
    try:
        result = character_instance.a()
    except Exception as e:
        pytest.fail(f"Calling {character_name}.a() raised an error: {e}")

    captured = capsys.readouterr()
    captured = captured.out.strip()
    expected_output = get_expected_a_output(character_name).strip()

    # Assert: Check printed output
    assert captured == expected_output, (
        f"Method {character_name}.a() failed print test.\n"
        f"Expected Output:\n{expected_output.strip()}\n"
        f"Actual Output:\n{captured.strip()}"
    )
    # Assert: Check return value (must be None as per UML [cite: 8, 19, 32])
    assert result is None, f"Method {character_name}.a() should return None, but returned {result}."

@pytest.mark.points(0.5)
def test_b_method_output(character_instance, character_name, capsys):
    """Test 4: Checks the print output of the b() method, handling polymorphism."""

    # Act: Call the method
    try:
        result = character_instance.b()
    except Exception as e:
        pytest.fail(f"Calling {character_name}.b() raised an error: {e}")

    captured = capsys.readouterr()
    captured = captured.out.strip()
    expected_output = get_expected_b_output(character_name).strip()

    # Assert: Check printed output
    assert captured == expected_output, (
        f"Method {character_name}.b() failed print test.\n"
        f"Expected Output:\n{expected_output.strip()}\n"
        f"Actual Output:\n{captured}"
    )
    # Assert: Check return value (must be None as per UML [cite: 9, 14])
    assert result is None, f"Method {character_name}.b() should return None, but returned {result}."

@pytest.mark.points(0.25)
def test_str_method_output(character_instance, character_name):
    """Test 5: Checks the return value of the __str__ method."""
    character_name = character_name.lower()
    expected_output = EXPECTED_STR[character_name]

    # Act: Call the str() built-in function
    try:
        str_output = str(character_instance)
    except Exception as e:
        pytest.fail(f"Calling str() on {character_name!r} instance raised an error: {e}")

    # Assert: Check the return value
    assert str_output == expected_output, (
        f"The __str__ method failed for {character_name!r}.\n"
        f"Expected: '{expected_output}', but got: '{str_output}'"
    )