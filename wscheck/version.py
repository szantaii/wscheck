from typing import Tuple

__version__ = (1, 3, 2)


class Version:
    def __init__(self) -> None:
        version_string_array = [str(v) for v in __version__]
        self.__version = '.'.join(version_string_array[:3])
        self.__release = '-'.join([self.__version] + version_string_array[3:])

    @property
    def version_array(self) -> Tuple[int, int, int]:
        return __version__

    @property
    def version(self) -> str:
        return self.__version

    @property
    def release(self) -> str:
        return self.__release
