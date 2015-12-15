# content of test_sample.py
from hloader.config import Config

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4


def test_configuration_is_found():
    print(Config.CLUSTER_BASE_PATH)
    assert Config.CLUSTER_BASE_PATH == "/user/playground"
