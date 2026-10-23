import pytest

from testing_course.exploration.calculator import Calculator


@pytest.fixture
def calculator() -> Calculator:
    return Calculator()


def test_add_returns_correct_result(calculator: Calculator) -> None:
    # Arrange
    x = 5
    y = 2
    expected = 7

    # Act
    actual = calculator.add(x, y)

    # Assert
    assert actual == expected


def test_subtract_returns_correct_result(calculator: Calculator) -> None:
    assert calculator.subtract(5, 2) == 3


def test_divide_by_zero_raises_zero_division_error(calculator: Calculator) -> None:
    with pytest.raises(ZeroDivisionError, match="divide by zero"):
        calculator.divide(10, 0)

def multiply_cases() -> list[tuple[int, int, int]]:
    return [
        (1, 2, 2),
        (2, 5, 10),
        (3, 6, 18),
    ]

@pytest.mark.parametrize(
    ("x", "y", "expected"),
    multiply_cases()
)
def test_multiply_returns_correct_result(
calculator: Calculator, x: int, y: int, expected: int
) -> None:
    assert calculator.multiply(x, y) == expected



@pytest.mark.parametrize(
    ("x", "y", "expected"),
    [
        pytest.param(1, 2, 3, id="positive numbers"),
        pytest.param(-4, -6, -10, id="negative numbers"),
        pytest.param(-2, 2, 0, id="mixed signs"),
        pytest.param(0.1, 0.2, 0.3, id="floating point numbers"),
        pytest.param(10**3, 1, 1001, id="large numbers"),
    ]
)
def test_add_returns_sum(
        calculator: Calculator,
        x: int, y: int, expected: int
    ):
    assert calculator.add(x, y) == pytest.approx(expected) 
