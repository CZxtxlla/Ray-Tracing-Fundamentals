import numpy as np
import random

def unit_vector(vector):
    """ Returns the unit vector of the vector. """
    return vector / np.linalg.norm(vector)

def reflect(v, n):
    """ Returns the reflection of a vector v around a normal vector n. """
    return v - 2*np.dot(v, n)*n 

def random_on_hemisphere(n):
    """ Returns a random ray on a hemisphere with normal vector normal. """
    random_on_unit_sphere = np.array([random.uniform(-1,1), random.uniform(-1,1), random.uniform(-1,1)]) #random point on unit sphere
    unit_on_sphere = random_on_unit_sphere/np.linalg.norm(random_on_unit_sphere) #unit vector on sphere
    if (np.dot(unit_on_sphere, n) > 0): #if unit vector is in the same direction as normal
        return unit_on_sphere
    return -unit_on_sphere

def near_zero(v):
    """checks if vector is near zero"""
    s = 1e-8
    return np.any(np.abs(v) < s)


