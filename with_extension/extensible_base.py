import functools
import inspect

from with_extension.exceptions import (
    ExtensionClassNotFoundError,
    MethodNotFoundInBaseClassError
)


class ExtensibleBase:

    def __init__(self, extension_file_name: str):
        # Getting extension class by name of the current class from imported
        # file
        try:
            extension_class: object = __import__(
                extension_file_name, fromlist=[self.__class__.__name__]
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
        for field_name, field in extension_class.__dict__.items():
            try:
                if (
                    callable(field) or callable(field.__get__)
                    and field_name not in ("__dict__", "__weakref__")
                ):
                    # Using self.__class__.__dict__ cuz self.__dict__ is empty
                    if field_name not in self.__class__.__dict__:
                        raise MethodNotFoundInBaseClassError(
                            f"Method '{field_name}' isn't in the base class!"
                        )
                    if callable(field):
                        pure_method = field
                    else:
                        pure_method = field.__get__
                    # Using functools.partial because self isn't being passed to
                    # methods, because they are methods from the class, not from
                    # instance of a class
                    self.__dict__[field_name] = functools.partial(
                        pure_method, self
                    )
            except AttributeError:
                pass
