"""This module contains base classes for defining game objects as well
as their individual components and behaviours.
"""
from pygame.sprite import Sprite


class Entity(Sprite):
    """An object within the game.

    It contains several Component objects that are used to define how it
    is handled graphically and physically, as well as its behaviour.

    Since it inherits from PyGame's Sprite class, it can be added to
    any Groups you have created. (Components will automatically add it
    to the appropriate Groups.)
    This also makes discarding it from the game simple, as it will
    automatically be removed from memory once it belongs to no Groups.

    Attributes:
        components (list): Contains all of the Component objects that
            are contained in this Entity.
        * Note that components will also be added as unique attributes
          automatically. This will make it possible to access each
          component directly, rather than having to add .components.
          in-between this Entity's name and the component's name.
    """
    components = []
