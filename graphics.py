"""This module contains classes for representing in-game images as they
are drawn on-screen.
"""
from pygame.surface import Surface
from pygame.rect import Rect


class Graphic(object):
    """A 2D image that can draw itself onto a Surface or another
    Graphic.

    It will automatically keep track of its position relative to its
    destination Surface/Graphic.
    Several effects can also be applied to it, such as flipping the
    image or adding and reducing transparency.

    Attributes:
        _image (Surface): Contains the Graphic's actual pixel data.
        _rect (Rect): Contains the Graphic's x and y-positions relative
            to _destination, as well as its width and height.
        _destination (Surface/Graphic): The visual object that will have
            _image blitted on top of it. This Graphic will remain bound
            to only one destination for its entire lifetime.
    """
    def __init__(self, source, destination, x, y):
        """Declare and initialize instance variables.

        Args:
            source (Surface): Contains the 2D image associated with this
                Graphic.
            destination (Surface/Graphic): The visual object that this
                Graphic will be drawn onto for the entire time it exists
                in memory.
            x (int): The x-position of the Graphic's top-left corner
                relative to its destination.
            y (int): The y-position of the Graphic's top-left corner
                relative to its destination.
        """
        self._image = source
        self._rect = Rect(x, y, source.get_width(), source.get_height())
        self._destination = destination
