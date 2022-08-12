from main import get_basket
import pytest


@pytest.mark.parametrize(
    "widgets_to_add,expected_total",
    [
        (["B01", "G01"], 37.85),
        (["R01", "R01"], 54.37),
        (["R01", "G01"], 60.85),
        (["B01", "B01", "R01", "R01", "R01"], 98.27),
    ],
)
def test_main(widgets_to_add, expected_total):
    basket = get_basket()
    for widget_code in widgets_to_add:
        basket.add(widget_code)

    assert f"{basket.total():.3f}"[:-1] == str(expected_total)
