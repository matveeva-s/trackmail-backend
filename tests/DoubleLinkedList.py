class Node:
    def __init__(self, data, prev, next):
        self.data = data
        self.prev = prev
        self.next = next

class DoubleLinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def clear(self):
        self.__init__()

    def delete(self, x):
        if self.first is None:
            return "Error: you can't delete this element, because list is empty"
        else:
            current = self.first
            while current.next is not None and current.data != x:
                current = current.next
            if current.next is not None:
                if current.prev is None:
                    self.shift()
                    return
                current.next.prev = current.prev
                current.prev.next = current.next
                self.length -=1
            else:
                if current.next is None and current.data == x:
                    self.pop()
                else:
                    return "Element you want to delete doesn't exist in list"

    def contains(self, x):
        if self.first is None:
            return "List is empty"
        else:
            current = self.first
            while current.next is not None and current.data != x:
                current = current.next
            if current.data == x:
                return "Requested item exists in list"
            if current.next is None and current.data !=x:
                return "Requested item not found in list"


    def show(self):
        if self.first == self.last is None:
            return ''
        else:
            current = self.first
            out = str(current.data)
            while current.next is not None:
                current = current.next
                out = out + ' ' + str(current.data)
            return out

    def unshift(self, x):
        self.length +=1
        if self.first is None:
            self.last = self.first = Node(x, None, None)
        else:
            self.first.prev = Node(x, None, self.first)
            self.first = self.first.prev

    def push(self, x):
        self.length += 1
        if self.first is None:
            self.last = self.first = Node(x, None, None)
        else:
            self.last.next = Node (x, self.last, None)
            self.last = self.last.next

    def len(self):
        return self.length

    def pop(self):
        if self.last is None:
            return "Error: list is empty"
        else:
            if self.last == self.first:
                self.clear()
                return
            self.length -= 1
            self.last = self.last.prev
            self.last.next = None

    def shift(self):
        if self.first is None:
            return "Error: list is empty"
        else:
            if self.last == self.first:
                self.clear()
                return
            self.length -= 1
            self.first = self.first.next
            self.last.prev = None

    def first_elem(self):
        if self.first is not None:
            return self.first.data
        else:
            return "Error: list is empty"

    def last_elem(self):
        if self.last is not None:
            return self.last.data
        else:
            return "Error: list is empty"

