from retirement.domain import Person

def test_age():
    assert Person("Jeff",1960).age(2026)==66
