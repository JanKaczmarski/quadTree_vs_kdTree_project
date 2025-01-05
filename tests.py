import quadtree as qt
import kdtree as kd
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
    start_time = time.perf_counter()
    out = func(*args, **kwargs)
    total_time = time.perf_counter() - start_time

    # TODO: jk: Make this printing prune alligned. Making restriction on max title length should solve the issue
    print(f"{title}:{DELIMITER}{round(total_time, TIME_OUT_PRECISION)} s")

    return out, total_time


def generate_points(gen_func: typing.Callable, num_points: int, range_min, range_max) -> list[tuple[float, float]]:
    """
    Generate points for both QuadTree and KDTree, respecting both data structures desired input. 
    """
    
    return [(gen_func(range_min, range_max), gen_func(range_min, range_max)) for _ in range(num_points)]


def test_random(count=200, capacity=1):
    points = generate_points(np.random.uniform, count, POINT_GEN_LOWER_BOUND, POINT_GEN_UPPER_BOUND)

    # Build and measure QuadTree init time
    qtree, _ = measure_func("QuadTree build time", qt.BuildQuadTree, qt.AABB(
            (DEFAULT_AABB_CENTER_X, DEFAULT_AABB_CENTER_Y), POINT_GEN_UPPER_BOUND/2, POINT_GEN_UPPER_BOUND/2
        ),
        capacity,
        points=points
    )

    # Build and measure KDTree init time
    kdtree, _ = measure_func("KDTree build time", kd.build_kd_tree, points)
    
    
    # x_min, x_max, y_min, y_max
    section = 2, 38, 5, 35
    rect_section = kd.rect(section[0], section[1], section[2], section[3])
    # convert section representation to AABB representation
    rect_aabb = qt.AABB(((section[0] + section[1])/2 , (section[2] + section[3])/2),
                        (section[1] - section[0])/2, (section[3] - section[2])/2)

    # Measure time for query in QuadTree
    q_out, _ = measure_func("Measure QuadTree query time", qtree.query_range, rect_aabb)

    # Measure time for query in KDTree
    kd_out, _ = measure_func("Measure KDTree query time", kd.points_inside_rect, rect_section, kdtree)

    return set(q_out) == set(kd_out)


def test_normal_dist(count=200, capacity=1):
    points = generate_points(np.random.normal, count, POINT_GEN_LOWER_BOUND, POINT_GEN_UPPER_BOUND)

    # Build and measure QuadTree init time
    qtree, _ = measure_func("QuadTree build time", qt.BuildQuadTree, qt.AABB(
            (DEFAULT_AABB_CENTER_X, DEFAULT_AABB_CENTER_Y), POINT_GEN_UPPER_BOUND/2, POINT_GEN_UPPER_BOUND/2
        ),
        capacity,
        points=points
    )

    # Build and measure KDTree init time
    kdtree, _ = measure_func("KDTree build time", kd.build_kd_tree, points)
    
    
    # x_min, x_max, y_min, y_max
    section = 25, 75, 25, 75
    rect_section = kd.rect(section[0], section[1], section[2], section[3])
    # convert section representation to AABB representation
    rect_aabb = qt.AABB(((section[0] + section[1])/2 , (section[2] + section[3])/2),
                        (section[1] - section[0])/2, (section[3] - section[2])/2)

    # Measure time for query in QuadTree
    q_out, _ = measure_func("Measure QuadTree query time", qtree.query_range, rect_aabb)

    # Measure time for query in KDTree
    kd_out, _ = measure_func("Measure KDTree query time", kd.points_inside_rect, rect_section, kdtree)

    return set(q_out) == set(kd_out)

def test_clusters(count=200, capacity=1):
    """
    Test for measuring clutered points query/build time
    """
    points = []
    # Ranges simulate 
    for _ in range(count // 2):
        points.extend(generate_points(np.random.uniform, count // 4, 0, 20))
    for _ in range(count // 2):
        points.extend(generate_points(np.random.uniform, count // 4, 80, 100))

    # Build and measure QuadTree init time
    qtree, _ = measure_func("QuadTree build time", qt.BuildQuadTree, qt.AABB(
            (DEFAULT_AABB_CENTER_X, DEFAULT_AABB_CENTER_Y), POINT_GEN_UPPER_BOUND/2, POINT_GEN_UPPER_BOUND/2
        ),
        capacity,
        points=points
    )

    # Build and measure KDTree init time
    kdtree, _ = measure_func("KDTree build time", kd.build_kd_tree, points)


    # x_min, x_max, y_min, y_max
    section = 10, 90, 10, 90
    rect_section = kd.rect(section[0], section[1], section[2], section[3])
    # convert section representation to AABB representation
    rect_aabb = qt.AABB(((section[0] + section[1])/2 , (section[2] + section[3])/2),
                        (section[1] - section[0])/2, (section[3] - section[2])/2)

    # Measure time for query in QuadTree
    q_out, _ = measure_func("Measure QuadTree query time", qtree.query_range, rect_aabb)

    # Measure time for query in KDTree
    kd_out, _ = measure_func("Measure KDTree query time", kd.points_inside_rect, rect_section, kdtree)

    return set(q_out) == set(kd_out)


def test_outliers(count=200, capacity=1):
    points = []
    for _ in range((count * 99) // 100):
        point = (np.random.uniform(40, 50), np.random.uniform(30, 40))
        points.append(point)
    for _ in range(count - (count * 99) // 100):
        point = (np.random.uniform(0, 100), np.random.uniform(0, 100))
        points.append(point)

    # Build and measure QuadTree init time
    qtree, _ = measure_func("QuadTree build time", qt.BuildQuadTree, qt.AABB(
            (DEFAULT_AABB_CENTER_X, DEFAULT_AABB_CENTER_Y), POINT_GEN_UPPER_BOUND/2, POINT_GEN_UPPER_BOUND/2
        ),
        capacity,
        points=points
    )

    # Build and measure KDTree init time
    kdtree, _ = measure_func("KDTree build time", kd.build_kd_tree, points)


    # x_min, x_max, y_min, y_max
    section = 45, 83, 23, 28
    rect_section = kd.rect(section[0], section[1], section[2], section[3])
    # convert section representation to AABB representation
    rect_aabb = qt.AABB(((section[0] + section[1])/2 , (section[2] + section[3])/2),
                        (section[1] - section[0])/2, (section[3] - section[2])/2)

    # Measure time for query in QuadTree
    q_out, _ = measure_func("Measure QuadTree query time", qtree.query_range, rect_aabb)

    # Measure time for query in KDTree
    kd_out, _ = measure_func("Measure KDTree query time", kd.points_inside_rect, rect_section, kdtree)

    return set(q_out) == set(kd_out)
   

def test_cross(count=200, capacity=1):
    points = []
    for _ in range(count // 2):
        point = (np.random.uniform(0, 50), 50)
        points.append(point)
    for _ in range(count // 2 + count % 2):
        point = (25, np.random.uniform(0, 100))
        points.append(point)

    # Build and measure QuadTree init time
    qtree, _ = measure_func("QuadTree build time", qt.BuildQuadTree, qt.AABB(
            (25, 50), 25, 50
        ),
        capacity,
        points=points
    )

    # Build and measure KDTree init time
    kdtree, _ = measure_func("KDTree build time", kd.build_kd_tree, points)


    # x_min, x_max, y_min, y_max
    section = 20, 40, 20, 60
    rect_section = kd.rect(section[0], section[1], section[2], section[3])
    # convert section representation to AABB representation
    rect_aabb = qt.AABB(((section[0] + section[1])/2 , (section[2] + section[3])/2),
                        (section[1] - section[0])/2, (section[3] - section[2])/2)

    # Measure time for query in QuadTree
    q_out, _ = measure_func("Measure QuadTree query time", qtree.query_range, rect_aabb)

    # Measure time for query in KDTree
    kd_out, _ = measure_func("Measure KDTree query time", kd.points_inside_rect, rect_section, kdtree)

    return set(q_out) == set(kd_out)


functions_fast = [test_random, test_normal_dist, test_outliers]
functions_slow = [test_clusters, test_cross]


# TODO: jk: Make this testing for different point ranges more verbose
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


print("Testing FAST functions")
print("&" * 35)
for n in [1000, 10000, 20000, 50000, 100000]:
    print("^" * 35)
    print("Number of points:", n)
    run_tests(functions_fast, count=n)

print("Testing SLOW functions")
print("&" * 35)
for n in [100, 200, 500, 1000, 2000]:
    print("^" * 35)
    print("Number of points:", n)
    run_tests(functions_slow, count=n)

