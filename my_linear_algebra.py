import math
from typing import List, Tuple, Callable

Vector = List[float]
Matrix = List[List[float]]

# Adding vectors
def add(v: Vector, w: Vector) -> Vector:
    assert len(v) == len(w), "Vectors must have equal len"
    return [ v_i + w_i for v_i, w_i in zip(v, w)]

def vector_sum(vectors: List[Vector]) -> Vector:
    assert vectors, "No vectors..."
    num_elements = len(vectors[0])
    assert all(len(v) == num_elements for v in vectors), "Different lens"
    return [sum(vector[i] for vector in vectors) for i in range(num_elements)]

# Substracting vectors
def substract(v: Vector, w: Vector) -> Vector:
    assert len(v) == len(w), "Vectors must have equal len"
    return [ v_i - w_i for v_i, w_i in zip(v, w)]

# Scalar multiply
def scalar_multiply(v: Vector, c: float) -> Vector:
    return [c * v_i for v_i in v]

# Means of vectors list
def vector_mean(vectors: List[Vector]) -> Vector:
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

# Scalar result
def dot(v: Vector, w: Vector) -> float:
    assert len(v) == len(w)
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

#Sum of squares
def sum_of_squares(v: Vector) -> float:
    return dot(v, v)

# Magnitude of Vector
def magnitude(v: Vector) -> float:
    return math.sqrt(sum_of_squares(v))

# Distance between vectors
def distance(v: Vector, w: Vector) -> float:
    return magnitude(substract(v, w))

# Matrix shape
def shape(A: Matrix) -> Tuple[int, int]:
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0
    return num_cols, num_rows

def get_row(A: Matrix, i: int) -> Vector:
    return A[i]

def get_column(A: Matrix, j: int) -> Vector:
    return [A_i[j] for A_i in A]

def make_matrix(num_rows: int, num_cols: int, entry_fn: Callable[[int, int], float]) -> Matrix:
    return [[entry_fn(i, j) for j in range(num_cols)] for i in range(num_rows)]

def identity_matrix(n: int) -> Matrix:
    return make_matrix(n, n, lambda i, j: 1 if i == j else 0)