import unittest
#from DoubleLinkedList import DoubleLinkedList

#import sys
#sys.path.insert(0, '/home/svetlana/backend/app')
#import DoubleLinkedList

from app.DoubleLinkedList import DoubleLinkedList

class TestClass (unittest.TestCase):
    def test_push (self):
        mylist = DoubleLinkedList()
        mylist.push(2)
        mylist.push('s')
        mylist.push('qwerty')
        mylist.push(3.1415)
        self.assertEqual(mylist.show(),'2 s qwerty 3.1415')
        self.assertEqual(mylist.len(), 4)

    def test_unshift(self):
        mylist = DoubleLinkedList()
        mylist.unshift(2)
        mylist.unshift('s')
        mylist.unshift('qwerty')
        mylist.unshift(3.1415)
        self.assertEqual(mylist.show(), '3.1415 qwerty s 2')
        self.assertEqual(mylist.len(), 4)

    def test_first_elem(self):
        mylist = DoubleLinkedList()
        #test on empty list
        self.assertEqual(mylist.first_elem(), "Error: list is empty")
        mylist.push(1)
        #test on list with single elem
        self.assertEqual(mylist.first_elem(), 1)
        #test on normal list
        mylist.unshift(2)
        self.assertEqual(mylist.first_elem(), 2)
        self.assertEqual(mylist.len(), 2)

    def test_last_elem(self):
        mylist = DoubleLinkedList()
        # test on empty list
        self.assertEqual(mylist.last_elem(), "Error: list is empty")
        mylist.push(1)
        # test on list with single elem
        self.assertEqual(mylist.last_elem(), 1)
        # test on normal list
        mylist.unshift(2)
        self.assertEqual(mylist.last_elem(), 1)
        self.assertEqual(mylist.len(), 2)

    def test_pop(self):
        mylist = DoubleLinkedList()
        # test on empty list
        self.assertEqual(mylist.pop(), "Error: list is empty")
        self.assertEqual(mylist.len(), 0)
        # test on list with single elem
        mylist.push(9)
        mylist.pop()
        self.assertEqual(mylist.show(), '')
        self.assertEqual(mylist.len(), 0)
        # test on normal list
        for i in range(3):
            mylist.push(i + 1)
        mylist.pop()
        self.assertEqual(mylist.show(), '1 2')
        self.assertEqual(mylist.len(), 2)

    def test_shift(self):
        mylist = DoubleLinkedList()
        # test on empty list
        self.assertEqual(mylist.shift(), "Error: list is empty")
        self.assertEqual(mylist.len(), 0)
        # test on list with single elem
        mylist.push(8)
        mylist.shift()
        self.assertEqual(mylist.show(), '')
        self.assertEqual(mylist.len(), 0)
        # test on normal list
        for i in range(3):
            mylist.push(i + 1)
        mylist.shift()
        self.assertEqual(mylist.show(), '2 3')
        self.assertEqual(mylist.len(), 2)

    def test_clear(self):
        mylist = DoubleLinkedList()
        # test on empty list
        mylist.clear()
        self.assertEqual(mylist.show(), '')
        self.assertEqual(mylist.len(), 0)
        # test on normal list
        for i in range(3):
            mylist.push(i + 1)
        mylist.clear()
        self.assertEqual(mylist.show(), '')
        self.assertEqual(mylist.len(), 0)

    def test_delete(self):
        mylist = DoubleLinkedList()
        # test on empty list
        self.assertEqual(mylist.delete(1), "Error: you can't delete this element, because list is empty")
        # test on list with single elem
        mylist.unshift(7)
        mylist.delete(7)
        self.assertEqual(mylist.show(), '')
        # test on normal list
        for i in range(4):
            mylist.push(i+1) # now list is: 1 2 3 4
        mylist.delete(3) #try to delete existing middle elem
        self.assertEqual(mylist.show(), '1 2 4')
        self.assertEqual(mylist.len(), 3)
        mylist.delete(4) #try to delete existing last elem
        self.assertEqual(mylist.show(), '1 2')
        self.assertEqual(mylist.len(), 2)
        mylist.delete(1) #try to delete existing first elem
        self.assertEqual(mylist.show(), '2')
        self.assertEqual(mylist.len(), 1)
        mylist.delete(8) #try to delete non-existing elem
        self.assertEqual(mylist.show(), '2')
        self.assertEqual(mylist.len(), 1)

    def test_contains(self):
        mylist = DoubleLinkedList()
        # test on empty list
        self.assertEqual(mylist.contains(3), "List is empty")
        # test on normal list
        for i in range(4):
            mylist.push(i + 1)
        self.assertEqual(mylist.contains(2), "Requested item exists in list") #consist on middle of list
        self.assertEqual(mylist.contains(1), "Requested item exists in list")  # consist on begin of list
        self.assertEqual(mylist.contains(4), "Requested item exists in list") #consist on end of list
        self.assertEqual(mylist.contains(8), "Requested item not found in list") #consist non-consisng elem list


if __name__ == '__main__':
    unittest.main()

