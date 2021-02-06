# pydesign

## Author

macbeth322


## About

Write OpenSCAD with all the niceness of python.


## Installation

```
python3 -m venv venv
source venv/bin/activate
pip install https://github.com/macbeth322/pydesign.git
```


## Usage

```
from pydesign import *

my_model = Cube(10, 10, 10, center=(X, Y, Z))
my_model -= sphere(r=6)
my_model **= Up(10)
my_model += Cube(10 * 2**0.5, 2, 5, center=(X, Y)) ** rotate([0, 0, 45])
my_model.render_to_file('output.scad')
```


`from pydesign import *`: Import all the names from the pydesign DSL.

`Cube(10, 10, 10, center=(X, Y, Z))`: Make a cube using the pydesign syntax; x,
y, and z dimensions and optionally which axes to center on.

`my_model -= sphere(r=6)`: Create a sphere with the standard OpenSCAD syntax,
then subtract it from the cube object created earlier.

`my_model **= Up(10)`: Translate my_model 10mm up the z-axis. This is
equivalent to `my_model **= translate([0, 0, 10])`. The `**` operator applies
the right argument to the left argument, for example the equivalent would be
`my_model =Up(10)(my_model)`.

`my_model += Cube(10 * 2**0.5, 2, 5, center=(X, Y)) ** rotate([0, 0, 45])`:
Create a rectangular prism, rotate it, then union it with my_model. The math to
decide the cube's dimensions is done in python so is exported to OpenSCAD as
literals.

`my_model.render_to_file('output.scad')`: Render my_model to 'output.scad'.


## API

### `_Element`

The python type representing all OpenSCAD objects; e.g. any parenthetical
OpenSCAD expression. `translate([...])` and `cube([...]` are each represented
as `_Element`s. This shouldn't be directly constructed and should be created
via one of the other functions.


#### `_Element.__add__`

Returns a new `_Element` which is `union` of the two arguments.


#### `_Element.__sub__`

Returns a new `_Element` which is `difference` of the two arguments.


#### `_Element.__mul__`

Returns a new `_Element` which is `intersection` of the two arguments.


#### `_Element.__call__`

Returns a new `_Element` where the arguments are added as children to the object
being called.


#### `_Element.__pow__`

Returns a new `_Element` where the right argument of the expression is a parent
of the left argument.


### `X`, `Y`, `Z`

Global constants for use with the `Cube` function.


### `Cube(x, y, z, centers=centers)`

Create a cube element with dimensions x, y, z and centered on the `centers`
axes. `centers` is optional and can be a single axes or an iterable of axes.


### `Up`, `Down`, `Left`, `Right`, `Back`, `Forward`

Create a translate element which translates along one axes in the positive or
negative direction.


### OpenSCAD Names

- `circle`
- `square`
- `polygon`
- `text`
- `Import`
- `projection`
- `sphere`
- `cube`
- `cylinder`
- `polyhedron`
- `linear_extrude`
- `rotate_extrude`
- `surface`
- `translate`
- `rotate`
- `scale`
- `resize`
- `mirror`
- `multmatrix`
- `color`
- `offset`
- `hull`
- `minkowski`
- `union`
- `difference`
- `intersection`

Each of these names will create the associated OpenSCAD element and forward
arguments from python.
