class CellData:
    q: int
    r: int
    richness: int
    index: int
    owner: int
    celltype: int
    ants: [int]

    def __init__(self, q: int, r: int, richness: int, index: int, owner: int, celltype: int, ants: [int]):
        self.q = q
        self.r = r
        self.richness = richness
        self.index = index
        self.owner = owner
        self.celltype = celltype
        self.ants = ants
