from using_extensible_base.tests.interfaces.interface import Interface


class ImplementedInterface(Interface):

    def some_abstract_method(self):
        pass

    # noinspection PyMissingConstructor,PyInitNewSignature
    def __init__(self):  # Overriding __init__ to remove extensibility
        pass
