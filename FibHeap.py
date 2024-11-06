class Node:
    def __init__(self, key, value):
        self.key = key  # Priority of the node
        self.value = value  # Value associated with the node (e.g., location or identifier)
        self.degree = 0  # Number of children
        self.parent = None  # Parent node
        self.child = None  # Child node
        self.mark = False  # True if the node has lost a child since it became a child of another node
        self.left = self  # Sibling pointers
        self.right = self  # Sibling pointers

class FibHeap:
    def __init__(self):
        self.min_node = None  # Minimum node
        self.total_nodes = 0  # Total nodes in the heap

    def insert(self, key, value):
        """Inserts a new node with the given key and value."""
        new_node = Node(key, value)
        if self.min_node is None:
            self.min_node = new_node
        else:
            # Insert new node into the root list
            new_node.left = self.min_node
            new_node.right = self.min_node.right
            self.min_node.right.left = new_node
            self.min_node.right = new_node
            if new_node.key < self.min_node.key:
                self.min_node = new_node
        self.total_nodes += 1
        return new_node

    def extract_min(self):
        """Removes and returns the node with the smallest key."""
        z = self.min_node
        if z is not None:
            # Move each child of z to the root list
            if z.child is not None:
                children = []
                child = z.child
                while True:
                    children.append(child)
                    child = child.right
                    if child == z.child:
                        break
                for child in children:
                    # Add child to root list
                    child.left.right = child.right
                    child.right.left = child.left
                    child.left = self.min_node
                    child.right = self.min_node.right
                    self.min_node.right.left = child
                    self.min_node.right = child
                    child.parent = None

            # Remove z from the root list
            z.left.right = z.right
            z.right.left = z.left
            if z == z.right:
                self.min_node = None
            else:
                self.min_node = z.right
                self._consolidate()

            self.total_nodes -= 1

        return z

    def decrease_key(self, x, new_key):
        """Decreases the key of node x to new_key."""
        if new_key > x.key:
            raise ValueError("New key is greater than current key")

        x.key = new_key
        y = x.parent

        if y is not None and x.key < y.key:
            self._cut(x, y)
            self._cascading_cut(y)

        if x.key < self.min_node.key:
            self.min_node = x

    def _consolidate(self):
        """Consolidates trees in the root list to maintain heap properties."""
        max_degree = int(self.total_nodes ** 0.5) + 1
        A = [None] * max_degree

        # List of root nodes to check
        nodes = []
        x = self.min_node
        if x is not None:
            while True:
                nodes.append(x)
                x = x.right
                if x == self.min_node:
                    break

        for w in nodes:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self._link(y, x)
                A[d] = None
                d += 1
            A[d] = x

        # Reconstruct the root list from A
        self.min_node = None
        for i in range(max_degree):
            if A[i] is not None:
                if self.min_node is None or A[i].key < self.min_node.key:
                    self.min_node = A[i]

    def _link(self, y, x):
        """Links node y as a child of node x."""
        y.left.right = y.right
        y.right.left = y.left
        y.parent = x

        if x.child is None:
            x.child = y
            y.right = y
            y.left = y
        else:
            y.left = x.child
            y.right = x.child.right
            x.child.right.left = y
            x.child.right = y

        x.degree += 1
        y.mark = False

    def _cut(self, x, y):
        """Cuts x from its parent y and moves it to the root list."""
        if x.right == x:
            y.child = None
        else:
            x.left.right = x.right
            x.right.left = x.left
            if y.child == x:
                y.child = x.right

        y.degree -= 1
        x.left = self.min_node
        x.right = self.min_node.right
        self.min_node.right.left = x
        self.min_node.right = x
        x.parent = None
        x.mark = False

    def _cascading_cut(self, y):
        """Performs cascading cuts to maintain the Fibonacci heap properties."""
        z = y.parent
        if z is not None:
            if y.mark is False:
                y.mark = True
            else:
                self._cut(y, z)
                self._cascading_cut(z)
