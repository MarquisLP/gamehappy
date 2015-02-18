"""This module contains classes for representing in-game images as they
are drawn on-screen.
"""
import pygame.transform
from enum import IntEnum
from pygame.surface import Surface
from pygame.rect import Rect
from game_objects import Component


class Axis(IntEnum):
    """Contains int representations of the possible 2D axes."""
    horizontal = 1
    vertical = 2


class Graphic(Component):
    """A 2D image that can draw itself onto a Surface or another
    Graphic.

    It maintains a position relative to the associated Entity's
    on-screen position and will be drawn there accordingly.
    (For example, if the Entity's position is (30, 30) and this
    Graphic's position is (2, 3), it will be drawn to (32, 33)
    on-screen.)

    Several effects can also be applied to it, such as flipping the
    image and adding or reducing transparency.

    Attributes:
        _image (Surface): Contains the Graphic's actual pixel data.
        _rect (Rect): Contains the Graphic's x and y-offsets relative
            to its associated Entity, as well as its width and height.
    """
    def __init__(self, source, x=0, y=0):
        """Declare and initialize instance variables.

        Args:
            source (Surface): Contains the 2D image associated with this
                Graphic.
            x (int): The x-offset of the Graphic's top-left corner
                relative to its associated Entity.
                The default value is 0.
            y (int): The y-offset of the Graphic's top-left corner
                relative to its associated Entity.
                The default value is 0.
        """
        super(Graphic, self).__init__()
        self._image = source.convert()
        self._image.set_alpha(255)
        self._rect = Rect(x, y, source.get_width(), source.get_height())

    def offset(self, dx=0, dy=0):
        """Move the Graphic away from its original position relative to
        the associated Entity by a set horizontal and/or vertical
        distance.

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
        self._rect.move_ip(int(round(dx)), int(round(dy)))

    def set_position(self, new_x=None, new_y=None):
        """Re-position the Graphic onto an exact location relative to
        its associated Entity.

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
        if new_x is not None:
            self._rect.x = int(round(new_x))
        if new_y is not None:
            self._rect.y = int(round(new_y))

    def get_width(self):
        return self._rect.width

    def get_height(self):
        return self._rect.height

    def center(self, axis, container_rect):
        """Move the associated Entity so that this Graphic is centered
        horizontally and/or vertically within an area of the screen.

        Args:
            axis (Axis): A literal from the Axis enum for specifying
                whether the image should be centered on the horizontal
                or vertical plane.
                To center the image on both planes, you can combine both
                values using the | (bitwise or) operator.
            container_rect (Rect): A Rect containing the position and
                dimensions of the area that this Graphic will be
                centered relative to.
        """
        if (axis & Axis.horizontal) == Axis.horizontal:
            centered_x = (container_rect.width - self.get_width()) / 2
            centered_x += container_rect.x
            self.entity.set_position(new_x=centered_x - self._rect.x)

        if (axis & Axis.vertical) == Axis.vertical:
            centered_y = (container_rect.height - self.get_height()) / 2
            centered_y += container_rect.y
            self.entity.set_position(new_y=centered_y - self._rect.y)

    def is_contained(self, container_rect):
        """Return a Boolean indicating whether this Graphic is
        completely contained within an area of the screen.
        (i.e. No pixels exceed the area's boundaries.)

        Args:
            container_rect (Rect): Contains the position and dimensions
                of the area this Graphic will be compared to.
        """
        if container_rect.contains(self.draw_rect()):
            return True
        else:
            return False

    def is_outside(self, container_rect):
        """Return a Boolean indicating whether this Graphic is
        completely outside of an area of the screen.
        (i.e. All pixels exceed the area's boundaries.)

        Args:
            container_rect (Rect): Contains the position and dimensions
                of the area this Graphic will be compared to.
        """
        if not container_rect.colliderect(self.draw_rect()):
            return True
        else:
            return False

    def draw_rect(self):
        """Return a Rect containing the actual position the Graphic
        will be drawn to, with the Entity's position taken into account.
        """
        return self._rect.move(self.entity.x, self.entity.y)

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

    def magnify(self, zoom):
        """Enlarge or shrink the image using an equal scale for the
        width and height.

        Args:
            zoom (float): The amount used to multiply the image's
                dimensions. For example, passing a value of 2 when the
                image's dimensions are 24x24 will enlarge the image to
                48x48. Passing 0.5 will shrink it to 12x12.
        """
        magnified_image = pygame.transform.scale(self._image,
            (int(round(self.get_width() * zoom)),
             int(round(self.get_height() * zoom))))
        self._image = magnified_image
        self._update_rect_dimensions()

    def resize(self, new_width, new_height):
        """Stretch and/or shrink the image to fit new dimensions.

        Args:
            new_width (int): The width that the image will shrink or
                stretch to fit.
            new_height (int): The height that the image will shrink or
                stretch to fit.
        """
        resized_image = pygame.transform.scale(self._image,
            (int(round(new_width)), int(round(new_height))))
        self._image = resized_image
        self._update_rect_dimensions()

    def _update_rect_dimensions(self):
        """Update the width and height of _rect with the current
        dimensions of _image.
        """
        self._rect.width = self._image.get_width()
        self._rect.height = self._image.get_height()

    def opacify(self, amount):
        """Increase or decrease the image's transparency.

        Note that Graphic images always start with an opacity of 255,
        which is fully opaque.

        Args:
            amount (int): How much to add to the image's opacity value.
                Positive values will make the image more opaque, while
                negative values will make it more transparent.
                To make the image fully opaque, pass 255 or more. To
                make the image fully transparent, pass -255 or less.
        """
        self._image.set_alpha(self._image.get_alpha() + amount)

    def is_opaque(self):
        """Return a Boolean indicating whether the image is fully
        opaque.
        """
        if self._image.get_alpha() >= 255:
            return True
        else:
            return False

    def is_transparent(self):
        """Return a Boolean indicating whether the image is fully
        transparent.
        """
        if self._image.get_alpha() <= 0:
            return True
        else:
            return False

    def blit(self, source, position, rect=None, special_flags=0):
        """Draw a Surface on top of this Graphic.

        Args:
            source (Surface): The image that will be drawn onto this
                Graphic.
            position (tuple of int, int): Contains the x and y-positions
                of the source image relative to this Graphic.
            area (Rect): An optional parameter specifying the region of
                the source image that will be used.
                Leave this parameter blank to draw the entire source
                image.
            special_flags (int): A combination of various PyGame flags
                for blitting effects. See the PyGame documentation on
                Surface.blit() for more information.
                This is an optional parameter; leave it blank to use no
                flags when blitting.

        Returns:
            A Rect containing the region of this Graphic that was drawn
            onto.
        """
        x = position[0]
        y = position[1]
        return self._image.blit(source, (x, y), rect, special_flags)

    def draw(self, destination):
        """Draw this Graphic's image onto of its destination.

        Returns:
            A Rect containing the region of the destination that was
            drawn onto.
        """
        return destination.blit(self._image, self.draw_rect())


class Animation(Graphic):
    """A 2D image that alternates between frames after set time
    intervals.

    As a subclass of Graphic, it can be used in all of the same
    situations as a regular Graphic instance. This is aided by the
    fact that it is added to an Entity under the attribute name
    'graphic', allowing you to write code that affects all Entities'
    graphical Components regardless of whether they are Graphics or
    Animations.

    Attributes:
        _frame_index (int): The ID of the frame currently being shown.
        _frame_counter (int): Keeps track of how many update cycles have
            passed since changing to the current frame. Once it exceeds
            the current frame's duration, the next frame is displayed.
        _frame_durations (list of int): Contains the duration, in
            update cycles, of each frame in order.
        _is_playing_backwards (Boolean): Specifies whether the Animation
            is cycling through its frames in reverse order.
            Animations play forward by default.
        _is_paused (Boolean): Specifies whether the Animation should
            prevent itself from changing the current frame.
            Animations are unpaused by default.
        _held_frame (int): A frame ID; the next time the Animation
            displays this frame, it will immediately pause itself.
            A value less than 0 means that no frame will be held.
    """
    def __init__(self, source, x=0, y=0, *frame_durations):
        """Declare and initialize instance variables.

        Args:
            source (Surface): Contains this Animation's sprite sheet.
            x (int): The x-offset of the top-left corner of this
                Animation relative to its associated Entity.
                The default value is 0.
            y (int): The y-offset of the top-left corner of this
                Animation relative to its associated Entity.
                The default value is 0.
            frame_durations: A set of integers for the duration, in
                update cycles, of each frame in order.
        """
        super(Animation, self).__init__(source, x, y)
        self._frame_index = 0
        self._frame_counter = 0
        self._frame_durations = frame_durations
        self._rect.width = self._calculate_frame_width()
        self._is_playing_backwards = False
        self._is_paused = False
        self._held_frame = -1

    def _calculate_frame_width(self):
        """Return the width, in pixels, of a single frame in this
        Animation.
        """
        return self._image.get_width() / len(self._frame_durations)
