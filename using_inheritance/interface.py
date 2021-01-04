from abc import ABC, abstractmethod

from using_inheritance.interface_extension import ExtensionForInterface


class Interface(ABC, ExtensionForInterface):

    @abstractmethod
    def some_abstract_method(self):
        pass
