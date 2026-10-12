"""Відкриті приклади 10 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(10)

PUBLIC = [('simulate_limiter',
  ([100, 200, 300, 400, 900, 1000, 1100, 1200, 1900], 'fixed_window', 3, 1000),
  [(True, 0),
   (True, 0),
   (True, 0),
   (False, 600),
   (False, 100),
   (True, 0),
   (True, 0),
   (True, 0),
   (False, 100)]),
 ('peak_allowed',
  ([100, 200, 300, 400, 900, 1000, 1100, 1200, 1900],
   [(True, 0),
    (True, 0),
    (True, 0),
    (False, 600),
    (False, 100),
    (True, 0),
    (True, 0),
    (True, 0),
    (False, 100)],
   1000),
  4),
 ('simulate_limiter',
  ([100, 200, 300, 400, 900, 1000, 1100, 1200, 1900], 'token_bucket', 3, 1000),
  [(True, 0),
   (True, 0),
   (True, 0),
   (False, 34),
   (True, 0),
   (True, 0),
   (True, 0),
   (False, 234),
   (True, 0)]),
 ('peak_allowed',
  ([100, 200, 300, 400, 900, 1000, 1100, 1200, 1900],
   [(True, 0),
    (True, 0),
    (True, 0),
    (False, 34),
    (True, 0),
    (True, 0),
    (True, 0),
    (False, 234),
    (True, 0)],
   1000),
  5)]


def _check(fn, args, expected):
    if isinstance(expected, tuple) and expected and expected[0] == "ValueError":
        with pytest.raises(ValueError) as info:
            getattr(M, fn)(*copy.deepcopy(args))
        assert str(info.value) == expected[1]
    else:
        assert getattr(M, fn)(*copy.deepcopy(args)) == expected


@pytest.mark.parametrize("fn,args,expected", PUBLIC, ids=[f"p{i}" for i in range(len(PUBLIC))])
def test_public(fn, args, expected):
    _check(fn, args, expected)


def test_functions_exist():
    for name in ('simulate_limiter', 'peak_allowed'):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
