from dataclasses import dataclass
import math
import numpy as np

__all__ = [
    "ModelResult", "fit_all_models", "choose_best",
    "fit_linear", "fit_poly2", "fit_poly3",
    "fit_exponential", "fit_logarithmic", "fit_power",
]

#вспомогательные статистические функции

def _rms(y, y_hat) -> float:
    """Среднеквадратическая ошибка (σ)."""
    return float(np.sqrt(np.mean((y - y_hat) ** 2)))

def _r_squared(y, y_hat) -> float:
    """Коэффициент детерминации R²."""
    ss_tot = np.sum((y - y.mean()) ** 2)
    ss_res = np.sum((y - y_hat) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot else float("nan")

def _pearson_r(x, y) -> float:
    """Коэффициент корреляции Пирсона (для линейной модели)."""
    if len(x) < 2:
        return float("nan")
    sx, sy = x.std(ddof=0), y.std(ddof=0)
    cov = np.cov(x, y, ddof=0)[0, 1]
    return float(cov / (sx * sy)) if sx and sy else float("nan")


#структура результата

@dataclass
class ModelResult:
    name: str                 #имя
    formula: str              # шаблон формулы для отчёта
    coef: np.ndarray          # коэффициенты (a, b, c, …)
    y_hat: np.ndarray         # значения модели в узлах
    sigma: float              # RMS‑ошибка
    r2: float                 # коэффициент детерминации
    extra: dict               # доп. показатели (р, …)

    def coef_str(self, digits: int = 5) -> str:
        return ", ".join(f"{c:.{digits}g}" for c in self.coef)


#МНК‑аппроксимации

def fit_linear(x, y) -> ModelResult:
    X = np.vstack([np.ones_like(x), x]).T
    a, b = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = a + b * x
    return ModelResult(
        name="Линейная",
        formula="y = {a:.5g} + {b:.5g}·x",
        coef=np.array([a, b]),
        y_hat=y_hat,
        sigma=_rms(y, y_hat),
        r2=_r_squared(y, y_hat),
        extra={"Pearson r": _pearson_r(x, y)},
    )


def fit_poly2(x, y) -> ModelResult:
    X = np.vstack([np.ones_like(x), x, x**2]).T
    a, b, c = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = a + b * x + c * x**2
    return ModelResult(
        name="Полином 2‑й ст.",
        formula="y = {a:.5g} + {b:.5g}·x + {c:.5g}·x²",
        coef=np.array([a, b, c]),
        y_hat=y_hat,
        sigma=_rms(y, y_hat),
        r2=_r_squared(y, y_hat),
        extra={},
    )


def fit_poly3(x, y) -> ModelResult:
    X = np.vstack([np.ones_like(x), x, x**2, x**3]).T
    a, b, c, d = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = a + b * x + c * x**2 + d * x**3
    return ModelResult(
        name="Полином 3‑й ст.",
        formula="y = {a:.5g} + {b:.5g}·x + {c:.5g}·x² + {d:.5g}·x³",
        coef=np.array([a, b, c, d]),
        y_hat=y_hat,
        sigma=_rms(y, y_hat),
        r2=_r_squared(y, y_hat),
        extra={},
    )


def fit_exponential(x, y) -> ModelResult:
    if np.any(y <= 0):
        raise ValueError("Экспоненциальная модель требует y > 0")
    Y = np.log(y)
    X = np.vstack([np.ones_like(x), x]).T
    ln_a, b = np.linalg.lstsq(X, Y, rcond=None)[0]
    a = math.exp(ln_a)
    y_hat = a * np.exp(b * x)
    return ModelResult(
        name="Экспоненциальная",
        formula="y = {a:.5g}·e^{b:.5g}·x",
        coef=np.array([a, b]),
        y_hat=y_hat,
        sigma=_rms(y, y_hat),
        r2=_r_squared(y, y_hat),
        extra={},
    )


def fit_logarithmic(x, y) -> ModelResult:
    if np.any(x <= 0):
        raise ValueError("Логарифмическая модель требует x > 0")
    X = np.vstack([np.ones_like(x), np.log(x)]).T
    a, b = np.linalg.lstsq(X, y, rcond=None)[0]
    y_hat = a + b * np.log(x)
    return ModelResult(
        name="Логарифмическая",
        formula="y = {a:.5g} + {b:.5g}·ln x",
        coef=np.array([a, b]),
        y_hat=y_hat,
        sigma=_rms(y, y_hat),
        r2=_r_squared(y, y_hat),
        extra={},
    )


def fit_power(x, y) -> ModelResult:
    if np.any(x <= 0) or np.any(y <= 0):
        raise ValueError("Степенная модель требует x, y > 0")
    Y = np.log(y)
    X = np.vstack([np.ones_like(x), np.log(x)]).T
    ln_a, b = np.linalg.lstsq(X, Y, rcond=None)[0]
    a = math.exp(ln_a)
    y_hat = a * x ** b
    return ModelResult(
        name="Степенная",
        formula="y = {a:.5g}·x^{b:.5g}",
        coef=np.array([a, b]),
        y_hat=y_hat,
        sigma=_rms(y, y_hat),
        r2=_r_squared(y, y_hat),
        extra={},
    )


#сборщик моделей

_MODEL_FUNCS = [
    fit_linear,
    fit_poly2,
    fit_poly3,
    fit_exponential,
    fit_logarithmic,
    fit_power,
]


def fit_all_models(x, y):
#Возвращает список ModelResult для всех шести моделей.
#Неприменимая (из-за ограничений) модель пропускается.
    models = []
    for fit_func in _MODEL_FUNCS:
        try:
            models.append(fit_func(x, y))
        except ValueError as e:
            print(f"→ {fit_func.__name__[4:]} пропущена: {e}")
    return models


def choose_best(models):
    """Модель с минимальной σ."""
    return min(models, key=lambda m: m.sigma)
