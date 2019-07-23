# Python3.7.4
# Chapter 4.


# 4.1 Manually Consuming an Iterator

with open('/etc/passwd') as f:
    try:
        while True:
            line = next(f)
#            print(line, end='')
    except StopIteration:
        pass

"""Normally, StopIteration is used to signal the end of iteration. If you're
using next() manually, you can instruct it to return a terminating value
such as None, instead"""

with open('/etc/passwd') as f:
    while True:
        line = next(f, None)
        if line is None:
            break
#        print(line, end='')

# This is what happens illustrating basic mechanics during iteration.

items = [1, 2, 3]

# Get the iterator.

it = iter(items)  # Invokes items.__iter__()

# Run the iterator

print(next(it))   # Invokes it.__next__()
print(next(it))
print(next(it))


# 4.2 Delegation Iteration

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

# Example:

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    for ch in root:
        print(ch)


# 4.3 Creating New Iteration Patterns with Generators

# Example creating generator that produces range of floating-point numbers.

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

"""To use this function, iterate over it using a for loop or some other
function that consumes an iterable"""

for n in frange(0, 4, 0.5):
    print(n)

print(list(frange(0, 1, 0.125)))

"""The presence of a yield statement in a function turns it into a
generator. Unlike a normal function, a generator only runs in response
to iteration"""

def countdown(n):
    print('Starting to count from', n)
    while n > 0:
            yield n
            n -= 1
    print('Done!')

# Create the generator, no output appears.

c = countdown(3)

print(c)

# Run to first yield & emit a value.

print(next(c))  # 3
print(next(c))  # 2
print(next(c))  # 1
# print(next(c))  # Done! & Traceback error.


# 4.4 Implementing the Iterator Protocol

"""Traversing nodes in a depth-first pattern"""

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        yield self
        for c in self:
            yield from c.depth_first()

# Example:

if __name__ == '__main__':
    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for ch in root.depth_first():
        print(ch)

# Alternative implementation of the depth_first() method.

class Node:
    def __init__(self, value):
        self._value = value
        self._children = []

    def __repr__(self):
        return 'Node({!r})'.format(self._value)

    def add_child(self, other_node):
        self._children.append(other_node)

    def __iter__(self):
        return iter(self._children)

    def depth_first(self):
        return DepthFirstIterator(self)

class DepthFirstIterator(object):
    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __iter__(self):
        return self

    def __next__(self):
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node

        # If processing a child, return its next item
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)

        # Advance to the next child & start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)


# 4.5 Iterating in Reverse

a = [1, 2, 3, 4]
for x in reversed(a):
    print(x)

"""Only works if object has a size that can be determined or implements
a __reversed__() special method"""

f = open('somefile.txt')
for line in reversed(list(f)):
    print(line, end='')

"""Turning an iterable into a list as shown could consume a lot of memory
if it's large"""

# Reversed iteration customized on user-defined classes.

class Countdown:
    def __init__(self, start):
        self.start = start

    # Forward iterator
    def __iter__(self):
        n = self.start
        while n > 0:
            yield n
            n -= 1

    # Reverse Iterator
    def __reversed__(self):
        n = 1
        while n <= self.start:
            yield n
            n += 1
