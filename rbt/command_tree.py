# command_tree.py

from .base_tree import ThreadSafeRedBlackTree
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class InsertCommand(Command):
    def __init__(self, tree, key):
        self.tree = tree
        self.key = key

    def execute(self):
        self.tree.super_insert(self.key)

    def undo(self):
        self.tree.super_delete(self.key)


class DeleteCommand(Command):
    def __init__(self, tree, key):
        self.tree = tree
        self.key = key

    def execute(self):
        self.tree.super_delete(self.key)

    def undo(self):
        self.tree.super_insert(self.key)


class CommandRedBlackTree(ThreadSafeRedBlackTree):
    def __init__(self):
        super().__init__()
        self.commands = []

    def insert(self, key):
        cmd = InsertCommand(self, key)
        with self.lock:
            cmd.execute()
            self.commands.append(cmd)

    def super_insert(self, key):
        super().insert(key)

    def delete(self, key):
        cmd = DeleteCommand(self, key)
        with self.lock:
            cmd.execute()
            self.commands.append(cmd)

    def super_delete(self, key):
        super().delete(key)

    def undo(self):
        with self.lock:
            if self.commands:
                command = self.commands.pop()
                command.undo()
