# base_tree.py

import threading
from copy import deepcopy
from .node import Node, RED, BLACK


class ThreadSafeRedBlackTree:
    def __init__(self):
        self.NIL_LEAF = Node(None, BLACK)
        self.root = self.NIL_LEAF
        self.lock = threading.Lock()

    def _rotate_left(self, node):
        right_temp = node.right
        node.right = right_temp.left
        if right_temp.left != self.NIL_LEAF:
            right_temp.left.parent = node
        right_temp.parent = node.parent
        if node.parent is None:
            self.root = right_temp
        elif node == node.parent.left:
            node.parent.left = right_temp
        else:
            node.parent.right = right_temp
        right_temp.left = node
        node.parent = right_temp

    def _rotate_right(self, node):
        left_temp = node.left
        node.left = left_temp.right
        if left_temp.right != self.NIL_LEAF:
            left_temp.right.parent = node
        left_temp.parent = node.parent
        if node.parent is None:
            self.root = left_temp
        elif node == node.parent.right:
            node.parent.right = left_temp
        else:
            node.parent.left = left_temp
        left_temp.right = node
        node.parent = left_temp

    def _insert_fix(self, node):
        while node != self.root and node.parent.color == RED:
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._rotate_right(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle.color == RED:
                    uncle.color = BLACK
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self._rotate_left(node.parent.parent)
        self.root.color = BLACK

    def insert(self, key):
        with self.lock:
            new_node = Node(key, RED, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            temp = self.root
            parent = None
            while temp != self.NIL_LEAF:
                parent = temp
                if key < temp.key:
                    temp = temp.left
                else:
                    temp = temp.right
            new_node.parent = parent
            if parent is None:
                self.root = new_node
            elif key < parent.key:
                parent.left = new_node
            else:
                parent.right = new_node
            self._insert_fix(new_node)

    def search(self, key):
        with self.lock:
            node = self.root
            while node != self.NIL_LEAF and node.key != key:
                if key < node.key:
                    node = node.left
                else:
                    node = node.right
            return node.key if node != self.NIL_LEAF else None

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _delete_fix(self, x):
        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self._rotate_right(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self._rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self._rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self._rotate_right(x.parent)
                    x = self.root
        x.color = BLACK

    def delete(self, key):
        with self.lock:
            z = self.root
            while z != self.NIL_LEAF and z.key != key:
                if key < z.key:
                    z = z.left
                else:
                    z = z.right
            if z == self.NIL_LEAF:
                return
            y = z
            y_original_color = y.color
            if z.left == self.NIL_LEAF:
                x = z.right
                self._transplant(z, z.right)
            elif z.right == self.NIL_LEAF:
                x = z.left
                self._transplant(z, z.left)
            else:
                y = z.right
                while y.left != self.NIL_LEAF:
                    y = y.left
                y_original_color = y.color
                x = y.right
                if y.parent == z:
                    x.parent = y
                else:
                    self._transplant(y, y.right)
                    y.right = z.right
                    y.right.parent = y
                self._transplant(z, y)
                y.left = z.left
                y.left.parent = y
                y.color = z.color
            if y_original_color == BLACK:
                self._delete_fix(x)

    def predecessor(self, key):
        with self.lock:
            node = self.search(key)
            if node is None:  # If node with specified key doesn't exist
                return None

            if node.left != self.NIL_LEAF:
                node = node.left
                while node.right != self.NIL_LEAF:
                    node = node.right
                return node

            while node.parent and node == node.parent.left:
                node = node.parent

            return node.parent

    def __deepcopy__(self, memo):
        with self.lock:
            new_tree = ThreadSafeRedBlackTree()
            memo[id(self)] = new_tree  # Add this instance to memo

            # Only deepcopy the root (which will recursively deepcopy the tree)
            new_tree.root = deepcopy(self.root, memo)

            # Create a new lock instance instead of copying the old one
            new_tree.lock = threading.Lock()

            return new_tree
