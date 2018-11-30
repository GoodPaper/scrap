class Singleton:

    _instance = None

    @classmethod
    def _getInstance( cls ):

        return cls._instance

    @classmethod
    def instance( cls ):

        cls._instance = cls()
        cls.instance = cls._getInstance
        return cls._instance
