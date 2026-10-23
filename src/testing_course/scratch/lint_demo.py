import pytest
from src.testing_course.scratch.calculator import Calculator


def find(name: str | None, items=None):
    if items is None:
        items = []
    if name is None:
        return False
    return name in items


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Calculator.divide(1, 0)


@pytest.mark.parametrize(("x", "y"), [1, 2])
def test_add(x, y):
    assert Calculator.add(x, y) == 3
