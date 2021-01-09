from abc import ABC

from using_extensible_base.tests.interfaces.implemented_interface \
    import ImplementedInterface


class Interface(ABC):

    # noinspection PyMethodMayBeStatic
    def some_extension_method(self) -> ImplementedInterface:
        return ImplementedInterface()
