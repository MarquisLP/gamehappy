"""This module contains base classes for defining game objects as well
as their individual components and behaviours.
"""
from inspect import getargspec
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
        x (int): The x-position of the Entity relative to the screen.
        y (int): The y-position of the Entity relative to the screen.
        components (list): Contains all of the Component objects that
            are contained in this Entity.
        * Note that components will also be added as unique attributes
          automatically. This will make it possible to access each
          component directly, rather than having to add .components.
          in-between this Entity's name and the component's name.
    """
    def __init__(self, x, y, *components):
        """Declare and initialize instance variables.

        Args:
            x (int): The x-position of the Entity relative to the
                screen.
            y (int): The y-position of the Entity relative to the
                screen.
            *components: The Component objects that make up this Entity.
        """
        self.x = x
        self.y = y
        self.components = []
        self.add_component(*components)

    def add_component(self, *components):
        """Bind one or multiple components to this Entity.

        Args:
            *components: One or more Component objects that will be
                bound to this Entity.
        """
        for component in components:
            self.components.append(component)
            component.bind_to_entity(self)

    def update(self, time):
        """Update all Components in this Entity.

        Args:
            time (float): The amount of time elapsed, in seconds, since
                the last update cycle.
        """
        for component in self.components:
            # Some Components may not require time for their operations.
            if self._component_takes_time_argument(component):
                component.update(time)
            else:
                component.update()

    def _component_takes_time_argument(self, component):
        """Return a Boolean indicating whether the Component's update()
        method requires the time parameter to be passed to it.

        Args:
            component (Component): The Component to check.
        """
        if len(getargspec(component.update)[0]) > 0:
            return True
        else:
            return False

    def send_message(self, message_type, *details):
        """Broadcast data to all Component objects within this Entity.

        Args:
            message_type (EnumType): One of the values from an Enum
                class. This is used to classify the data being passed.
                For example, if you had an Enum class called
                MessageType, passing MessageType.enemy_collision would
                indicate that the Entity collided with an enemy.
            details: A set of data to be read and interpreted by each
                Component, based on the type of message. The number of
                arguments, as well as each one's type, should correspond
                to the message type.
                For example, if the message type was
                MessageType.enemy_collision, the details could contain
                the amount of damage, knockback, and hitstun.
        """
        for component in self.components:
            component.receive_message(message_type, details)


class Component(object):
    """Part of an Entity object.

    It will handle one facet of the Entity, which can be graphics,
    physics, or part of its behaviour. Subclasses should define their
    own attributes and methods in order to accomplish this.

    Ideally, a game would have many Component subclasses to define the
    many different parts that make up different game objects.

    To communicate with other Components in the same Entity, a simple
    messaging system is used via the Entity's send_message() and each
    Component's receive_message().
    For example, a Physics component can call the Entity's
    send_message() passing data about a collision, and other Components
    can decide how to react to that data based on their
    receive_message().
    In order for this to work, it is highly recommended that you create
    your own Enum class for classifying the types of messages that can
    be sent. (You could call it MessageType, for example.) Every game
    will require different types of interaction between Components,
    which is why a default message Enum is not included with this
    library.

    Attributes:
        entity (Entity): This Component is bound to it and has access
            to all of its members.
    """
    def __init__(self, *args):
        """Declare and initialize instance variables.

        Subclasses can override this method with their own unique
        parameters. However, make sure to call this as a super method in
        order to initialize the entity attribute.
        """
        self.entity = None

    def bind_to_entity(self, entity):
        """Bind this Component to an Entity object.

        Args:
            entity (Entity): This component will be bound to it and have
                access to all of its members.
        """
        self.entity = entity
        self._add_self_as_attribute(entity)

    def _add_self_as_attribute(self, entity):
        """Add this Component as a new attribute in an Entity object.

        Note that this will overwrite an existing Component in the
        Entity if it is of the same class as this one.

        Args:
            entity (Entity): Will receive this Component as an
                attribute.
        """
        class_name = type(self).__name__
        setattr(entity, class_name.lower(), self)

    def update(self, time):
        """Update the processes within this Component.

        Subclasses have the option of overriding this method in order to
        provide periodic behaviour. If the component does not require
        updates after each game cycle, don't override this method.

        You may also choose to omit the time parameter when overriding,
        if the component does not need to perform any time-based
        operations.

        Args:
            time (float): The amount of time, in seconds, that have
                elapsed since the last update cycle.
        """
        pass

    def receive_message(self, message_type, *details):
        """Act on a set of data received from another Component within
        the containing Entity.

        Args:
            message_type (EnumType): One of the values from an Enum
                class. This is used to classify the data being passed.
                For example, if you had an Enum class called
                MessageType, passing MessageType.enemy_collision would
                indicate that the Entity collided with an enemy.
            details: A set of data to be read and interpreted by each
                Component, based on the type of message. The number of
                arguments, as well as each one's type, should correspond
                to the message type.
                For example, if the message type was
                MessageType.enemy_collision, the details could contain
                the amount of damage, knockback, and hitstun.
        """
        raise NotImplementedError
