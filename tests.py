import quadtree as qt
import numpy as np
import time
import typing

TIME_OUT_PRECISION=3
DELIMITER="\t"*3
DEFAULT_POINTS_COUNT=200
DEFAULT_NODE_CAPACITY=1
POINT_GEN_LOWER_BOUND=0
POINT_GEN_UPPER_BOUND=100
DEFAULT_AABB_CENTER_X=50
DEFAULT_AABB_CENTER_Y=50

# Allows to annotate return value to be the same as that of accepted parameter
# Used in measure_func function
T = typing.TypeVar('T')


def measure_func(title, func: typing.Callable[..., T], *args, **kwargs) -> tuple[T, float]:
    """
    Takes function that takes any number of params and return any type. Measures time for this function to commplete and returns function output
    """
    start_time = time.time()
    out = func(*args, **kwargs)
    total_time = time.time() - start_time

    # Make this printing prune alligned. Making restriction on max title length should solve the issue
    print(f"{title}:{DELIMITER}{round(total_time, TIME_OUT_PRECISION)}")

    return out, total_time


def generate_random_points(num_points, range_min, range_max) -> list[qt.XY]:
    return [qt.XY(np.random.uniform(range_min, range_max), np.random.uniform(range_min, range_max)) for _ in range(num_points)]


def test_random(count=200, capacity=1):
    points = generate_random_points(count, POINT_GEN_LOWER_BOUND, POINT_GEN_UPPER_BOUND)

    # Build and measure QuadTree init time
    qtree, _ = measure_func("QuadTree build time", qt.BuildQuadTree, qt.AABB(
            qt.XY(DEFAULT_AABB_CENTER_X, DEFAULT_AABB_CENTER_Y), POINT_GEN_UPPER_BOUND/2, POINT_GEN_UPPER_BOUND/2
        ),
        capacity,
        points=points
    )

    # TODO: jk: Build and measure KDTree init time
    # <implementation here>

    rect_aabb = qt.AABB(qt.XY(20, 20), 18, 15)

    # Measure time for query in QuadTree
    q_out = measure_func("Measure QuadTree query time", qtree.query_range, rect_aabb)

    # Measure time for query in KDTree

    # TODO: jk: Make Testing for KDTree querying

    #result = compare_out(q_out, kd_out)
    #assert(result, True)

    #return result
    return True

functions = [test_random]

def run_tests(functions: list[typing.Callable], count=DEFAULT_POINTS_COUNT, capacity=DEFAULT_NODE_CAPACITY):
    passed, total_test_num = 0, len(functions)
    for func in functions:
        print(f"Running test: {func.__name__}")
        print('-' * 35)
        res = func(count, capacity)
        # Check if out from KDTree and from QuadTree matches
        print("Test Passed:", res)
        if res:
            passed += 1

    print('*' * 35)
    print("Tests passed:", passed, "Total tests run:", total_test_num)

run_tests(functions)

