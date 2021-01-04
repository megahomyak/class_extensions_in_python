from using_inheritance.interface import Interface


class ExtendedInterfaceImplemented(Interface):

    # noinspection PyMethodMayBeStatic
    def some_abstract_method(self):
        print("abc")


extended_interface_implemented = ExtendedInterfaceImplemented()
extended_interface_implemented.some_abstract_method()
print(extended_interface_implemented.some_extension_method())
