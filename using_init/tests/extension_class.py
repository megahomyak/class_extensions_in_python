class A:

    # noinspection PyMethodMayBeStatic
    def a(self):
        print("regular method")
        # noinspection PyUnresolvedReferences,PyStatementEffect
        self._check

    @staticmethod
    def b():
        print("@staticmethod")

    @classmethod
    def c(cls):
        print("@classmethod")

    # noinspection PyPropertyDefinition
    # because I don't want to return anything; let it be None
    @property
    def d(self):
        print("@property")
        # noinspection PyUnresolvedReferences,PyStatementEffect
        self._check
