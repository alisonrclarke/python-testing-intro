from main import get_grid_size

def test_get_grid_size():
    assert get_grid_size(9) == 3
    assert get_grid_size(16) == 4
