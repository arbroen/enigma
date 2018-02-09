#!/usr/bin/python
# -*- coding: utf8 -*-
from typing import Any

from .exceptions import ParameterException


class _Parameter:
    """
    ### Descriptor Protocol ###

    Enables control of the limits of the instance variable (type, value).
    Custom class since I'm assuming a lot of parameters wil be created in a
    game and this will create a level of protection during runtime.
    """
    type: Any = None
    cast: bool = False
    name: str = None
    default: Any = None

    def __caster__(self, value: Any, key: str) -> Any:
        """Checks for type if applicable."""
        if self.type is None or isinstance(value, self.type):
            return value
        else:
            try:
                return self.type(value)
            except (ValueError, TypeError):
                raise ParameterException(
                    f"Given value {value} cannot be cast to {self.type} on "
                    f"parameter {self.__class__.__qualname__}. Attr: {key}.")

    def __init__(self, default: Any=None):
        """
        :param default:
            Value to be returned if None configured by other means.
        """
        self.default = self.__caster__(value=default, key='default')

    def __get__(self, instance, owner=None):
        return instance.__dict__.get(self, self.default)

    def __set__(self, instance, value):
        instance.__dict__[self] = \
            self.__caster__(value=value, key='value')

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

    def __min_max__(self, value):
        if self.maximum < value or value < self.minimum:
            raise ParameterException(
                f"Value outside allowed range "
                f"({self.maximum}-{value}-{self.minimum}).")

    def __init__(self, minimum, maximum, default):
        self.minimum = minimum
        self.maximum = maximum
        self.__min_max__(value=default)
        super(MinMaxParameter, self).__init__(default)

    def __set__(self, instance, value):
        self.__min_max__(value=value)
        super().__set__(instance=instance, value=value)


class LimitedIntegerParameter(IntegerParameter, MinMaxParameter):
    pass


class LimitedFloatParameter(FloatParameter, MinMaxParameter):
    pass
