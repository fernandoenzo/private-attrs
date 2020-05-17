# private-attrs

[![PyPI](https://img.shields.io/pypi/v/private-attrs?label=latest)](https://pypi.org/project/private-attrs/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/private-attrs)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/private-attrs)
![PyPI - Status](https://img.shields.io/pypi/status/private-attrs)

![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/fernandoenzo/private-attrs)
[![GitHub last commit](https://img.shields.io/github/last-commit/fernandoenzo/private-attrs)](https://github.com/fernandoenzo/private-attrs)
[![Build Status](https://img.shields.io/travis/com/fernandoenzo/private-attrs?label=tests)](https://travis-ci.com/fernandoenzo/private-attrs)
![Maintenance](https://img.shields.io/maintenance/yes/2020)

This little library, consisting of a single module, provides support for easy addition of **truly private attributes**
 inside classes, which are totally unreachable from outside the class definition, **as in C++ private clause**.

## Table of contents

<!--ts-->
  * [Installation](#installation)
  * [Usage](#usage)
      * [A simple example](#a-simple-example)
      * [An example with proxy=True](#an-example-with-proxytrue)
  * [Contributing](#contributing)
  * [License](#license)
<!--te-->

## Installation

Use the package manager [**pip**](https://pip.pypa.io/en/stable/) to install **private-attrs**.

```bash
pip3 install private-attrs
```

## Usage

This is a simple schema on how a custom class could use private attributes.
```python
from private_attrs import PrivateAttrs

def MyClass():
    p = PrivateAttrs()

    class MyClass:
        def __init__(self):
            p.register_instance(self)
            
        # From now on, we'll define our public attrs with 'self.attr' syntax as usual,
        # and private ones with 'p.attr' or 'p.attr_static'.

        def __del__(self):
            p.delete(self)

    MyClass.__qualname__ = 'MyClass'    

    return MyClass

MyClass = MyClass()  # override the function definition
```
As you can see, we first need to define the class inside a function. Outside that class, but inside the function scope, we
 instantiate a `PrivateAttrs` object.  

Now, inside `MyClass`, if we plan to have private instance attributes, and not just static ones, it's mandatory to
 register, in the `__init__()` method, the instance by calling the `register_instance()` function.

Finally we return `MyClass` and we override the function definition.
- - -

#### A simple example

Let's now dive into a more complete example:

```python
from private_attrs import PrivateAttrs

def Person():
    p = PrivateAttrs()

    class Person:
        def __init__(self, name, social_security_number):
            p.register_instance(self)
            self.name = name
            p.ssn = social_security_number

        @property
        def ssn(self):
            return p.ssn

        def __eq__(self, other):
            return self.ssn == other.ssn

        def __hash__(self):
            return hash(self.ssn)

        def __str__(self):
            return f"{self.name} - {self.ssn}"

        def __del__(self):
            p.delete(self)

    Person.__qualname__ = 'Person'

    return Person

Person = Person()
```
Although a person can change their name, surname or even their sex, it's really unlikely (not to say impossible) for someone
 to change their social security number (SSN).

That's why we store the SSN as a private attribute, safe, unmodifiable, and we can rely on it to compare whether two people
 are the same person.
- - -


#### An example with proxy=True

If we are working with the Python `multiprocessing` library and we want to create a class with private attributes that are
 accessible and modifiable from different running processes (we already know that, unlike threads, processes don't share
  memory space), we need to instantiate the `PrivateAttrs` object with the argument `proxy = True`.  

Let's see an example:

```python
from private_attrs import PrivateAttrs


def Person():
    p = PrivateAttrs(proxy=True)

    class Person:
        def __init__(self, name, social_security_number):
            p.register_instance(self)
            self.name = name
            p.cell_phones = p.manager.list()
            p.ssn = social_security_number

        @property
        def ssn(self):
            return p.ssn

        @property
        def cell_phones(self):
            return tuple(p.cell_phones)

        def add_cell_phone(self, phone):
            p.cell_phones.append(phone)

        def __str__(self):
            return f"{self.name} - {self.ssn} - {self.cell_phones}"

        def __del__(self):
            p.delete(self)

        def __getstate__(self):
            state = dict(self.__dict__)
            state['private'] = p.getstate(self)
            return state

        def __setstate__(self, state):
            private = state.pop('private')
            p.setstate(private, self)
            self.__dict__ = state

    Person.__qualname__ = 'Person'    

    return Person

Person = Person()
```

By doing this, all the private attributes that we store are automatically available in all processes, and you can modify
 them from anyone.

Pay particular attention to certain specific attributes that need to be instantiated using the `Manager` class, such as
 lists or dictionaries. Fortunately, there is an attached manager object in the `PrivateAttrs` class to simplify life for
  the programmer.
 
Also be aware of the need to define `__getstate__()` and `__setstate__()` magic methods as you see them so the class can be
 correctly serialized and deserialized with all its private attributes when shared between processes.

You should know that, the way we wrote this `Person` class, it's impossible for other processes to modify the public 
 `name` attribute and make that change visible for the rest. This is because this attribute has not been instantiated with
  `Manager.Value()` nor inside a `Manager.Namespace()` or similar.

One possible workaround if you don't want to use the mentioned methods for storing shared simple attributes like `str` or
 `int` would be to make them private and then make a getter (`@property`) and a setter for each one. So the former
  `Person` class would look like this:

```python
class Person:
    def __init__(self, name, social_security_number):
        p.register_instance(self)
        p.name = name
        p.cell_phones = p.manager.list()
        p.ssn = social_security_number

    @property
    def name(self):
        return p.name

    @name.setter
    def name(self, name):
        p.name = name

    @property
    def ssn(self):
        return p.ssn

    @property
    def cell_phones(self):
        return tuple(p.cell_phones)

    def add_cell_phone(self, phone):
        p.cell_phones.append(phone)

    def __str__(self):
        return f"{self.name} - {self.ssn} - {self.cell_phones}"

    def __del__(self):
        p.delete(self)

    def __getstate__(self):
        state = dict(self.__dict__)
        state['private'] = p.getstate(self)
        return state

    def __setstate__(self, state):
        private = state.pop('private', self)
        p.setstate(private)
        self.__dict__ = state
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

![PyPI - License](https://img.shields.io/pypi/l/private-attrs)

This library is licensed under the
 [GNU General Public License v3 or later (GPLv3+)](https://choosealicense.com/licenses/gpl-3.0/)