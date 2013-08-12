RATIO = 0.0625    
TEXTURE_COOD = ( (16, 13),
                 (2, 16),
                 (3, 16),
                 (1, 7),
                 (4, 16),
                 (5, 16)
                )


class World:

    @staticmethod
    def genTexcoord(coordId):
        ''' Coordinate is generate clockwisely'''
        x, y = TEXTURE_COOD[coordId]
        x, y = [x*RATIO, y*RATIO]
        return (
            (x-RATIO, y-RATIO), (x, y-RATIO), (x, y), (x-RATIO, y)
        )


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
