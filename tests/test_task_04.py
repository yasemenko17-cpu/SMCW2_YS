"""Відкриті приклади 04 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(4)

PUBLIC = [('choose_patterns',
  ({'remote': True,
    'transient_errors': True,
    'idempotent': True,
    'long_outages': True,
    'excess_traffic': False},),
  ['Circuit Breaker', 'Retry', 'Timeout']),
 ('choose_patterns', ({'remote': True, 'transient_errors': True},), ['Timeout'])]


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
    for name in ('choose_patterns',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
