# Super Turtle 

Pablo Pacheco Pérez



<img src = "welcomeSuperTurtle.svg" width = "666">



Convert the Python turtle into a class called SuperTurtle, which provides new functionalities by executing/creating methods within the SuperTurtle class. Create new drawings, including circles, polygons, Cartesian and polar arrays of various shapes, fractals (both recursive and L-system-based), and arrays of figures positioned at specific coordinates.

- Convert the classic Python turtle into a class called superTurtle.
- It will gain new functionalities by executing/creating methods of the superTurtle class.
- Use the methods of the superTurtle class to quickly create new drawings, such as:
    - Circles drawn from the center.
    - Polygons.
    - Cartesian arrays of different shapes (which can be created using other methods of the same class).
    - Polar arrays of shapes.
    - Geometric figures.
    - Fractals using recursive functions.
    - Fractals using the L-system method.
    - Arrays of figures on points with established coordinates.

## Some of the elements:

### Circle: (circulo2)

- **Function Name**: circulo
- **radio**
- **steps**: number of lines that compose the circle
- **colorRelleno**: fillColor

### Polar Array (polararray)

- **nrad**: number of elements in the radial direction
- **nang**: number of elements in the angular direction
- **l0r1**:
    - if 0, the array is created counterclockwise
    - if 1, the array is created clockwise
- **ang**: angle/arc covered by the elements
- **ang0**: initial angle of inclination of the array
- **radio0**: initial radius where the elements of the array start

### Poligon (poligon)

- **n**: number of sides
- **lado**: side length
- **vertex**: True or False, whether the polygon starts from the edge or the vertex

### Cartesian Array (xyarray)

- **lx**: length of the array in X
- **ly**: length of the array in Y
- **nx**: number of elements in the array in X
- **ny**: number of elements in the array in Y
- **center**: False or True, whether the array is centered at the initial point

### Line Array (linearray)

- **nlines**: number of lines
- **lline**: line length
- **startangle**: initial angle of inclination of the array
- **totalangle**: angle/arc covered by the elements
- **l0r1**:
    - if 0, the array is created counterclockwise
    - if 1, the array is created clockwise

## Requirements

It works for me with the following versions:

svg-turtle                0.4.1                    
numpy                     1.21.5          
pandas                    1.4.4           
python                    3.9.13 
matplotlib                3.5.2    

## Examples

Check the examples folder, you will find ipynb files with a wide variety.
