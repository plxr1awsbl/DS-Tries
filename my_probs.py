import math
import random

# * Probability density function and Cumulative distribution function
# * The probability of observing a value in a certain interval is equal to the integral of the density function over this interval
# * The cumulative distribution function shows the probability that a random variable is less than or equal to a certain value
# Uniform probability density function
def uniform_pdf(x: float) -> float:
    return 1 if x>=0 and x < 1 else 0

# Uniform cumulative density function
def uniform_cdf(x: float) -> float:
    if x < 0: return 0
    elif x < 1: return x
    else: return 1

# * The Normal Distribution is determined by two parameters: its mean value (mu) and its standard deviation (sigma)
# * Probability Density function for Normal Distribution:
# * f(x | mu, sigma) = 1 * exp( -(x - mu)**2 / 2 / sigma **2) / sqrt(2 * PI * sigma)
def normal_pdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    SQRT_TWO_PI = math.sqrt(2 * math.pi)
    return math.exp(-(x - mu) ** 2 / 2 / sigma ** 2) / (SQRT_TWO_PI * sigma)

# * Cumulative Density function for Normal Distribution:
def normal_cdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    return (1 + math.erf((x - mu) / math.sqrt(2) / sigma)) / 2

# * Inversive CDF is used to find the value, according to probability
def inverse_normal_cdf(p: float, mu: float = 0, sigma: float = 1, tolerance: float = 0.00001) -> float:
    if mu != 0 or sigma != 1:
        return mu + sigma * inverse_normal_cdf(p, tolerance=tolerance)
    
    low_z = -10.0 # * normal_cdf(-10) tends to 0
    hi_z  = 10.0  # * normal_cdf(10) tends to 1
    
    while hi_z - low_z > tolerance:
        mid_z = (low_z + hi_z) / 2 # Middle point
        mid_p = normal_cdf(mid_z)
        if mid_p < p:
            low_z = mid_z
        else:
            hi_z = mid_z
    
    return mid_z

# * Bernoulli trial returns 1 with prob = p and 0 with prob = p-1
def bernoulli_trial(p: float) -> int:
    return 1 if random.random() < p else 0

# * Sum of n independent random values with Bernoulli trial
def binominal(n: int, p: float) -> int:
    return sum(bernoulli_trial(p) for _ in range(n))

