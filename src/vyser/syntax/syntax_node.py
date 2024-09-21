from abc import abstractmethod


class SyntaxNode:

    @property
    @abstractmethod
    def kind(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def get_children(self):
        raise NotImplementedError
