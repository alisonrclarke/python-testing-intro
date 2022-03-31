import pytest
from main import get_grid_size

grid_size_data = [
    (9, 3),  # square number
    (16, 4), # square number
    (10, 4), # 1 bigger than square - should round up
    (15, 4)  # 1 smaller than square - should round up
]

@pytest.mark.parametrize("data_size,expected", grid_size_data)
def test_get_grid_size(data_size, expected):
    assert get_grid_size(data_size) == expected
