# node.py

# 赤黒木のノードの色を表す定数
RED = 0
BLACK = 1


class Node:
    def __init__(self, key, color, parent=None, left=None, right=None):
        self.key = key
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right
