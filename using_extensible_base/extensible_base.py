import inspect
from typing import Optional

from using_extensible_base.exceptions import (
    ExtensionClassNotFoundError
)


class ExtensibleBase:

    @classmethod
    def extend(
            cls, extension_file_name: str,
            class_name: Optional[str] = None) -> None:
        if class_name is None:
            class_name = cls.__name__
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
        for field_name in dir(extension_class):
            try:
                setattr(cls, field_name, getattr(extension_class, field_name))
            except AttributeError:
                pass
