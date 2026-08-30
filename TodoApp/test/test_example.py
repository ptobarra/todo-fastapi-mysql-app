import pytest


def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("10", int)


def test_boolean():
    validated = True
    assert validated is True
    assert ("hello" == "world") is False


def test_type():
    assert isinstance("Hello", str)
    assert not isinstance("World", int)
    # assert type("Hello" == str)
    # assert type("World" != int)


def test_greater_and_less_than():
    assert 7 > 3
    assert 4 < 10


def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    assert 1 in num_list
    assert 7 not in num_list

    assert all(num_list)
    # assert all(num_list) checks that every element in num_list ([1, 2, 3, 4, 5]) is
    # truthy.

    # all() is a Python built-in that takes an iterable and returns True only if every
    # item evaluates to truthy (non-zero, non-empty, non-None, non-False) — it returns
    # False as soon as it hits one falsy item.

    # In this case, 1, 2, 3, 4, 5 are all non-zero numbers, so every element is truthy,
    # and all (num_list) returns True. The assert then passes.

    assert not any(any_list)
    # Its sibling, assert not any(any_list), does the opposite check: any() returns
    # True if at least one element is truthy. Since any_list = [False, False] has no
    # truthy elements, any(any_list) is False, and not False is True — so that
    # assertion passes too.


class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years


# def test_person_initialization():
#     p = Student("John", "Doe", "Computer Science", 3)
#     assert p.first_name == "John", "First name should be John"
#     assert p.last_name == "Doe", "Last name should be Doe"
#     assert p.major == "Computer Science"
#     assert p.years == 3


@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 3)


def test_person_initialization(default_employee):
    assert default_employee.first_name == "John", "First name should be John"
    assert default_employee.last_name == "Doe", "Last name should be Doe"
    assert default_employee.major == "Computer Science"
    assert default_employee.years == 3
