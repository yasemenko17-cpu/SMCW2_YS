"""Відкриті приклади 07 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(7)

PUBLIC = [('change_locality',
  ([['catalog_ui', 'catalog_logic', 'catalog_db'],
    ['readers_ui', 'readers_logic'],
    ['catalog_logic']],
   {'catalog_ui': 'ui-service',
    'readers_ui': 'ui-service',
    'catalog_logic': 'logic-service',
    'readers_logic': 'logic-service',
    'catalog_db': 'data-service',
    'readers_db': 'data-service'}),
  {'per_change': [3, 2, 1],
   'average': 2.0,
   'cross_service': 2,
   'worst': 3,
   'most_changed': 'logic-service'}),
 ('change_locality',
  ([['catalog_ui', 'catalog_logic', 'catalog_db'],
    ['readers_ui', 'readers_logic'],
    ['catalog_logic']],
   {'catalog_ui': 'catalog',
    'catalog_logic': 'catalog',
    'catalog_db': 'catalog',
    'readers_ui': 'readers',
    'readers_logic': 'readers',
    'readers_db': 'readers'}),
  {'per_change': [1, 1, 1],
   'average': 1.0,
   'cross_service': 0,
   'worst': 1,
   'most_changed': 'catalog'})]


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
    for name in ('change_locality',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
