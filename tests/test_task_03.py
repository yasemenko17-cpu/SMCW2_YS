"""Відкриті приклади 03 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(3)

PUBLIC = [('scaling_cost',
  ({'catalog': {'load': 900, 'capacity': 300, 'memory_mb': 200},
    'reservations': {'load': 60, 'capacity': 100, 'memory_mb': 300},
    'readers': {'load': 40, 'capacity': 100, 'memory_mb': 150}},
   100),
  {'instances': {'catalog': 3, 'reservations': 1, 'readers': 1},
   'microservices_mb': 1550,
   'monolith_instances': 3,
   'monolith_mb': 2250,
   'cheaper': 'мікросервіси'}),
 ('scaling_cost',
  ({'a': {'load': 50, 'capacity': 100, 'memory_mb': 50},
    'b': {'load': 50, 'capacity': 100, 'memory_mb': 50},
    'c': {'load': 50, 'capacity': 100, 'memory_mb': 50}},
   100),
  {'instances': {'a': 1, 'b': 1, 'c': 1},
   'microservices_mb': 450,
   'monolith_instances': 1,
   'monolith_mb': 250,
   'cheaper': 'моноліт'})]


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
    for name in ('scaling_cost',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
