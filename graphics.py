"""This module contains classes for representing in-game images as they
are drawn on-screen.
"""
import pygame.transform
from enum import IntEnum
from pygame.surface import Surface
from pygame.rect import Rect


class Axis(IntEnum):
    """Contains int representations of the possible 2D axes."""
    horizontal = 1
    vertical = 2


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

    def move(self, dx=0, dy=0):
        """Move the Graphic a set horizontal and/or vertical distance in
        pixels.

        It is safe to pass floats as arguments to this method; they will
        automatically be rounded to the nearest whole number.

        Args:
            dx (int): The horizontal distance to travel. A positive
                value will move the Graphic to the right, while a
                negative value will move it to the left.
                Defaults to 0.
            dy (int): The vertical distance to travel. A positive value
                will move the Graphic down, while a negative value will
                move it up.
                Defaults to 0.
        """
        self._rect.move(int(round(dx)), int(round(dy)))

    def set_position(self, new_x=None, new_y=None):
        """Re-position the Graphic onto an exact location relative to
        its destination.

        It is safe to pass floats as arguments to this method; they will
        automatically be rounded to the nearest whole number.

        Args:
            new_x (int): The x-coordinate of the top-left corner for the
                Graphic's new position.
                This parameter is optional; you can omit it from the
                function call if you want to retain the Graphic's
                x-position.
            new_y (int): The y-coordinate of the top-left corner for the
                Graphic's new position.
                This parameter is optional; you can omit it from the
                function call if you want to retain the Graphic's
                y-position.
        """
        self._rect.x = int(round(new_x))
        self._rect.y = int(round(new_y))

    def get_width(self):
        return self._rect.width

    def get_height(self):
        return self._rect.height

    def destination_width(self):
        return self._destination.get_width()

    def destination_height(self):
        return self._destination.get_height()

    def is_contained(self):
        """Return a Boolean indicating whether the entire image is
        within the bounds of its destination.

        For example, if this Graphic's destination is the Surface
        representing the screen, this method will return True if every
        pixel of the image is on-screen.
        """
        bounds = Rect(0, 0, self.destination_width(),
            self.destination_height())
        if bounds.contains(self._rect):
            return True
        else:
            return False

    def is_outside(self):
        """Return a Boolean indicating whether the entire image is out
        of the bounds of its destination.

        For example, if this Graphic's destination is the Surface
        representing the screen, this method will return True if all
        pixels in the image are off-screen.
        """
        if ((self._rect.x + self.get_width() < 0) or
                (self._rect.x > self.destination_width()) or
                (self._rect.y + self.get_height() < 0) or
                (self._rect.y > self.destination_height())):
            return True
        else:
            return False

    def center(self, axis):
        """Center the image horizontally and/or vertically on its
        destination.

        Args:
            axis (Axis): A literal from the Axis enum for specifying
                whether the image should be centered on the horizontal
                or vertical plane.
                To center the image on both planes, you can combine both
                values using the | (bitwise or) operator.
        """
        if (axis & Axis.horizontal) == Axis.horizontal:
            centered_x = (self.destination_width() - self.get_width()) / 2
            self.set_position(new_x=centered_x)

        if (axis & Axis.vertical) == Axis.vertical:
            centered_y = (self.destination_height() - self.get_height()) / 2
            self.set_position(new_y=centered_y)

    def flip(self, axis):
        """Flip the image horizontally and/or vertically.

        Args:
            axis (Axis): A literal from the Axis enum for specifying
                whether to apply a horizontal or vertical flip.
                To flip the image both ways, you can combine both values
                using the | (bitwise or) operator.
        """
        if (axis & Axis.horizontal) == Axis.horizontal:
            self._image = pygame.transform.flip(self._image, True, False)
        if (axis & Axis.vertical) == Axis.vertical:
            self._image = pygame.transform.flip(self._image, False, True)
