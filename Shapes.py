import numpy as np

class Sphere:
    """Class for sphere"""
    def __init__(self, center, radius, material, tag="sphere"):
        self.tag = tag
        self.center = center
        self.radius = radius
        self.material = material
        self.light_source = False
        self.emission = np.array([0.0, 0.0, 0.0])
        self.emission_strength = 0.0
    
    def hit(self, ray, t_min: float, t_max: float):
        """finds if sphere intersects ray"""
        oc = self.center-ray.origin #origin of ray to center of circle
        a = np.dot(ray.direction, ray.direction)
        #b = -2.0*np.dot(ray.direction, oc)
        h = np.dot(ray.direction, oc)
        c = np.dot(oc, oc) - self.radius*self.radius
        discriminant = h*h - a*c
        if discriminant < 0:
            return False
        sqrtd = np.sqrt(discriminant) 
        root = (h-sqrtd)/(a) #find first root
        if t_min < root < t_max:
            ray.t = root
            return True
        root = (h+sqrtd)/(a) #if root is negative, use other root
        if t_min < root < t_max:
            ray.t = root
            return True
        return False
    
    def normal(self, point, ray):
        """returns normal vector of sphere at point"""
        return (point - self.center)/self.radius
    
class Quad:
    """Class for quad"""
    def __init__(self, p, v1, v2, material, tag="quad"):
        self.tag = tag
        self.n = np.cross(v1, v2)
        self.p = p
        self.v1 = v1
        self.v2 = v2
        self.D = np.dot(self.n, p)
        self.material = material
        self.light_source = False
        self.emission = np.array([0.0, 0.0, 0.0])
        self.emission_strength = 0.0 
    def hit(self, ray, t_min: float, t_max: float):
        """Finds if quad intersects ray"""
        denom = np.dot(self.n, ray.direction)
        # Check if the ray is not parallel to the quad
        if abs(denom) > 1e-8:
            t = (self.D - np.dot(self.n, ray.origin)) / denom
            # Check if t is within the valid range
            if t_min < t < t_max:
                point = ray.at(t)
                v = point - self.p # Vector from the quad origin to the intersection point
                q1 = np.dot(self.v1, v) 
                q2 = np.dot(self.v2, v)
                # Check if the intersection point is within the quad bounds
                if 0 < q1 < np.dot(self.v1, self.v1) and 0 < q2 < np.dot(self.v2, self.v2):
                    ray.t = t
                    return True
        return False
    def normal(self, point, ray_in):
        self.front_face = np.dot(ray_in.direction, self.n) < 0 # Check if the ray is hitting the front face
        normal = self.n if self.front_face else -self.n # If the ray is hitting the back face, flip the normal
        return normal