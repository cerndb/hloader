# content of test_sample.py
from hloader.config import config

def func(x):
    return x + 1

def test_answer():
    assert func(3) == 4
