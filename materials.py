import numpy as np
import useful_functions as uf
from Ray import Ray

class Diffuse:
    """Class for diffuse"""
    def __init__(self, colour):
        self.colour = colour

    def scatter(self, ray, normal):
        """Returns scattered ray"""
        scatter_direction = uf.random_on_hemisphere(normal) #random vector on hemisphere
        scattered = Ray(ray.at(ray.t), scatter_direction) #ray at p of intersection with scatter direction
        return scattered

class Specular:
    """Class for specular"""
    def __init__(self, colour):
        self.colour = colour

    def scatter(self, ray, normal):
        """Returns reflected ray"""
        reflected = uf.reflect(ray.direction, normal) #reflect ray direction around normal
        scattered = Ray(ray.at(ray.t), reflected) #ray at p of intersection with reflected direction
        return scattered