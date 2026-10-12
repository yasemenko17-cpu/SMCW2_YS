"""Відкриті приклади 06 (з картки). Повний набір перевірок — у викладача."""
import copy

import pytest
from conftest import load

M = load(6)

PUBLIC = [('table_violations',
  ({'lending': ['SELECT * FROM lending_loans WHERE member = ?',
                'SELECT title FROM lending_loans l JOIN catalog_resources r ON r.id = l.rid'],
    'notifications': ['INSERT INTO notifications_outbox VALUES (?)']},
   ['catalog', 'members', 'lending', 'notifications']),
  ['lending[2]: SQL зачіпає таблицю catalog_resources, що не належить модулю lending (власник: '
   'catalog)']),
 ('table_violations',
  ({'members': ['UPDATE members_cards SET blocked = 1 WHERE id = ?',
                'DELETE FROM audit_log WHERE ts < ?',
                'CREATE TABLE IF NOT EXISTS Members_Flags (id INTEGER)',
                'SELECT n FROM (SELECT count(*) AS n FROM lending_loans)']},
   ['catalog', 'members', 'lending', 'notifications']),
  ['members[2]: SQL зачіпає таблицю audit_log, що не належить модулю members (власника немає)',
   'members[4]: SQL зачіпає таблицю lending_loans, що не належить модулю members (власник: '
   'lending)'])]


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
    for name in ('table_violations',):
        assert callable(getattr(M, name, None)), f"немає функції {name}"
