


class World:
    def __init__(self):
        # cube coord
        self.map = {}
        
        # cube motion vector
        self.vec = {}

        # generate world
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
                self.vec[(x, -2, z)] = [0, 0, 0]

        # give origin a motion
        self.vec[(0, -2, 0)] = [0, 2, 0]

    def genWave(self):
        for x in range(-5, 5):
            for z in range(-5, 5):
                if sum(self.vec[(x, -2, z)]) > 0.01:
                    vec =  map(sum, zip([x, -2, z], self.vec[(x, -2, z)]))
                    self.map[(x, -2, z)] = self.genCube(*vec)

                    if (x-1, -2, z) in self.map:
                        self.vec[(x-1, -2, z)] = self.vec[(x, -2, z)]
                    
                    if (x, -2, z-1) in self.map:
                        self.vec[(x, -2, z-1)] = self.vec[(x, -2, z)]

                    if (x+1, -2, z) in self.map:
                        self.vec[(x+1, -2, z)] = self.vec[(x, -2, z)]

                    if (x, -2, z+1) in self.map:
                        self.vec[(x, -2, z+1)] = self.vec[(x, -2, z)]

                    self.vec[(x, -2, z)] = [x*.8 for x in self.vec[(x, -2, z)]]
                   
                    
                    


