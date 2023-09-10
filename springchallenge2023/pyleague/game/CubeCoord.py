from math import atan2, pi


class CubeCoord:
    directions = [(1, -1, 0), (0, -1, 1), (-1, 0, 1), (-1, 1, 0), (0, 1, -1), (1, 0, -1)]
    CENTER = None  # Will be defined later after the class definition
    INDEX: int = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.index = CubeCoord.INDEX
        CubeCoord.INDEX += 1

    def __hash__(self):
        prime = 31
        result = 1
        result = prime * result + self.x
        result = prime * result + self.y
        result = prime * result + self.z
        return result

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def neighbor(self, orientation, distance=1):
        nx = self.x + CubeCoord.directions[orientation][0] * distance
        ny = self.y + CubeCoord.directions[orientation][1] * distance
        nz = self.z + CubeCoord.directions[orientation][2] * distance
        return CubeCoord(nx, ny, nz)


    def neighbours(self):
        return [
            CubeCoord(
                self.x + dx,
                self.y + dy,
                self.z + dz
            )
            for dx, dy, dz in CubeCoord.directions
        ]


    def distance_to(self, dst):
        return (abs(self.x - dst.x) + abs(self.y - dst.y) + abs(self.z - dst.z)) // 2

    def __str__(self):
        return f"{self.x},{self.y},{self.z}"

    def get_opposite(self):
        return CubeCoord(-self.x, -self.y, -self.z)

    def distance_from_center(self) -> int:
        return (abs(self.x) + abs(self.y) + abs(self.z)) // 2

    @property
    def axial_coordinate(self) -> (int, int):
        return self.x, self.z

    def angle_from_center(self) -> float:
        return atan2(self.y, self.x) % (2 * pi)

    # z,x,y
    # q,s,r
    def sort(self):
        return \
            self.distance_from_center(), \
            self.y, self.z, self.x, -self.z


# Define CENTER now that the class is complete
CubeCoord.CENTER = CubeCoord(0, 0, 0)
