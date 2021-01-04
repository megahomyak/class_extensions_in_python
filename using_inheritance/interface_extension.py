from abc import ABC

from using_inheritance.implemented_interface import ImplementedInterface


class ExtensionForInterface(ABC):

    # noinspection PyMethodMayBeStatic
    def some_extension_method(self) -> ImplementedInterface:
        return ImplementedInterface()
