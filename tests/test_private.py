#!/usr/bin/env python3
# encoding:utf-8

from unittest import TestCase, main

from tests.person import Person


class TestPrivate(TestCase):

    def test_person_with_private_attrs(self):
        p1 = Person(name='John', surname='Doe', social_security_number=123)
        p2 = Person(name='Alice', surname='Jackson', social_security_number=123)
        p3 = Person(name='James', surname='Potter', social_security_number=456)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        # We cannot change the value of 'ssn' since it's private and we only have defined a getter for it.
        self.assertRaises(AttributeError, p1.__setattr__, 'ssn', 456)
        self.assertEqual(p1.ssn, 123)
        self.assertEqual(p3.ssn, 456)

    def test_person_with_private_static_attrs(self):
        # Since 'surname' is a static attribute, it's shared between all instances.
        p1 = Person(name='John', surname='Doe', social_security_number=123)
        p2 = Person(name='Alice', surname='Jackson', social_security_number=456)
        self.assertEqual(p1.surname, 'Jackson')
        p1.surname = 'Potter'
        self.assertEqual(p2.surname, 'Potter')


if __name__ == '__main__':
    main()
