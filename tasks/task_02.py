def api_violations(
    package: str,
    imports: list[tuple[str, str]],
    public: tuple = ("api",),
    roots: tuple = ("app", "cli"),
    open_units: tuple = ("shared",)
) -> list[str]:
    violations = []
    for src, tgt in imports:
        src_parts = src.split(".")
        tgt_parts = tgt.split(".")
        
        if len(src_parts) >= 2 and src_parts[0] == package:
            src_block = src_parts[1]
        else:
            continue
            
        if len(tgt_parts) >= 2 and tgt_parts[0] == package:
            tgt_block = tgt_parts[1]
        else:
            continue
            
        # Пропускаємо, якщо джерело дорівнює цілі, джерело або ціль входять до roots
        if src_block == tgt_block or src_block in roots or tgt_block in roots:
            continue
            
        if tgt_block in open_units:
            continue
        if len(tgt_parts) == 2:
            continue
        if len(tgt_parts) >= 3 and tgt_parts[2] in public:
            continue
            
        msg = f"{src} -> {tgt}: імпорт нутрощів модуля {tgt_block}"
        if msg not in violations:
            violations.append(msg)
            
    return violations