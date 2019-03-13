# -*- coding: utf-8 -*-

'''Image meta information.'''

from pathlib import Path


class ImageInfo:
    '''Container for image meta information'''

    def __init__(self, path, index):
        self.path = Path(path).resolve()
        self.fname = self.path.name
        self.index = int(index)

    def __str__(self):
        return str(self.path)
