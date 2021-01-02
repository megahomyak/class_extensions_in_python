import functools
import inspect

from using_init.exceptions import (
    ExtensionClassNotFoundError,
    MethodNotFoundInBaseClassError
)


class ExtensibleBase:

    def __init__(self, extension_file_name: str):
        # Getting extension class by name of the current class from imported
        # file
        try:
            extension_class: object = __import__(
                extension_file_name, fromlist=['my_class']
            ).__dict__[self.__class__.__name__]
        except KeyError:
            raise ExtensionClassNotFoundError(
                f"Nothing named '{self.__class__.__name__}' is found in file "
                f"'{extension_file_name}', which should contain the extension "
                f"class named '{self.__class__.__name__}'"
            )
        if not inspect.isclass(extension_class):
            raise ExtensionClassNotFoundError(
                f"'{self.__class__.__name__}' from '{extension_file_name}' has "
                f"type {type(extension_class)}, but it should be a class! "
                f"(type {type(type)})"  # Python...
            )
        extended_methods = {
            field_name: field
            for field_name, field in extension_class.__dict__.items()
            # Using isfunction, because ismethod isn't working, because methods
            # is from class, not from instance of a class
            if inspect.isfunction(field)
        }
        for method_name, method in extended_methods.items():
            # self.__dict__ is empty at this moment IDK why, so using
            # self.__class__.__dict__
            if method_name not in self.__class__.__dict__:
                raise MethodNotFoundInBaseClassError(
                    f"Method '{method_name}' isn't in the base class!"
                )
            # Using functools.partial because self isn't being passed to
            # methods, because they are methods from the class, not from
            # instance of a class
            self.__dict__[method_name] = functools.partial(method, self)
        # And we're done!
