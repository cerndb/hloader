# content of test_sample.py
from hloader.config import config

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4


def test_configuration_is_found():
    print(config.CLUSTER_BASE_PATH)
    assert config.CLUSTER_BASE_PATH == "/user/playground"
