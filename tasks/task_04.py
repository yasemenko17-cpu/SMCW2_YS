def choose_patterns(scenario: dict) -> list[str]:
    valid_keys = {'remote', 'transient_errors', 'long_outages', 'excess_traffic', 'idempotent', 'has_key'}
    for k, v in scenario.items():
        if k not in valid_keys:
            raise ValueError(f"Невідоме поле сценарію: {k}")
        if not isinstance(v, bool):
            raise ValueError(f"Некоректне значення поля {k}: {v!r}")
            
    if not scenario.get('remote', False):
        return []
        
    patterns = []
    if scenario.get('excess_traffic', False):
        patterns.append('Rate Limiting')
    if scenario.get('long_outages', False):
        patterns.append('Circuit Breaker')
    if scenario.get('transient_errors', False) and (scenario.get('idempotent', False) or scenario.get('has_key', False)):
        patterns.append('Retry')
    patterns.append('Timeout')
    
    return patterns