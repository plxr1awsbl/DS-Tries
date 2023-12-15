import math

from typing import List

import my_linear_algebra as LA

# Mean. Return sum / len
def mean(xs: List[float]) -> float:
    return sum(xs) / len(xs)

# Median. Returns the middle value
def _median_odd(xs: List[float]) -> float:
    return sorted(xs)[len(xs) // 2]

def _median_even(xs: List[float]) -> float:
    sorted_xs = sorted(xs)
    hi_midpoint = len(xs) // 2
    return (sorted_xs[hi_midpoint - 1] + sorted_xs[hi_midpoint]) / 2

def median(v: List[float]) -> float:
    return _median_even(v) if len(v) % 2 == 0 else _median_odd(v)

# Quantile. The value that is bigger than a certain percentile of data
def quantile(xs: List[float], p: float) -> float:
    p_index = int(p * len(xs))
    return sorted(xs)[p_index]

# Range. The difference between min and max
def data_range(xs: List[float]) -> float:
    return max(xs) - min(xs)

# Variance. Data variation index
def de_mean(xs: List[float]) -> List[float]:
    x_bar = mean(xs)
    return [x - x_bar for x in xs]

def variance(xs: List[float]) -> float:
    assert len(xs) >= 2, "Variance requires at least 2 elements"
    n = len(xs)
    deviations = de_mean(xs)
    return LA.sum_of_squares(deviations) / (n-1)

# Standart deviation. Square root of the variance
def standart_deviation(xs: List[float]) -> float:
    return math.sqrt(variance(xs))

# Interquantile range. Difference between 75-quantile and 25-quantile
def interquantile_range(xs: List[float]) -> float:
    return quantile(xs, 0.75) - quantile(xs, 0.25)

# Covariance. A paired analog of variance
def covariance(xs: List[float], ys: List[float]) -> float:
    assert len(xs) == len(ys), "xs and ys must contain equal number of elements"
    return LA.dot(de_mean(xs), de_mean(ys)) / (len(xs) - 1)

# Corelation
def corelation(xs: List[float], ys: List[float]) -> float:
    stdev_x = standart_deviation(xs)
    stdev_y = standart_deviation(ys)
    if stdev_x > 0 and stdev_y > 0:
        return covariance(xs, ys) / stdev_x /stdev_y
    else:
        return 0
