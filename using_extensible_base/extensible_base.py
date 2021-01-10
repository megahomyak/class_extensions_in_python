import functools
import inspect
import itertools
from copy import deepcopy
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
                    if field_name not in [
                        self.__class__.__dict__,
                        *[
                            superclass.__dict__
                            for superclass in self.__class__.__mro__
                        ]  # Jewish tricks
                    ]:
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

    def __new__(
            cls, extension_file_name: str,
            class_name: Optional[str] = None, **kwargs):
        if class_name is None:
            class_name = cls.__name__
        cls_copy = deepcopy(cls)
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
        all_accessible_fields = {
            *cls_copy.__dict__.keys(),
            *list(itertools.chain(
                *[superclass.__dict__.keys() for superclass in cls_copy.__mro__]
            ))
            # Jewish tricks
        }
        print(all_accessible_fields)
        for field_name, field in extension_class.__dict__.items():
            try:
                if (
                    callable(field) or callable(field.__get__)
                    and field_name not in ("__dict__", "__weakref__")
                ):
                    # Using self.__class__.__dict__ cuz self.__dict__ is empty
                    if field_name not in all_accessible_fields:
                        raise MethodNotFoundInBaseClassError(
                            f"Method '{field_name}' isn't in the base "
                            f"class or its subclasses!"
                        )
                    if callable(field):
                        pure_method = field
                    else:
                        pure_method = field.__get__
                    # Using functools.partial because self isn't being passed to
                    # methods, because they are methods from the class, not from
                    # instance of a class
                    setattr(cls_copy, field_name, pure_method)
            except AttributeError:
                pass
        # noinspection PyArgumentList
        print("fdfosjds", cls_copy.__dict__)
        return super(cls_copy, cls).__new__(
            cls_copy, extension_file_name=extension_file_name,
            class_name=class_name
        )
