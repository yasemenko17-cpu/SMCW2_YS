"""МКР. Завдання 10: Обмеження частоти: фіксоване вікно і кошик токенів."""


def simulate_limiter(times_ms: list[int], kind: str, limit: int, window_ms: int, burst: int | None = None) -> list[tuple[bool, int]]:
    """Реалізуйте за умовою завдання."""
    raise NotImplementedError  # TODO: реалізуйте за карткою


def peak_allowed(times_ms: list[int], decisions: list[tuple[bool, int]], span_ms: int) -> int:
    """Реалізуйте за умовою завдання."""
    raise NotImplementedError  # TODO: реалізуйте за карткою
