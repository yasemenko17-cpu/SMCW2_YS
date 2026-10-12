def ring_violations(
    rings: list[str],
    modules: dict,
    imports: list[tuple[str, str]],
    forbidden: dict,
    ports: list[tuple[str, str]] = (),
    root: str | None = None
) -> list[str]:
    ring_indices = {ring: i for i, ring in enumerate(rings)}
    
    for mod, ring in modules.items():
        if ring not in ring_indices:
            raise ValueError(f"Невідоме коло: {ring}")
            
    for port_mod, impl_mod in ports:
        if port_mod != root and port_mod not in modules:
            raise ValueError(f"Невідомий модуль: {port_mod}")
        if impl_mod != root and impl_mod not in modules:
            raise ValueError(f"Невідомий модуль: {impl_mod}")
            
    for src, tgt in imports:
        if src != root and src not in modules:
            raise ValueError(f"Невідомий модуль: {src}")
            
    violations = []
    
    for src, tgt in imports:
        if src == root:
            continue
        src_ring = modules[src]
        src_idx = ring_indices[src_ring]
        
        if tgt in modules:
            tgt_ring = modules[tgt]
            tgt_idx = ring_indices[tgt_ring]
            if tgt_idx > src_idx:
                msg = f"{src} -> {tgt}: внутрішнє коло ({src_ring}) знає зовнішнє ({tgt_ring})"
                if msg not in violations:
                    violations.append(msg)
        else:
            tgt_first = tgt.split('.')[0]
            if tgt_first in forbidden.get(src_ring, []):
                msg = f"{src} імпортує {tgt}: інфраструктура у внутрішньому колі ({src_ring})"
                if msg not in violations:
                    violations.append(msg)
                    
    for port_mod, impl_mod in ports:
        if impl_mod == root:
            continue
        port_ring = modules[port_mod]
        impl_ring = modules[impl_mod]
        port_idx = ring_indices[port_ring]
        impl_idx = ring_indices[impl_ring]
        
        if port_idx >= impl_idx:
            msg = f"{impl_mod} реалізує порт з {port_mod}: порт ({port_ring}) не лежить глибше за реалізацію ({impl_ring})"
            if msg not in violations:
                violations.append(msg)
                
    return violations