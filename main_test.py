import pytest
from main import get_grid_size

grid_size_data = [
    (9, 3),
    (16, 4)
]

@pytest.mark.parametrize("data_size,expected", grid_size_data)
def test_get_grid_size(data_size, expected):
    assert get_grid_size(data_size) == expected
