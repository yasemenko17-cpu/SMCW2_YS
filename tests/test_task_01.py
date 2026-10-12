"""Відкриті приклади 01 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(1)

PUBLIC = [('layer_violations',
  ('layered',
   ['presentation', 'business', 'data'],
   [('layered.presentation.cli', 'layered.business.service'),
    ('layered.business.service', 'layered.data.repository'),
    ('layered.presentation.cli', 'layered.data.repository'),
    ('layered.presentation.cli', 'sqlite3')],
   True),
  ['layered.presentation.cli -> layered.data.repository: пропуск шару (presentation -> data)']),
 ('layer_violations',
  ('layered',
   ['presentation', 'business', 'data'],
   [('layered.presentation.cli', 'layered.business.service'),
    ('layered.business.service', 'layered.data.repository'),
    ('layered.presentation.cli', 'layered.data.repository'),
    ('layered.data.repository', 'layered.business.service')],
   False),
  ['layered.data.repository -> layered.business.service: залежність угору (data -> business)'])]


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
    for name in ('layer_violations',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
