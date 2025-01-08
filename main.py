import numpy as np
import matplotlib.pyplot as plt
from Ray import Ray
from Shapes import Sphere, Quad
import useful_functions as uf
import random
from materials import Diffuse, Specular
import time

#camera
center = np.array([0, 0, 0]) #camera position
ratio = 1.0/1.0
width = 500
height = int(width/ratio)
samples_per_pixel = 3#used for anti-aliasing
pixel_samples_scale = 1.0/samples_per_pixel

#viewport
focal_length = 1 #focal length of camera (distance to viewport)
viewport_height = 2.0 * focal_length
viewport_width = (float(width)/height)*viewport_height
viewport_u = np.array([viewport_width, 0, 0])
viewport_v = np.array([0, -viewport_height, 0])
pixel_delta_u = viewport_u/width
pixel_delta_v = viewport_v/height
viewport_upper_left = center - viewport_u/2 - viewport_v/2 + np.array([0,0,focal_length]) #upper left corner of viewport
first_pixel = viewport_upper_left + pixel_delta_u/2 + pixel_delta_v/2

def sky():
    """returns sky colour"""
    return np.array([0.5, 0.7, 1.0], dtype=np.float64) #sky colour (light blue)

def collide(ray, objects):
    """finds if ray collides with any object in objects list"""
    hit = False
    closest_object = None #closest object hit by ray
    closest_t = float(1000000000000000) #arbitrarily large number
    for object in objects:
        if object.hit(ray, 0.0001, closest_t):
            hit = True #ray has hit object
            closest_t = ray.t #update closest t
            closest_object = object #update closest object
    return hit, closest_object, closest_t

def trace(ray, objects):
    """traces ray and returns colour of pixel"""
    total_light = np.array([0.0, 0.0, 0.0], dtype=np.float64)
    max_depth = 10 #max depth of ray tracing, to prevent infinite recursion
    colour = np.array([1, 1, 1], dtype=np.float64)
    for i in range(max_depth):
        hit = collide(ray, objects)
        if hit[0]:
            normal = hit[1].normal(ray.at(hit[2]), ray)
            emittedlight = hit[1].emission * hit[1].emission_strength #emitted light, zero if not a light source
            total_light += emittedlight*colour #add emitted light
            colour *= hit[1].material.colour #pick up the colour of the object
            if hit[1].light_source:
                break
            ray = hit[1].material.scatter(ray, normal)
        else:
            #total_light += sky()*colour (uncomment for sky)
            break
    return total_light

def render():
    """renders image"""
    objects = []
    red = Specular(np.array([0.65, 0.05, 0.05]))
    white = Diffuse(np.array([0.73, 0.73, 0.73]))
    green = Diffuse(np.array([0.12, 0.45, 0.15]))
    teal = Diffuse(np.array([0.0, 0.5, 0.5]))
    light_material = Diffuse(np.array([1.0, 1.0, 1.0]))

    # Create the objects for the Cornell Box
    objects = []
    # Floor (white)
    objects.append(Quad(np.array([250, -250, -10]), np.array([-500, 0, 0]), np.array([0, 0, 510]), white, "floor"))

    # Ceiling (white)
    objects.append(Quad(np.array([250, 250, 500]), np.array([-500, 0, 0]), np.array([0, 0, -510]), white, "ceiling"))

    # Back wall (white)
    objects.append(Quad(np.array([250, 250, 500]), np.array([0, -500, 0]), np.array([-500, 0, 0]), white, "back wall"))

    # Left wall (red)
    objects.append(Quad(np.array([-250, 250, -10]), np.array([0, 0, 510]), np.array([0, -500, 0]), red, "left wall"))

    # Right wall (green)
    objects.append(Quad(np.array([250, 250, -10]), np.array([0, -500, 0]), np.array([0, 0, 510]), green, "right wall"))

    #behind camera
    objects.append(Quad(np.array([250, 250, -10]), np.array([0, -500, 0]), np.array([-500, 0, 0]), teal, "behind camera"))

    #light = Quad(np.array([-100, 210, 150]), np.array([200, 0, 0]), np.array([0, 0, 200]), light_material, "light")

    light = Sphere(np.array([0, 200, 250]), 50, light_material, "light")
    light.light_source = True
    light.emission = np.array([1.0, 1.0, 1.0])
    light.emission_strength = 15 #15 for cornell box
    objects.append(light)

    central_sphere = Sphere(np.array([0, -150, 300]), 100, Specular(np.array([0.8,0.8,0.3])))
    objects.append(central_sphere)

    image = np.zeros((height, width, 3)) #image array
    for i in range(height):
        print('{:.1f}'.format((i/height)*100)) #prints progress
        for j in range(width):
            pixel_colour = np.array([0.0, 0.0, 0.0]) 
            for s in range(samples_per_pixel): 
                offset = np.array([random.random()-0.5, random.random()-0.5, 0]) #random offset for anti-aliasing
                ray = Ray(center, first_pixel + (j+offset[0])*pixel_delta_u + (i+offset[1])*pixel_delta_v) #shoots ray from camera to pixel
                pixel_colour += trace(ray, objects)
            pixel_colour *= pixel_samples_scale
            max = np.max(pixel_colour)
            if max > 1.0:
                pixel_colour /= max #normalise pixel colour
            image[i, j] = np.sqrt(pixel_colour) #square root for gamma correction
        plt.imsave('image.png', image) #saves image after each row
    print('100.0')
    return image

time_limit = 100 #time limit for rendering in seconds
start = time.time()
num_of_renders = 1 #number of renders to do
rend = np.zeros((height, width, 3))
tic = 0
for i in range(num_of_renders): #averages multiple renders to reduce noise
    im = render()
    rend += im
    w = rend/(i+1)
    plt.imsave('Final.png', w) #saves image after each render
    print('Render', i+1, 'done')
    tic +=1
    print('Time elapsed:', (time.time()-start)/60, 'minutes')
    if time.time() - start > time_limit:
        print('Time limit reached')
        break
rend /= tic
plt.imsave('Final.png', rend) #saves final image
print(f'{tic} renders done') #prints number of renders done