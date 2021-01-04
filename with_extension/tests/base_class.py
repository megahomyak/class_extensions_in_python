from with_extension.extensible_base import ExtensibleBase


class A(ExtensibleBase):

    def __init__(self, extension_file_name: str):
        super().__init__(extension_file_name)
        self._check = True

    def a(self):
        raise NotImplementedError

    @staticmethod
    def b():
        raise NotImplementedError

    @classmethod
    def c(cls):
        raise NotImplementedError

    @property
    def d(self):
        raise NotImplementedError
