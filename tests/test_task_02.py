"""Відкриті приклади 02 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(2)

PUBLIC = [('api_violations',
  ('modmono',
   [('modmono.lending.service', 'modmono.catalog.api'),
    ('modmono.lending.service', 'modmono.catalog.internal.repo'),
    ('modmono.app.main', 'modmono.catalog.internal.repo'),
    ('modmono.lending.service', 'json'),
    ('modmono.members.api', 'modmono.shared.events')]),
  ['modmono.lending.service -> modmono.catalog.internal.repo: імпорт нутрощів модуля catalog']),
 ('api_violations',
  ('modmono',
   [('modmono.notifications.handlers', 'modmono.lending.events'),
    ('modmono.notifications.handlers', 'modmono.lending.domain'),
    ('modmono.notifications.handlers', 'modmono.lending')],
   ('api', 'events')),
  ['modmono.notifications.handlers -> modmono.lending.domain: імпорт нутрощів модуля lending'])]


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
    for name in ('api_violations',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
