#!/usr/bin/python
# -*- coding: utf8 -*-
import pytest

from src.parameters import \
    IntegerParameter, ParameterException, LimitedIntegerParameter


class TestClass:
    class Foo:
        param = IntegerParameter(default=12)

        def __init__(self, p=None):
            """Toy toy toy"""
            if p:
                self.param = p
            super().__init__()

    def test_int_parameter_default(self):
        test_cls = self.Foo()
        assert test_cls.param == 12

    def test_int_parameter_setter(self):
        test_cls = self.Foo()
        test_cls.param = 100
        assert test_cls.param == 100

    def test_multiple_classes(self):
        test_cls_one = self.Foo(p=123)
        test_cls_two = self.Foo(p=12)
        assert test_cls_one.param != test_cls_two.param

    def test_invalid_type(self):
        test_cls = self.Foo()
        assert isinstance(test_cls, self.Foo)

        with pytest.raises(ParameterException):
            test_cls.param = "SomeString"

    def test_no_delete(self):
        test_cls = self.Foo()

        with pytest.raises(ParameterException):
            del test_cls.param

    def test_multi_params(self):
        class Multiple:
            param1 = IntegerParameter(default=13)
            param2 = IntegerParameter(default=16)

        cls1 = Multiple()
        assert cls1.param1 != cls1.param2

        cls1.param1 = 124
        cls1.param2 = 134
        assert cls1.param1 != cls1.param2

    def test_class_variable(self):
        """Check for the classic class variable problem."""
        class Contained:
            param = IntegerParameter(default=12)

            def __init__(self, p=None):
                """Toy toy toy"""
                if p:
                    self.param = p
                super().__init__()

        test_cls_one = Contained(p=123)
        test_cls_two = Contained()

        test_val = 12341
        Contained.param = test_val

        new_cls = Contained()
        assert new_cls.param is not None
        assert new_cls.param == test_val

        # Instance overwrite test.
        assert test_cls_one != test_val
        # Default overwrite test.
        assert test_cls_two != test_val

    def test_limited_int(self):
        class Limited:
            param = LimitedIntegerParameter(
                default=27, minimum=12, maximum=141)

        test_cls = Limited()
        with pytest.raises(ParameterException):
            test_cls.param = 11

        # Should be fine
        test_cls.param = 12

        with pytest.raises(ParameterException):
            test_cls.param = 142

        # Should be fine
        test_cls.param = 141
