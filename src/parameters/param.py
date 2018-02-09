#!/usr/bin/python
# -*- coding: utf8 -*-
from typing import Any

from .exceptions import ParameterException


class _Parameter:
    """
    ### Descriptor ###
    Enables control of the limits of the instance variable (type, value).
    Custom class since I'm assuming a lot of parameters wil be created in a
    game and this will create a level of protection during runtime.
    """
    name: str = None
    type: Any = None
    cast: bool = False
    default: Any = None

    def __setter__(self, value: Any, key: str) -> Any:
        """Checks for type if applicable."""
        if not self.cast:
            return value

        if not isinstance(value, self.type):
            try:
                return self.type(value)
            except ValueError as e:
                raise ParameterException(
                    f"Given value {value} cannot be cast to {self.type} on "
                    f"parameter {self.name}. Attribute: {key}.")

    def __init__(self, cast: bool=False, default: Any=None):
        """
        :param cast:
            Enable to attempt type conversion if value is not of self.type
        :param default:
            Value to be returned if None configured by other means.
        """
        self.default = self.__setter__(value=default, key='default')
        self.cast = cast

    def __get__(self, instance, owner=None):
        return instance.__dict__.get(self.name, self.default)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = \
            self.__setter__(value=value, key='value')

    def __delete__(self, instance):
        raise ParameterException(
            f"It is impossible to delete the parameter {self.name} on "
            f"{instance.__class__.__qualname__}.")


class IntegerParameter(_Parameter):
    type = int


class FloatParameter(_Parameter):
    type = float


class MinMaxParameter(_Parameter):
    """
    Allows for a parameter to support a minimum and maximum value, for as long
    as the given type supports the comparison operators.
    """
    minimum = None
    maximum = None

    def __init__(self, minimum, maximum, **kwargs):

        self.minimum = minimum
        self.maximum = maximum
        super(MinMaxParameter, self).__init__(**kwargs)


class LimitedIntegerParameter(IntegerParameter, MinMaxParameter):
    pass


class LimitedFloatParameter(FloatParameter, MinMaxParameter):
    pass
