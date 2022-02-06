#!/usr/bin/env python3
# encoding:utf-8


from private_attrs import PrivateAttrs


def Person():
    p = PrivateAttrs()

    class Person:
        def __init__(self, name, surname, social_security_number):
            p.register_instance(self)
            self.name = name
            p.surname_static = surname
            p.ssn = social_security_number

        @property
        def ssn(self):
            return p.ssn

        @property
        def surname(self):
            return p.surname_static

        @surname.setter
        def surname(self, surname):
            p.surname_static = surname

        def __eq__(self, other):
            return self.ssn == other.ssn

        def __hash__(self):
            return hash(self.ssn)

        def __del__(self):
            p.delete(self)

    Person.__qualname__ = 'Person'

    return Person


def PersonProxy():
    p = PrivateAttrs(proxy=True)

    class PersonProxy:
        def __init__(self, name, surname, social_security_number):
            p.register_instance(self)
            self.name = name
            p.surname_static = surname
            p.ssn = social_security_number
            p.cell_phones = p.manager.list()

        @property
        def ssn(self):
            return p.ssn

        @ssn.setter
        def ssn(self, ssn):
            p.ssn = ssn

        @property
        def surname(self):
            return p.surname_static

        @surname.setter
        def surname(self, surname):
            p.surname_static = surname

        @property
        def cell_phones(self):
            return tuple(p.cell_phones)

        def add_cell_phone(self, phone):
            p.cell_phones.append(phone)

        def __eq__(self, other):
            return self.ssn == other.ssn

        def __hash__(self):
            return hash(self.ssn)

        def __getstate__(self):
            state = dict(self.__dict__)
            state['private'] = p.getstate(self)
            return state

        def __setstate__(self, state):
            private = state.pop('private')
            p.setstate(self, private)
            self.__dict__ = state

        def __del__(self):
            p.delete(self)

    PersonProxy.__qualname__ = 'PersonProxy'

    return PersonProxy


Person = Person()
PersonProxy = PersonProxy()
