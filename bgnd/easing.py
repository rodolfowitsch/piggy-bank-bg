"""Easing functions for animations."""


def ease_in_quad(t: float) -> float:
    return t * t


def ease_out_bounce(t: float) -> float:
    if t < 1 / 2.75:
        return 7.5625 * t * t
    elif t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625 / 2.75
        return 7.5625 * t * t + 0.984375


def coin_drop(t: float) -> float:
    """Ease-in fall (0-0.7) then bouncy landing (0.7-1.0)."""
    if t < 0.7:
        return ease_in_quad(t / 0.7) * 0.7
    else:
        return 0.7 + ease_out_bounce((t - 0.7) / 0.3) * 0.3
