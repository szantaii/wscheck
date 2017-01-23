import os


class FileIterator(object):
    def __init__(self, base_path=None):
        """
        :type base_path: str or None
        """
        self.__base_path = base_path
        if base_path is None:
            base_path = os.getcwd()

    def __get_full_path(self, path):
        """
        :type path: str
        :rtype: str
        """

        if path[0] == os.path.sep:
            return path

        return os.path.join(self.__base_path, path)

    def iter(self, paths, include_globs=None, exclude_globs=None):
        """
        :type paths: list
        :type include_globs: list or None
        :type exclude_globs: list or None
        :rtype: iterator
        """

        full_paths = [self.__get_full_path(path) for path in paths]

        if include_globs is None:
            include_globs = []

        if exclude_globs is None:
            exclude_globs = []

        for path in full_paths:
            yield path

    #         if os.path.isfile(include_path):
    #             yield include_path
    #             continue
    #
    #         os.walk(include_path)
    # #
    # # def _
    # #
    # #
    # #     return [x[0] for x in os.walk('/home/tia/bin')]
    # #
