#!/usr/bin/env python3
# encoding:utf-8

"""
This module provides support for easy addition of private attributes inside your custom objects,
which are totally unreachable from outside the class definition, as in C++ 'private' clause.
"""

import inspect
from multiprocessing import Manager
from typing import Dict, Any, Tuple


def PrivateAttrs(proxy=False):
    '''
    Create a brand new PrivateAttrs instance. If 'proxy' is True, then the stored attributes are shared
    between processes, as long as those attributes are also proxy objects when they are mutable, like lists or dictionaries.
    :param proxy: Whether the stored attributes have to be shared between processes. False by default.
    :return: An independent and empty PrivateAttrs instance.
    '''

    # In this dict we store the private attributes of each instance,
    # following this pattern { id(self): { "attr1": val1, "attr2": val2, ...}, }
    # with self as the object instance.
    private_attrs: Dict[int, Dict[str, Any]] = {}

    # In this dict we store the private static attributes, which are
    # shared between all the instances of a same object.
    static_private_attrs: Dict[str, Any] = {}

    if proxy:
        m = Manager()
        private_attrs: Dict[int, Dict[str, Any]] = m.dict()
        static_private_attrs: Dict[str, Any] = m.dict()

    def get_instance():
        return inspect.currentframe().f_back.f_back.f_locals['self']

    class PrivateAttrs:

        def __init__(self):
            if proxy:
                super().__setattr__('manager', m)

        @staticmethod
        def register_instance(instance: object) -> None:
            '''
            We need to register the instance in the PrivateAttrs object before starting storing our own attributes. This
            method must be called in the class __init__() method, and only once. It will create an empty dictionary
            to store the private attrs of the instance.
            :param instance: The object instance.
            '''
            if private_attrs.get(id(instance)) is None:
                if proxy:
                    private_attrs[id(instance)] = m.dict()
                else:
                    private_attrs[id(instance)] = {}

        @staticmethod
        def delete(instance: object) -> None:
            '''
            Call this method inside, and only inside, the __del__() method of your custom class to avoid
            really unlikely but possible references problems.
            :param instance: The object instance.
            '''
            # Needs to be in a try-except block because of unexpected errors
            try:
                private_attrs.pop(id(instance), None)
            except:
                pass

        @staticmethod
        def get_private_attr(name: str, instance: object, exception: bool = True, default: Any = None) -> Any:
            '''
            Retrieve a private attribute from an object instance.
            :param name: Name of the attribute.
            :param instance: The object instance.
            :param exception: Whether this method should raise an AttributeError or not if the attribute does not exist.
            True by default.
            :param default: Default value to return if 'exception' is False and the attribute does not exist. None by default.
            '''
            try:
                return private_attrs[id(instance)][name]
            except KeyError:
                if exception:
                    raise AttributeError(f"'{type(instance)}' object has no private attribute '{name}'")
            return default

        def __getattr__(self, item):
            if item.endswith('_static'):
                return self.get_static_private_attr(item)
            instance = get_instance()
            return self.get_private_attr(name=item, instance=instance)

        @staticmethod
        def set_private_attr(name: str, value: Any, instance: object) -> None:
            '''
            Create or modify, if already exists, a private attribute in a object instance.
            :param name: Name of the attribute.
            :param value: Value of the attribute.
            :param instance: The object instance.
            :param return: None
            '''
            private_attrs[id(instance)][name] = value

        def __setattr__(self, key, value):
            if key.endswith('_static'):
                self.set_static_private_attr(name=key, value=value)
            else:
                instance = get_instance()
                self.set_private_attr(name=key, value=value, instance=instance)

        @staticmethod
        def del_private_attr(name: str, instance: object) -> None:
            '''
            Remove a private attribute from an object instance.
            This method always returns None, even if the attribute doesn't exist.
            :param name: Name of the attribute to remove.
            :param instance: The object instance.
            :return: None
            '''
            private_attrs[id(instance)].pop(name, None)

        def __delattr__(self, item):
            if item.endswith('_static'):
                self.del_static_private_attr(name=item)
            else:
                instance = get_instance()
                self.del_private_attr(item, instance)

        @staticmethod
        def get_static_private_attr(name: str, exception: bool = True, default: Any = None) -> Any:
            '''
            Retrieve a private static attribute from a class.
            :param name: Name of the static attribute.
            :param exception: Whether this method should raise an AttributeError or not if the attribute does not exist.
            True by default.
            :param default: Default value to return if 'exception' is False and the attribute does not exist. None by default.
            '''
            try:
                return static_private_attrs[name]
            except KeyError:
                if exception:
                    raise AttributeError(f"This class has no private static attribute '{name}'")
            return default

        @staticmethod
        def set_static_private_attr(name: str, value: Any) -> None:
            '''
            Create or modify, if already exists, a private static attribute in a class.
            :param name: Name of the static attribute.
            :param value: Value of the static attribute.
            :param return: None
            '''
            static_private_attrs[name] = value

        @staticmethod
        def del_static_private_attr(name: str) -> None:
            '''
            Remove a private static attribute from a class.
            This method always returns None, even if the attribute doesn't exist.
            :param name: Name of the static attribute to remove.
            '''
            static_private_attrs.pop(name, None)

        @staticmethod
        def getstate(instance: object) -> Tuple[int, Dict[str, Any], Dict[str, Any]]:
            uid, private = id(instance), private_attrs[id(instance)]
            return uid, private, static_private_attrs

        @staticmethod
        def setstate(state: Tuple[int, Dict[str, Any], Dict[str, Any]], instance: object):
            uid, private, static = state
            private_attrs[id(instance)] = private_attrs[uid] if uid in private_attrs.keys() else private
            for key in static.keys():
                if key not in static_private_attrs.keys():
                    static_private_attrs[key] = static[key]

    PrivateAttrs.__qualname__ = 'PrivateAttrs'

    return PrivateAttrs()
