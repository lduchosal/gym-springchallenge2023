import unittest
from math import atan2
from typing import List

from matplotlib import pyplot as plt

from springchallenge2023.pyleague.game.CubeCoord import CubeCoord
from springchallenge2023.pyleague.game.PointyBoardPlotter import PointyBoardPlotter

def sort_hexagon(cube_coords: List[(CubeCoord)]) -> List[CubeCoord]:

    sort = []

    return sorted(
        cube_coords,
        key=lambda c: (c.distance_from_center(), -c.angle_from_center())
    )


def alternate_sort_hexagon(cube_coords: List[CubeCoord]) -> List[CubeCoord]:
    sorted_coords = sorted(
        cube_coords,
        key=lambda c: (c.distance_from_center(), -c.angle_from_center())
    )

    alternate_sorted_coords = []
    for i in range(0, len(sorted_coords) // 2):
        alternate_sorted_coords.append(sorted_coords[i])
        alternate_sorted_coords.append(sorted_coords[-(i + 1)])

    if len(sorted_coords) % 2 != 0:
        alternate_sorted_coords.append(sorted_coords[len(sorted_coords) // 2])

    return alternate_sorted_coords

def axial_sort(cube_coords: List[CubeCoord]) -> List[CubeCoord]:
    center_q, center_r = (0, 0, 0)
    sorted_coords = sorted(
        cube_coords,
        key=lambda c: (c.distance_from_center(), c.axial_coordinate)
    )
    return sorted_coords


def sort_by_axes(cube_coords: List[CubeCoord]) -> List[CubeCoord]:
    return sorted(cube_coords, key=lambda c: c.sort())

def sort_by_index(cube_coords: List[CubeCoord]) -> List[CubeCoord]:
    return sorted(cube_coords, key=lambda c: c.index)

class TestHexagonSorting(unittest.TestCase):
    def test_sort_hexagon(self):

        neighbors_cube = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1), (0,0,0)]
        coords1 = [CubeCoord(*tuple_) for tuple_ in neighbors_cube]

        sorted_coords = sort_hexagon(coords1)
        sorted_coords_str = [(c.x, c.y, c.z) for c in sorted_coords]

        # Expected sorted coordinates (you may need to adjust this based on your requirements)
        coords2 = [CubeCoord(*tuple_) for tuple_ in sorted_coords_str]
        expected_coords_str = []

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_grid(ax, coords2)
        plt.show()

        self.assertEqual(sorted_coords_str, expected_coords_str)


    def test_sort_hexagon_alternate(self):

        neighbors_cube = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1), (0,0,0)]
        coords1 = [CubeCoord(*tuple_) for tuple_ in neighbors_cube]

        sorted_coords = alternate_sort_hexagon(coords1)
        sorted_coords_str = [(c.x, c.y, c.z) for c in sorted_coords]

        # Expected sorted coordinates (you may need to adjust this based on your requirements)
        coords2 = [CubeCoord(*tuple_) for tuple_ in sorted_coords_str]
        expected_coords_str = []

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_grid(ax, coords2)
        plt.show()


        self.assertEqual(sorted_coords_str, expected_coords_str)



    def test_sort_by_axes(self):

        neighbors_cube = [(1, -1, 0), (1, 0, -1), (0, 1, -1), (-1, 1, 0), (-1, 0, 1), (0, -1, 1), (0,0,0)]
        coords1 = [CubeCoord(*tuple_) for tuple_ in neighbors_cube]

        sorted_coords = sort_by_axes(coords1)
        sorted_coords_str = [(c.x, c.y, c.z) for c in sorted_coords]

        # Expected sorted coordinates (you may need to adjust this based on your requirements)
        coords2 = [CubeCoord(*tuple_) for tuple_ in sorted_coords_str]
        expected_coords_str = [(0, 0, 0),  (0, 1, -1), (0, -1, 1),  (1, 0, -1), (-1, 0, 1), (1, -1, 0), (-1, 1, 0)]


        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_grid(ax, coords2)
        plt.show()


        self.assertEqual(sorted_coords_str, expected_coords_str)

    def test_sort_by_index(self):

        neighbors_cube = []

        for x in range(-3, 4):
            for y in range(max(-3, -x - 3), min(3, -x + 3) + 1):
                z = -x - y
                neighbors_cube.append((x, y, z))

        print(neighbors_cube)

        coords1 = [CubeCoord(*tuple_) for tuple_ in neighbors_cube]

        sorted_coords = sort_by_index(coords1)
        sorted_coords_str = [(c.x, c.y, c.z) for c in sorted_coords]

        # Expected sorted coordinates (you may need to adjust this based on your requirements)
        coords2 = [CubeCoord(*tuple_) for tuple_ in sorted_coords_str]
        expected_coords_str = [(0, 0, 0), (0, 1, -1), (0, -1, 1), (1, 0, -1), (-1, 0, 1), (1, -1, 0), (-1, 1, 0)]

        bplot = PointyBoardPlotter()
        fig, ax = plt.subplots()
        bplot.plot_grid(ax, coords2)
        plt.show()


if __name__ == '__main__':
    unittest.main()
