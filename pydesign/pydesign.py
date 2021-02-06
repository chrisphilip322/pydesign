#!/usr/bin/env python3

from __future__ import annotations

import dataclasses
import random
import sys
from typing import *


class _Element:
  def __add__(self, other):
    if not isinstance(other, _Element):
      return NotImplemented
    return _ElementImpl('union', [], {}, [self, other])

  def __sub__(self, other):
    if not isinstance(other, _Element):
      return NotImplemented
    return _ElementImpl('difference', [], {}, [self, other])

  def __mul__(self, other):
    if not isinstance(other, _Element):
      return NotImplemented
    return _ElementImpl('intersection', [], {}, [self, other])

  def render(self, *, extra_globals=dict(), depth=False):
    self = self._resolve()
    all_args = ', '.join(
        [str(arg) for arg in self.args]
        + [f'{k}={v}' for k, v in self.kwargs.items()]
    )
    this = f'{self.name}({all_args})'
    if self.children:
      if len(self.children) > 1:
        this += ' {'
      result = '\n'.join([this] + [child.render(depth=True) for child in self.children])
      if len(self.children) > 1:
        result += '\n}'
    else:
      result = f'{this};'
    if depth:
      return '  ' + result.replace('\n', '\n' + '  ')
    else:
      return '\n'.join([f'{k}={v};' for k, v in extra_globals.items()] + [result])

  def render_to_file(self, fname, *args, **kwargs):
      src_fname = sys.modules['__main__'].__file__
      with open(src_fname) as f:
          src = f.readlines()

      with open(fname, 'w') as f:
          f.write('////// pydesign source\n')
          f.write(f'////// {src_fname}\n')
          f.write(''.join(f'// {line}' for line in src))
          f.write('\n')
          f.write(self.render(*args, **kwargs))
          f.write('\n')


@dataclasses.dataclass(frozen=True)
class _ElementImpl(_Element):
  name: str
  args: list
  kwargs: dict
  children: List[_Element]

  def __post_init__(self):
    object.__setattr__(self, 'children', [child._resolve() for child in self.children])

  def _resolve(self):
    return self

  @classmethod
  def create(cls, name, *args, **kwargs):
    return cls(name, args, kwargs, [])

  @classmethod
  def partial(cls, name):
    return lambda *args, **kwargs: cls.create(name, *args, **kwargs)

  def __pow__(self, other):
    if type(other) is not _ElementImpl:
      return NotImplemented
    return _PowBundle([self, other])

  def __call__(self, child):
    if not isinstance(child, _Element):
      return NotImplemented
    return dataclasses.replace(self, children=self.children + [child])


@dataclasses.dataclass(frozen=True)
class _PowBundle(_Element):
  bundle: List[_ElementImpl]

  def __pow__(self, other):
    if type(other) is _ElementImpl:
      return _PowBundle(self.bundle + [other])
    elif type(other) is _PowBundle:
      return _PowBundle(self.bundle + other.bundle)
    return NotImplemented

  def __rpow__(self, other):
    if type(other) is _ElementImpl:
      return _PowBundle([other] + self.bundle)
    return NotImplemented

  def _resolve(self):
    node = self.bundle[0]
    for other in self.bundle[1:]:
      node = dataclasses.replace(other, children=other.children + [node])
    return node

  def __call__(self, child):
    if not isinstance(child, _Element):
      return NotImplemented
    return dataclasses.replace(self, bundle=[child] + self.bundle)


def _make_mono_dir_translate(vec):
    return lambda dist: _ElementImpl.create('translate', [x * dist for x in vec])


NAMES = ('''\
circle
square
polygon
text
projection
sphere
cube
cylinder
polyhedron
linear_extrude
rotate_extrude
surface
translate
rotate
scale
resize
mirror
multmatrix
color
offset
hull
minkowski
union
difference
intersection'''.splitlines())
for name in NAMES:
  locals()[name] = _ElementImpl.partial(name)

Import = _ElementImpl.partial('import')

for name, vec in {
    'Up': (0, 0, 1),
    'Down': (0, 0, -1),
    'Left': (-1, 0, 0),
    'Right': (1, 0, 0),
    'Back': (0, -1, 0),
    'Forward': (0, 1, 0),
}.items():
    locals()[name] = _make_mono_dir_translate(vec)


class X: pass
class Y: pass
class Z: pass


def Cube(x, y, z, center=tuple()):
    try:
        center = frozenset(center)
    except:
        center = frozenset((center,))
    return cube([x, y, z]) ** translate([
        -x/2 * (1 if X in center else 0),
        -y/2 * (1 if Y in center else 0),
        -z/2 * (1 if Z in center else 0),
    ])


def _main():
    return Cube(10, 20, 30, center=X).render()


if __name__ == '__main__':
  print(_main())
