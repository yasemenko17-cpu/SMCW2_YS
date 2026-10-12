import ast

def analyze_project(
    sources: dict,
    package: str,
    allowed: dict,
    public: tuple = ("api",),
    roots: tuple = ("app", "cli"),
    open_units: tuple = ("shared",)
) -> dict:
    sorted_mods = sorted(sources.keys())
    import_records = []
    
    # Обробляємо модулі у порядку зростання повного імені
    for mod_name in sorted_mods:
        code = sources[mod_name]
        parts = mod_name.split('.')
        if len(parts) < 2 or parts[0] != package:
            continue
        block = parts[1]
        if block in roots:
            continue
            
        try:
            tree = ast.parse(code)
        except SyntaxError:
            raise ValueError(f"Синтаксична помилка у модулі {mod_name}")
            
        mod_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    target = alias.name
                    mod_imports.append((node.lineno, node.col_offset, mod_name, block, target))
            elif isinstance(node, ast.ImportFrom):
                if node.level and node.level > 0:
                    continue
                if node.module:
                    base = node.module
                    base_parts = base.split('.')
                    if len(base_parts) <= 2:
                        for alias in node.names:
                            target = f"{base}.{alias.name}"
                            mod_imports.append((node.lineno, node.col_offset, mod_name, block, target))
                    else:
                        target = base
                        mod_imports.append((node.lineno, node.col_offset, mod_name, block, target))
                        
        # Сортуємо імпорти всередині конкретного модуля за рядком та стовпчиком
        mod_imports.sort(key=lambda x: (x[0], x[1]))
        import_records.extend(mod_imports)
        
    edges_set = set()
    violations = []
    
    for lineno, col, src_mod, src_block, tgt in import_records:
        tgt_parts = tgt.split('.')
        if len(tgt_parts) < 2 or tgt_parts[0] != package:
            continue
        tgt_block = tgt_parts[1]
        if tgt_block in roots:
            continue
        if src_block == tgt_block:
            continue
            
        edge_str = f"{src_block} -> {tgt_block}"
        edges_set.add(edge_str)
        
        if tgt_block in open_units:
            continue
            
        allowed_blocks = allowed.get(src_block, [])
        if tgt_block not in allowed_blocks:
            msg = f"{src_mod} -> {tgt}: залежність {src_block} -> {tgt_block} не дозволена"
            if msg not in violations:
                violations.append(msg)
        else:
            if len(tgt_parts) > 2 and tgt_parts[2] not in public:
                msg = f"{src_mod} -> {tgt}: імпорт нутрощів модуля {tgt_block}"
                if msg not in violations:
                    violations.append(msg)
                    
    edges = sorted(list(edges_set))
    
    adj = {}
    all_blocks = set()
    for e in edges:
        u, v = e.split(' -> ')
        all_blocks.add(u)
        all_blocks.add(v)
        adj.setdefault(u, set()).add(v)
        
    index_counter = [0]
    stack = []
    indices = {}
    lowlink = {}
    on_stack = {}
    sccs = []
    
    def strongconnect(node):
        indices[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack[node] = True
        
        for neighbor in sorted(adj.get(node, [])):
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif on_stack.get(neighbor, False):
                lowlink[node] = min(lowlink[node], indices[neighbor])
                
        if lowlink[node] == indices[node]:
            scc = []
            while True:
                n = stack.pop()
                on_stack[n] = False
                scc.append(n)
                if n == node:
                    break
            if len(scc) >= 2:
                sccs.append(sorted(scc))
                
    for b in sorted(list(all_blocks)):
        if b not in indices:
            strongconnect(b)
            
    sccs.sort()
    
    return {
        "edges": edges,
        "violations": violations,
        "cycles": sccs
    }