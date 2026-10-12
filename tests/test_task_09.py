"""Відкриті приклади 09 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(9)

PUBLIC = [('analyze_project',
  ({'modmono.catalog.api': 'from modmono.catalog.repo import ResourceRepo\n',
    'modmono.catalog.repo': 'import sqlite3\n',
    'modmono.lending.service': 'from modmono.catalog.api import CatalogApi\n'
                               'from modmono.members import api\n'
                               'from modmono.catalog.repo import ResourceRepo\n',
    'modmono.members.api': 'from modmono.lending.api import LendingApi\n',
    'modmono.lending.api': 'from modmono.members.api import MembersApi\n',
    'modmono.app.main': 'from modmono.catalog.repo import ResourceRepo\n'},
   'modmono',
   {'lending': ['catalog', 'members'], 'members': [], 'catalog': [], 'notifications': ['lending']}),
  {'edges': ['lending -> catalog', 'lending -> members', 'members -> lending'],
   'violations': ['modmono.lending.service -> modmono.catalog.repo: імпорт нутрощів модуля catalog',
                  'modmono.members.api -> modmono.lending.api: залежність members -> lending не '
                  'дозволена'],
   'cycles': [['lending', 'members']]}),
 ('analyze_project',
  ({'modmono.notifications.handlers': 'import json\n'
                                      'from . import helpers\n'
                                      'from .local import thing\n'
                                      'def on_event():\n'
                                      '    import modmono.lending.domain as d\n'
                                      '    from modmono.shared.events import Bus\n'
                                      '    return d\n',
    'modmono.lending.api': 'import modmono.catalog.api\n'
                           'import modmono.members.api, modmono.members.model\n',
    'modmono.cli.run': 'from modmono.lending.internal.repo import X\n'},
   'modmono',
   {'lending': ['catalog', 'members'], 'members': [], 'catalog': [], 'notifications': ['lending']}),
  {'edges': ['lending -> catalog',
             'lending -> members',
             'notifications -> lending',
             'notifications -> shared'],
   'violations': ['modmono.lending.api -> modmono.members.model: імпорт нутрощів модуля members',
                  'modmono.notifications.handlers -> modmono.lending.domain: імпорт нутрощів '
                  'модуля lending'],
   'cycles': []})]


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
    for name in ('analyze_project',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
