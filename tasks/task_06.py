import re

def table_violations(queries: dict, modules: list[str]) -> list[str]:
    for mod in queries.keys():
        if mod not in modules:
            raise ValueError(f"Невідомий модуль: {mod}")
            
    table_name_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
    ignore_words = {'select', 'values', 'set', 'exists', 'if', 'not'}
    
    violations = []
    
    for mod, q_list in queries.items():
        for q_idx, query in enumerate(q_list, 1):
            words = query.split()
            seen_tables_in_query = set()
            
            i = 0
            while i < len(words):
                w = words[i]
                w_upper = w.upper()
                
                target_word_idx = -1
                if w_upper in ('FROM', 'JOIN', 'INTO', 'UPDATE', 'TABLE'):
                    if i + 1 < len(words):
                        target_word_idx = i + 1
                        if w_upper == 'TABLE' and i + 3 < len(words) and words[i+1].upper() == 'IF' and words[i+2].upper() == 'NOT' and words[i+3].upper() == 'EXISTS':
                            if i + 4 < len(words):
                                target_word_idx = i + 4
                                
                if target_word_idx != -1 and target_word_idx < len(words):
                    raw_tbl = words[target_word_idx].strip('(),;')
                    tbl_lower = raw_tbl.lower()
                    if table_name_pattern.match(raw_tbl) and tbl_lower not in ignore_words:
                        if tbl_lower not in seen_tables_in_query:
                            seen_tables_in_query.add(tbl_lower)
                            
                            is_own = tbl_lower.startswith(mod.lower() + '_')
                            if not is_own:
                                owner = None
                                max_len = 0
                                for m in modules:
                                    if tbl_lower.startswith(m.lower() + '_') and len(m) > max_len:
                                        owner = m
                                        max_len = len(m)
                                        
                                if owner:
                                    msg = f"{mod}[{q_idx}]: SQL зачіпає таблицю {raw_tbl}, що не належить модулю {mod} (власник: {owner})"
                                else:
                                    msg = f"{mod}[{q_idx}]: SQL зачіпає таблицю {raw_tbl}, що не належить модулю {mod} (власника немає)"
                                    
                                if msg not in violations:
                                    violations.append(msg)
                i += 1
                
    return violations