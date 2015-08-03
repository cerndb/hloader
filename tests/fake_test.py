import pytest


def sys_exit():
    raise SystemExit(1)


def test_success():
    with pytest.raises(SystemExit):
        quit()
