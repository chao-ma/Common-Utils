"""
Make a single iterator work with nested for-loop
Use case:
for slice in IteratorSlicer([1,2,3,4,5,6], 3):
    for item in slice:
        func(item)
slice_list([1,2,3,4,5,6], 3) -> [[1,2,3],[4,5,6]]
slice_list([1,2,3,4,5,6], 3) -> [[1,2,3,4],[5,6]]
Note: slice_list is to demonstrate the usage, it doesn't mean it is the best way to slice list.
To slice list, see list_utils.slice_list

Sometimes we need to deal with database. For performance, we usually don't read row by row. Instead
we do bulk fetch: read 1024 rows everytime
for collection in read(cursor, 1024):
    for item in collection:
        func(item)
BufferedIteratorSlicer is for this purpose
I am using list as demonstration
DemoReader reads length of size elements
list(BufferedIteratorSlicer([1,2,3,4,5,6,7,8],4)) -> [[1,2,3,4], [5,6,7,8]]

Python iterator definition does not have has_next function. I am adding it here: ExtendedIterator
e_iter = ExtendedIterator(iter([1,2,3,4,5]))
list(e_iter) -> [1,2,3,4,5]

e_iter = ExtendedIterator(iter([1,2,3]))
e_iter.has_next()   -> True
e_iter.next()       -> 1
e_iter.next()       -> 2
e_iter.has_next()   -> True
e_iter.next()       -> 3
e.has_next()        -> False
e.next()        -> StopIteration exception
"""

class IteratorSlicer(object):

    def __init__(self, iterable, length):
        self.length = int(length)
        assert self.length > 0
        self.iterator = iter(iterable)
        self.index = -1;

    def __iter__(self):
        return self

    def next(self):
        # None indicates outer loop should quit as input interator quited
        if self.index is None:
            raise StopIteration
        if self.index == -1:
            self.index = 0
            return self
        if self.index == self.length:
            self.index = -1
            raise StopIteration
        try:
            obj = next(self.iterator)
            self.index += 1
        except StopIteration:
            self.index = None
            raise StopIteration
        return obj

def slice_list(input_list, length):
    ret_value = list()
    for iter in IteratorSlicer(input_list, length):
        slice = list(iter)
        if slice:
            ret_value.append(slice)
    return ret_value

class DemoReader(object):

    def __init__(self, input_list, size):
        self.input_list = input_list
        self.size = size
        self.cursor = 0

    def has_next(self):
        return self.cursor < len(self.input_list)

    def next(self):
        if not self.has_next():
            raise StopIteration
        ret_value = self.input_list[self.cursor: self.cursor+self.size]
        self.cursor += self.size
        return ret_value


class BufferedIteratorSlicer(object):

    def __init__(self, iterable, length):
        self.reader = DemoReader(iterable, length)

    def __iter__(self):
        return self

    def next(self):
        if self.reader.has_next():
            return self.reader.next()
        raise StopIteration



class ExtendedIterator(object):
    
    def __init__(self, iterator):
        self.iterator = iterator
        self.element = None
        self._has_next = True
        self._next()

    def __iter__(self):
        return self

    def _next(self):
        try:
            self.element = next(self.iterator)
        except StopIteration:
            self._has_next = False        

    def next(self):
        if not self.has_next():
            raise StopIteration
        ret_value = self.element
        self._next()
        return ret_value

    def has_next(self):
        return self._has_next

