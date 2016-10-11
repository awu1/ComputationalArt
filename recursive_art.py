""" Alyssa Wu """

import random, math
from PIL import Image


def build_random_function(min_depth, max_depth):
    curr_depth = max_depth

    functions = ['prod', 'avg', 'cos_pi', 'sin_pi', 'add', 'neg']
    random_function = random.choice(functions)


    funct = []
    xy_funct = ['x','y']

    if(max_depth == 1):
        random_xy = random.choice(xy_funct)
        funct.append(random_xy)
        return funct
    elif(min_depth <= 1):
        functions.extend(xy_funct)
        ran = random.random()
        if(ran >= 0.6):
            random_xy = random.choice(xy_funct)
            funct.append(random_xy)
            return funct

    funct.append(random_function)
    curr_depth -=1


    if(random_function == 'prod' or random_function == 'avg' or random_function == 'add'):
        funct.append(build_random_function(min_depth - 1, curr_depth))
        funct.append(build_random_function(min_depth - 1, curr_depth))
    elif(random_function == 'cos_pi' or random_function == 'sin_pi' or random_function == 'neg'):
        funct.append(build_random_function(min_depth - 1, curr_depth))

    return funct


def evaluate_random_function(f, x, y):
    a = x
    b = y

    functions = {'x':x, 'y':y}

    if(len(f) == 3):
        c = evaluate_random_function(f[1],x,y)
        d = evaluate_random_function(f[2],x,y)
        functions['prod'] = c*d
        functions['avg'] = 0.5*(c+d)
        functions['add'] = c+d
        return functions[f[0]]
    elif(len(f)==2):
        c = evaluate_random_function(f[1],x,y)
        functions['cos_pi'] = math.cos(math.pi*c)
        functions['sin_pi'] = math.sin(math.pi*c)
        functions['neg'] = -c
        return functions[f[0]]
    else:
        return functions[f[0]]


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    input_range = input_interval_end - input_interval_start
    output_range = output_interval_end - output_interval_start
    input_proportion = (float(val)-float(input_interval_start))/float(input_range)

    new_value = float(output_range)*float(input_proportion)+float(output_interval_start)
    return new_value


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(5, 9)
    green_function = build_random_function(5, 9)
    blue_function = build_random_function(5, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")
    generate_art("1.png")
    generate_art("2.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
