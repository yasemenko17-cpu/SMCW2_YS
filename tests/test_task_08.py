"""Відкриті приклади 08 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(8)

PUBLIC = [('pool_analysis',
  (20, 50, {'normal': 100, 'degraded': 5000}, 2000),
  {'normal_busy': 5.0,
   'degraded_busy': 100.0,
   'utilization': 5.0,
   'verdict': 'пул вичерпано',
   'max_safe_timeout': 319}),
 ('pool_analysis',
  (20, 50, {'normal': 100, 'degraded': 5000}, 300),
  {'normal_busy': 5.0,
   'degraded_busy': 15.0,
   'utilization': 0.75,
   'verdict': 'норма',
   'max_safe_timeout': 319})]


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
    for name in ('pool_analysis',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
