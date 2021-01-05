import functools
import inspect
from typing import Optional

from using_extensible_base.exceptions import (
    ExtensionClassNotFoundError,
    MethodNotFoundInBaseClassError
)


class ExtensibleBase:

    def __init__(
            self, extension_file_name: str, class_name: Optional[str] = None):
        # Getting extension class by name of the current class from imported
        # file
        if class_name is None:
            class_name = self.__class__.__name__
        try:
            extension_class: object = __import__(
                extension_file_name, fromlist=[class_name]
            ).__dict__[class_name]
        except KeyError:
            raise ExtensionClassNotFoundError(
                f"Nothing named '{class_name}' is found in file "
                f"'{extension_file_name}', which should contain the extension "
                f"class named '{class_name}'"
            )
        if not inspect.isclass(extension_class):
            raise ExtensionClassNotFoundError(
                f"'{class_name}' from '{extension_file_name}' has "
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
