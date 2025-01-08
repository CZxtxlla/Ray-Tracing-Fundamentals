import useful_functions as uf

class Ray:
    def __init__(self, origin, direction):
        """Class for ray with origin and direction"""
        self.origin = origin #origin of ray
        self.direction = uf.unit_vector(direction) #direction of ray
        self.t = 0

    def at(self, t):
        """returns point at t along ray"""
        return self.origin + t*self.direction 