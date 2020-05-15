#!/usr/bin/env python3
# encoding:utf-8
from multiprocessing import Manager
from unittest import TestCase, main

from tests.person import PersonProxy


class TestPrivate(TestCase):

    def test_person_proxy_equals(self):
        m = Manager()
        p1 = PersonProxy(name='John', surname='Doe', social_security_number=123)
        p2 = PersonProxy(name='Alice', surname='Jackson', social_security_number=123)
        p3 = PersonProxy(name='James', surname='Potter', social_security_number=456)
        ls = m.list((p1, p2, p3))
        p1_ls, p2_ls, p3_ls = ls
        for p, p_ls in {p1: p1_ls, p2: p2_ls, p3: p3_ls}.items():
            self.assertNotEqual(id(p), id(p_ls))
            self.assertEqual(p, p_ls)
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)
        p1.ssn = 456
        self.assertEqual(p1, p1_ls)
        self.assertNotEqual(p1, p2)
        self.assertEqual(p1, p3)

    def test_person_proxy_with_non_shared_attribute(self):
        '''
        We see here that there is no way to modify a public simple 'str' attribute like 'name' if the instance is handled as a proxy.
        '''
        m = Manager()
        p1 = PersonProxy(name='John', surname='Doe', social_security_number=123)
        ls = m.list((p1,))
        p1_ls, = ls
        self.assertEqual(p1.name, p1_ls.name)
        self.assertNotEqual(id(p1_ls), id(ls[0]))  # Two different objects, but they should be the same. It's because of the existence of a non-shared attribute.
        p1.name = 'Harry'
        p1_ls.name = 'James'  # This 'name' attribute has nothing to do with p1.name. They are completely independet one from each other.
        ls[0].name = 'Sirius'  # This line does nothing. The name cannot be changed.
        self.assertEqual(p1.name, 'Harry')
        self.assertEqual(p1_ls.name, 'James')
        self.assertNotEqual(ls[0].name, 'Sirius')
        self.assertEqual(ls[0].name, 'John')

    def test_person_proxy_with_shared_attribute(self):
        '''
        Unlike the previous test, here we see that we can change the value of a simple 'int' private attribute, even if the instance is handled as a proxy.
        '''
        m = Manager()
        p1 = PersonProxy(name='John', surname='Doe', social_security_number=123)
        ls = m.list((p1,))
        p1_ls, = ls
        self.assertEqual(p1.ssn, p1_ls.ssn)
        p1.ssn = 456  # The change is also visible from the p1_ls object since it's a shared attribute (because of proxy=True)
        self.assertEqual(p1_ls.ssn, 456)
        p1_ls.ssn = 789
        self.assertEqual(p1.ssn, 789)

    def test_person_proxy_list(self):
        '''
        Here we see that we can modify a 'list' attribute (regardless of whether it's public or private) as long as it has been created with a manager.
        '''
        m = Manager()
        p1 = PersonProxy(name='John', surname='Doe', social_security_number=123)
        ls = m.list((p1,))
        p1_ls, = ls
        self.assertTrue(not p1.cell_phones)  # The list of cell phones is empty
        p1_ls.add_cell_phone(674123)  # We add one phone number to p1_ls.cell_phones
        self.assertTrue(674123 in p1.cell_phones)  # We p1 again and now we see that its cell phones list is no longer empty

    def test_person_proxy_with_private_static_attrs(self):
        # Since 'surname' is a static attribute, it's shared between all instances, even if those instances are being handled as proxies.
        m = Manager()
        p1 = PersonProxy(name='John', surname='Doe', social_security_number=123)
        p2 = PersonProxy(name='Alice', surname='Jackson', social_security_number=456)
        ls = m.list((p1, p2))
        p1_ls, p2_ls = ls
        self.assertEqual(p1.surname, 'Jackson')
        p1_ls.surname = 'Potter'  # We modify the 'surname' in the p1_ls object
        self.assertEqual(p1.surname, 'Potter')
        self.assertEqual(p1.surname, p2.surname)  # and the change is visible from the rest of instances
        self.assertEqual(p1.surname, p2_ls.surname)


if __name__ == '__main__':
    main()
