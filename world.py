


class World:
    def __init__(self):
        self.map = {}
        self.genWorld()

    @staticmethod
    def genCube(x, y, z, n=.5):
        return (
            ((x-n,y+n,z-n), (x-n,y+n,z+n), (x+n,y+n,z+n), (x+n,y+n,z-n)),  # top
            ((x-n,y-n,z-n), (x+n,y-n,z-n), (x+n,y-n,z+n), (x-n,y-n,z+n)),  # bottom
            ((x-n,y-n,z-n), (x-n,y-n,z+n), (x-n,y+n,z+n), (x-n,y+n,z-n)),  # left
            ((x+n,y-n,z+n), (x+n,y-n,z-n), (x+n,y+n,z-n), (x+n,y+n,z+n)),  # right
            ((x-n,y-n,z+n), (x+n,y-n,z+n), (x+n,y+n,z+n), (x-n,y+n,z+n)),  # front
            ((x+n,y-n,z-n), (x-n,y-n,z-n), (x-n,y+n,z-n), (x+n,y+n,z-n)),  # back
        )


    def genWorld(self):
        for x in range(-5, 5):
            for z in range(-5, 5):
                self.map[(x, -2, z)] = self.genCube(x, -2, z)