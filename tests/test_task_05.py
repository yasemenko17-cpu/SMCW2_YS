"""Відкриті приклади 05 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(5)

PUBLIC = [('ring_violations',
  (['entities', 'usecases', 'adapters', 'frameworks'],
   {'cleanapp.entities.resource': 'entities',
    'cleanapp.usecases.reserve': 'usecases',
    'cleanapp.adapters.presenter': 'adapters',
    'cleanapp.frameworks.main': 'frameworks',
    'cleanapp.usecases.gateway': 'usecases',
    'cleanapp.adapters.gateway_sqlite': 'adapters'},
   [('cleanapp.usecases.reserve', 'cleanapp.entities.resource'),
    ('cleanapp.usecases.reserve', 'cleanapp.adapters.presenter'),
    ('cleanapp.entities.resource', 'sqlite3'),
    ('cleanapp.frameworks.main', 'cleanapp.usecases.reserve')],
   {'entities': ['sqlite3', 'json'], 'usecases': ['sqlite3']}),
  ['cleanapp.usecases.reserve -> cleanapp.adapters.presenter: внутрішнє коло (usecases) знає '
   'зовнішнє (adapters)',
   'cleanapp.entities.resource імпортує sqlite3: інфраструктура у внутрішньому колі (entities)']),
 ('ring_violations',
  (['entities', 'usecases', 'adapters', 'frameworks'],
   {'cleanapp.entities.resource': 'entities',
    'cleanapp.usecases.reserve': 'usecases',
    'cleanapp.adapters.presenter': 'adapters',
    'cleanapp.frameworks.main': 'frameworks',
    'cleanapp.usecases.gateway': 'usecases',
    'cleanapp.adapters.gateway_sqlite': 'adapters'},
   [('cleanapp.adapters.gateway_sqlite', 'cleanapp.usecases.gateway'),
    ('cleanapp.frameworks.main', 'cleanapp.adapters.gateway_sqlite')],
   {'entities': ['sqlite3', 'json'], 'usecases': ['sqlite3']},
   [('cleanapp.usecases.gateway', 'cleanapp.adapters.gateway_sqlite'),
    ('cleanapp.usecases.reserve', 'cleanapp.adapters.gateway_sqlite'),
    ('cleanapp.adapters.presenter', 'cleanapp.adapters.gateway_sqlite')]),
  ['cleanapp.adapters.gateway_sqlite реалізує порт з cleanapp.adapters.presenter: порт (adapters) '
   'не лежить глибше за реалізацію (adapters)'])]


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
    for name in ('ring_violations',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
