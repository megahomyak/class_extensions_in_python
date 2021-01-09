from abc import abstractmethod, ABC

from using_extensible_base.extensible_base import ExtensibleBase


class Interface(ABC, ExtensibleBase):

    @abstractmethod
    def some_abstract_method(self):
        pass

    @abstractmethod
    def some_extension_method(self):
        pass
