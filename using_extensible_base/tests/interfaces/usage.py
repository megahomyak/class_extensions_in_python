from using_extensible_base.tests.interfaces.interface import Interface


class ExtendedInterfaceImplemented(Interface):

    # noinspection PyMethodMayBeStatic
    def some_abstract_method(self):
        print("abc")


ExtendedInterfaceImplemented.extend(
    "using_extensible_base.tests.interfaces.interface_extension", "Interface"
)
extended_interface_implemented = ExtendedInterfaceImplemented()
extended_interface_implemented.some_abstract_method()
print(extended_interface_implemented.some_extension_method())
