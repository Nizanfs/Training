import midas


def test_adding_terorist():
    new_terrorist = midas.add_terrorist('a', 'b', 'c', 'd')
    terrorist = midas.get_terrorist(new_terrorist.id)
    assert terrorist is not None
    assert terrorist.name == new_terrorist.name
    assert terrorist.last_name == new_terrorist.last_name
    assert terrorist.role == new_terrorist.role
    assert terrorist.location == new_terrorist.location
